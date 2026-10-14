"""Read-only Angel One integration check.

Run ONLY within the private-in-practice GitHub Actions job after adding secrets.
Do not print environment values, SDK responses, bearer tokens, or TOTP digits.
Does not change portfolio state or submit any orders.
"""
from __future__ import annotations
import contextlib
import io
import os
import sys

from src.angel_prices import AngelHistoricalPrices, AngelPriceError, REQUIRED_ENV


def main() -> int:
    missing = [name for name in REQUIRED_ENV if not os.getenv(name, "").strip()]
    if missing:
        print("ANGEL_CHECK=CONFIG_MISSING")
        print("Missing repository secret names: " + ", ".join(missing))
        return 2
    print("ANGEL_CHECK=SECRETS_PRESENT (values not displayed)", flush=True)
    try:
        import pyotp
        from SmartApi import SmartConnect
        assert callable(SmartConnect)
        assert callable(pyotp.TOTP)
        print("ANGEL_CHECK=SDK_IMPORT_OK", flush=True)
    except Exception:
        print("ANGEL_CHECK=SDK_IMPORT_FAILED; inspect requirements", flush=True)
        return 3

    # Suppress any verbose response bodies emitted by external SDK.
    api = AngelHistoricalPrices()
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            api._client()
        print("ANGEL_CHECK=AUTHENTICATED", flush=True)
    except AngelPriceError as exc:
        # The adapter masks network and SDK responses.
        print("ANGEL_CHECK=AUTHENTICATION_FAILED")
        print("Reason: " + str(exc))
        return 4
    except Exception:
        print("ANGEL_CHECK=UNEXPECTED_AUTHENTICATION_FAILURE")
        return 4

    # Request a dated 1-minute candle for a known liquid NSE equity.
    # No real orders, no portfolio state changes.
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            quote = api.get_nse_quote("RELIANCE", "2026-10-14")
        print("ANGEL_CHECK=HISTORICAL_PRICE_OK")
        print("Symbol: RELIANCE; NSE quote date: " + quote["quote_time"][:10]
              + "; source: " + quote["source"])
        return 0
    except AngelPriceError as exc:
        print("ANGEL_CHECK=HISTORICAL_PRICE_FAILED")
        print("Reason: " + str(exc))
        return 5
    except Exception:
        print("ANGEL_CHECK=UNEXPECTED_HISTORICAL_PRICE_FAILURE")
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
