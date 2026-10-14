"""Read-only NSE daily closing prices from Angel One SmartAPI.

No brokerage order functions are called anywhere in this module.
Credentials are provided only through environment variables / GitHub Actions secrets.
No network connection is made when unconfigured.
"""
from __future__ import annotations

import math
import os
from datetime import date, datetime, time

import requests
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


def _daily_candle(response: dict, symbol: str, expected_date: str) -> dict:
    """Require an actual NSE daily OHLC candle on the target session date.

    SmartAPI timestamps ONE_DAY bars at the *start* of a daily candle.
    Its close field is the daily close, not an execution price at that timestamp.
    """
    if not isinstance(response, dict) or response.get("status") is not True:
        raise AngelPriceError(f"Angel One NSE ONE_DAY request rejected for {symbol}")
    candles = response.get("data")
    if not isinstance(candles, list):
        raise AngelPriceError(f"Angel One returned no NSE daily OHLC data for {symbol}")
    valid = []
    for row in candles:
        if not isinstance(row, (list, tuple)) or len(row) < 5:
            continue
        try:
            at = datetime.fromisoformat(str(row[0]).replace("Z", "+00:00"))
            if at.tzinfo is None:
                at = at.replace(tzinfo=IST)
            at = at.astimezone(IST)
            close = float(row[4])
            if at.date().isoformat() == expected_date and math.isfinite(close) and close > 0:
                valid.append((at, close))
        except (ValueError, TypeError, OverflowError):
            continue
    if len(valid) != 1:
        raise AngelPriceError(
            f"Expected exactly one valid NSE ONE_DAY bar for {symbol} on {expected_date}; got {len(valid)}"
        )
    at, close = valid[0]
    return {
        "price": round(close, 4),
        "quote_time": at.isoformat(),
        "source": "Angel One SmartAPI NSE ONE_DAY daily close",
    }


MASTER_URL = "https://margincalculator.angelone.in/OpenAPI_File/files/OpenAPIScripMaster.json"


def _token_from_master(records: list, symbol: str) -> str:
    """Resolve an NSE cash-equity token from Angel One's published instrument master.

    Never choose derivative, BSE or partial-name symbols. Reject ambiguous tokens.
    """
    if not isinstance(records, list):
        raise AngelPriceError("Angel One instrument master has an invalid format")
    matches = []
    for row in records:
        if not isinstance(row, dict):
            continue
        seg = str(row.get("exch_seg", "")).strip().lower()
        if seg not in ("nse", "nse_cm"):
            continue
        if str(row.get("expiry") or "").strip():
            continue
        if str(row.get("instrumenttype") or "").strip().upper() not in ("", "EQ"):
            continue
        name = str(row.get("symbol", "")).strip().upper()
        if name not in (symbol, symbol + "-EQ", symbol + "-BE", symbol + "-BZ"):
            continue
        token = str(row.get("token") or "").strip()
        if token.isdigit() and int(token) > 0:
            matches.append((name, token))
    for suffix in ("-EQ", "", "-BE", "-BZ"):
        exact = {token for name, token in matches if name == symbol + suffix}
        if len(exact) == 1:
            return next(iter(exact))
        if len(exact) > 1:
            raise AngelPriceError(f"Ambiguous NSE instrument master tokens for {symbol}")
    raise AngelPriceError(f"No exact NSE equity token found in instrument master for {symbol}")


class AngelHistoricalPrices:
    def __init__(self, client=None):
        self.client = client
        self.tokens = {}
        self._master_records = None

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

    def _token(self, symbol: str, client) -> str:
        if symbol not in self.tokens:
            try:
                self.tokens[symbol] = _exact_instrument(client.searchScrip("NSE", symbol), symbol)
            except Exception:
                if self._master_records is None:
                    try:
                        response = requests.get(MASTER_URL, timeout=(9, 55))
                        response.raise_for_status()
                        records = response.json()
                        if not isinstance(records, list):
                            raise ValueError("Non-array Angel instrument master")
                        self._master_records = records
                    except Exception:
                        raise AngelPriceError(
                            f"Angel One instrument master unavailable for {symbol}"
                        ) from None
                self.tokens[symbol] = _token_from_master(self._master_records, symbol)
        return self.tokens[symbol]

    def get_daily_close(self, symbol: str, expected_date: str) -> dict:
        """Retrieve the verified daily close for one NSE trading session.

        Never substitute a scanner price, a minute bar or a prior-day close.
        """
        symbol = str(symbol).strip().upper().removesuffix(".NS")
        if not symbol or not symbol.replace("-", "").replace("&", "").replace("_", "").isalnum():
            raise AngelPriceError("Invalid NSE symbol")
        try:
            date.fromisoformat(expected_date)
        except ValueError as exc:
            raise AngelPriceError("Invalid NSE session date") from exc
        client = self._client()
        token = self._token(symbol, client)
        query = {
            "exchange": "NSE",
            "symboltoken": token,
            "interval": "ONE_DAY",
            "fromdate": expected_date + " 09:00",
            "todate": expected_date + " 15:35",
        }
        try:
            response = client.getCandleData(query)
        except Exception:
            raise AngelPriceError(f"Angel One daily close request failed for {symbol}") from None
        return _daily_candle(response, symbol, expected_date)

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
            # Angel searchScrip can return a successful but empty result even
            # for a listed symbol. Angel publishes an exact instrument master.
            try:
                response = client.searchScrip("NSE", symbol)
                self.tokens[symbol] = _exact_instrument(response, symbol)
            except Exception:
                # Public instrument-master endpoint; never send login secrets.
                if self._master_records is None:
                    try:
                        response = requests.get(MASTER_URL, timeout=(9, 55))
                        response.raise_for_status()
                        records = response.json()
                        if not isinstance(records, list):
                            raise ValueError("Non-array instrument master")
                        self._master_records = records
                    except Exception:
                        raise AngelPriceError(
                            f"Angel One instrument search and master list unavailable for {symbol}"
                        ) from None
                self.tokens[symbol] = _token_from_master(self._master_records, symbol)
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
