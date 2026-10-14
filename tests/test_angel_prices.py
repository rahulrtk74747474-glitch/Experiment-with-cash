"""No-network tests of read-only Angel One price fallback and safety rules."""
import os
import unittest
from unittest.mock import Mock, patch

from src.angel_prices import (
    AngelHistoricalPrices, AngelPriceError, _dated_candle, _exact_instrument, configured,
)


class TestAngelPriceFallback(unittest.TestCase):
    def test_no_credentials_means_no_connection(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(configured())
            with self.assertRaisesRegex(AngelPriceError, "not configured"):
                AngelHistoricalPrices().get_nse_quote("V2RETAIL", "2026-10-14")

    def test_exact_nse_cash_symbol_not_similarly_named_security(self):
        response = {"status": True, "data": [
            {"exchange": "NSE", "tradingsymbol": "V2RETAIL-AB", "symboltoken": "111"},
            {"exchange": "NSE", "tradingsymbol": "V2RETAIL-EQ", "symboltoken": "222"},
            {"exchange": "NSE", "tradingsymbol": "V2RETAIL-BE", "symboltoken": "333"},
        ]}
        self.assertEqual(_exact_instrument(response, "V2RETAIL"), "222")
        with self.assertRaisesRegex(AngelPriceError, "No exact"):
            _exact_instrument({"status": True, "data": [
                {"exchange": "NSE", "tradingsymbol": "V2RETAIL-AB", "symboltoken": "111"}]},
                "V2RETAIL")

    def test_intraday_candle_timestamp_and_valid_close(self):
        api = Mock()
        api.searchScrip.return_value = {"status": True, "data": [
            {"exchange": "NSE", "tradingsymbol": "V2RETAIL-EQ", "symboltoken": "222"}
        ]}
        api.getCandleData.return_value = {"status": True, "data": [
            ["2026-10-13T14:46:00+05:30", 150, 151, 149, 150.3, 100],
            ["2026-10-13T15:28:00+05:30", 151, 152, 150, 151.45, 200],
            ["2026-10-13T15:29:00+05:30", 153, 155, 152, 154, 900],
            ["2026-10-14T15:27:00+05:30", 155, 157, 154, 156, 900],
        ]}
        quote = AngelHistoricalPrices(client=api).get_nse_quote("V2RETAIL", "2026-10-13")
        self.assertEqual(quote["price"], 151.45)
        self.assertEqual(quote["source"], "Angel One SmartAPI NSE 1m")
        self.assertTrue(quote["quote_time"].startswith("2026-10-13T15:28"))
        api.getCandleData.assert_called_once_with({
            "exchange": "NSE", "symboltoken": "222", "interval": "ONE_MINUTE",
            "fromdate": "2026-10-13 14:45", "todate": "2026-10-13 15:28",
        })

    def test_stale_candles_cannot_cause_paper_exits(self):
        with self.assertRaisesRegex(AngelPriceError, "No same-session"):
            _dated_candle({"status": True, "data": [
                ["2026-10-12T15:28:00+05:30", 100, 100, 100, 100, 500],
            ]}, "V2RETAIL", "2026-10-13")

    def test_error_response_cannot_be_misread_as_valid_market_price(self):
        with self.assertRaises(AngelPriceError):
            _dated_candle({"status": False, "message": "Rate limit", "data": []},
                          "V2RETAIL", "2026-10-13")

    def test_missing_or_ambiguous_token_must_fail(self):
        with self.assertRaisesRegex(AngelPriceError, "Ambiguous"):
            _exact_instrument({"status": True, "data": [
                {"tradingsymbol": "V2RETAIL-EQ", "symboltoken": "111"},
                {"tradingsymbol": "V2RETAIL-EQ", "symboltoken": "222"},
            ]}, "V2RETAIL")

    def test_connection_error_does_not_echo_secrets(self):
        api = Mock()
        api.searchScrip.side_effect = RuntimeError("secretTestPin could not authenticate")
        with self.assertRaises(AngelPriceError) as caught:
            AngelHistoricalPrices(client=api).get_nse_quote("V2RETAIL", "2026-10-13")
        self.assertNotIn("secretTestPin", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
