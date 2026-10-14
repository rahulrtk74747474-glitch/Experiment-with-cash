"""Read-only NSE historical price fallback through Angel One SmartAPI.

No brokerage order functions are called anywhere in this module.
Credentials are provided only through environment variables / GitHub Actions secrets.
No network connection is made when unconfigured.
"""
from __future__ import annotations

import os
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
REQUIRED_ENV = ("ANGEL_API_KEY", "ANGEL_CLIENT_CODE", "ANGEL_PIN", "ANGEL_TOTP_SECRET")


class AngelPriceError(RuntimeError):
    """Non-sensitive public error; never expose responses containing credentials."""


def configured() -> bool:
    return all(os.environ.get(key, "").strip() for key in REQUIRED_ENV)


def _exact_instrument(results: dict, symbol: str) -> str:
    """Match only the requested NSE cash symbol; never use a fuzzy search hit."""
    if not isinstance(results, dict) or results.get("status") is not True:
        raise AngelPriceError(f"Angel One NSE instrument search failed for {symbol}")
    rows = results.get("data")
    if not isinstance(rows, list) or not rows:
        raise AngelPriceError(f"No NSE instrument was found for {symbol}")
    exact = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if str(row.get("exchange", "NSE")).upper() != "NSE":
            continue
        candidate = str(row.get("tradingsymbol", "")).strip().upper()
        if candidate not in (symbol, symbol + "-EQ", symbol + "-BE", symbol + "-BZ"):
            continue
        token = row.get("symboltoken")
        if token is not None and str(token).strip():
            exact.append((candidate, str(token).strip()))
    for preferred in (symbol + "-EQ", symbol, symbol + "-BE", symbol + "-BZ"):
        tokens = {token for name, token in exact if name == preferred}
        if len(tokens) == 1:
            return next(iter(tokens))
        if len(tokens) > 1:
            raise AngelPriceError(f"Ambiguous NSE instrument tokens for {symbol}")
    raise AngelPriceError(f"No exact NSE equity instrument was found for {symbol}")


def _dated_candle(response: dict, symbol: str, expected_date: str) -> dict:
    if not isinstance(response, dict) or response.get("status") is not True:
        raise AngelPriceError(f"Angel One historical candle lookup failed for {symbol}")
    candles = response.get("data")
    if not isinstance(candles, list):
        raise AngelPriceError(f"Angel One returned no candle data for {symbol}")
    matching = []
    for candle in candles:
        if not isinstance(candle, (list, tuple)) or len(candle) < 5:
            continue
        try:
            dt = datetime.fromisoformat(str(candle[0]).replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=IST)
            dt = dt.astimezone(IST)
            price = float(candle[4])
        except (TypeError, ValueError, OverflowError):
            continue
        if (dt.date().isoformat() == expected_date
            and time(14, 45) <= dt.time() <= time(15, 28, 59)
            and 0 < price < float("inf")):
            matching.append((dt, price))
    if not matching:
        raise AngelPriceError(
            f"No same-session NSE minute candle between 14:45–15:28 IST for {symbol} on {expected_date}"
        )
    dt, price = max(matching, key=lambda r: r[0])
    return {"price": round(price, 4), "quote_time": dt.isoformat(),
            "source": "Angel One SmartAPI NSE 1m"}


class AngelHistoricalPrices:
    def __init__(self, client=None):
        self.client = client
        self.tokens = {}

    def _client(self):
        if self.client is not None:
            return self.client
        if not configured():
            raise AngelPriceError("Angel One credentials are not configured in this repository")
        # Import only when needed, so optional pricing leaves the scanner usable.
        try:
            import pyotp
            from SmartApi import SmartConnect
            api = SmartConnect(api_key=os.environ["ANGEL_API_KEY"])
            totp = pyotp.TOTP(os.environ["ANGEL_TOTP_SECRET"]).now()
            login = api.generateSession(
                os.environ["ANGEL_CLIENT_CODE"],
                os.environ["ANGEL_PIN"],
                totp,
            )
            if not isinstance(login, dict) or login.get("status") is not True or not login.get("data"):
                raise AngelPriceError(
                    "Angel One authentication failed; check configured secrets, permissions and static-IP restrictions"
                )
        except AngelPriceError:
            raise
        except Exception:
            # API/SDK errors can contain sensitive request data; don't log them.
            raise AngelPriceError(
                "Angel One connection failed; check secrets, network/IP permission or SmartAPI service"
            ) from None
        self.client = api
        return api

    def get_nse_quote(self, symbol: str, expected_date: str) -> dict:
        symbol = str(symbol).strip().upper().removesuffix(".NS")
        if not symbol or not symbol.replace("-", "").replace("&", "").replace("_", "").isalnum():
            raise AngelPriceError("Invalid NSE symbol")
        try:
            date.fromisoformat(expected_date)
        except ValueError as exc:
            raise AngelPriceError("Invalid expected NSE session date") from exc

        client = self._client()
        if symbol not in self.tokens:
            try:
                response = client.searchScrip("NSE", symbol)
            except Exception:
                raise AngelPriceError(f"Angel One instrument lookup failed for {symbol}") from None
            self.tokens[symbol] = _exact_instrument(response, symbol)
        query = {
            "exchange": "NSE",
            "symboltoken": self.tokens[symbol],
            "interval": "ONE_MINUTE",
            "fromdate": expected_date + " 14:45",
            "todate": expected_date + " 15:28",
        }
        try:
            response = client.getCandleData(query)
        except Exception:
            raise AngelPriceError(f"Angel One candle request failed for {symbol}") from None
        return _dated_candle(response, symbol, expected_date)
