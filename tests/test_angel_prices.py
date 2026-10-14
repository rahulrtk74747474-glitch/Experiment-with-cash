"""No-network tests of read-only Angel One price fallback and safety rules."""
import os
import unittest
from unittest.mock import Mock, patch

from src.angel_prices import (
    AngelHistoricalPrices, AngelPriceError, _dated_candle, _exact_instrument, configured,
)


class TestAngelPriceFallback(unittest.TestCase):
    def test_official_smartapi_sdk_imports_on_workflow_runner(self):
        # Detect missing third-party runtime imports before a credentialed run.
        from SmartApi import SmartConnect
        import pyotp
        self.assertTrue(callable(SmartConnect))
        self.assertTrue(callable(pyotp.TOTP))

    def test_official_instrument_master_fallback_when_search_is_empty(self):
        api = Mock()
        api.searchScrip.return_value = {"status": True, "data": []}
        api.getCandleData.return_value = {"status": True, "data": [
            ["2026-10-14T15:28:00+05:30", 100, 101, 99, 100.8, 200]
        ]}
        source = AngelHistoricalPrices(client=api)
        source._master_records = [
            {"symbol": "RELIANCE-EQ", "token": "2885", "exch_seg": "NSE",
             "expiry": "", "instrumenttype": ""},
            {"symbol": "RELIANCE24OCTFUT", "token": "12345",
             "exch_seg": "NFO", "expiry": "24OCT2026", "instrumenttype": "FUT"},
        ]
        quote = source.get_nse_quote("RELIANCE", "2026-10-14")
        self.assertEqual(quote["price"], 100.8)
        self.assertEqual(api.getCandleData.call_args.args[0]["symboltoken"], "2885")

    def test_instrument_master_rejects_bse_and_unrelated_or_ambiguous_tokens(self):
        from src.angel_prices import _token_from_master
        with self.assertRaisesRegex(AngelPriceError, "No exact"):
            _token_from_master([
                {"symbol": "RELIANCE-EQ", "token": "12", "exch_seg": "BSE"},
                {"symbol": "RELIANCE-EQ", "token": "13", "exch_seg": "NFO"},
            ], "RELIANCE")
        with self.assertRaisesRegex(AngelPriceError, "Ambiguous"):
            _token_from_master([
                {"symbol": "RELIANCE-EQ", "token": "12", "exch_seg": "NSE"},
                {"symbol": "RELIANCE-EQ", "token": "13", "exch_seg": "NSE"},
            ], "RELIANCE")

    def test_daily_ohlc_close_includes_only_exact_session_candle(self):
        from src.angel_prices import _daily_candle
        response = {"status": True, "data": [
            ["2026-10-14T09:15:00+05:30", 100, 103, 99, 101.22, 9000],
            ["2026-10-13T09:15:00+05:30", 100, 103, 99, 999.0, 9000],
        ]}
        data = _daily_candle(response, "RELIANCE", "2026-10-14")
        self.assertEqual(data["price"], 101.22)
        self.assertIn("ONE_DAY", data["source"])
        self.assertTrue(data["quote_time"].startswith("2026-10-14"))

    def test_daily_lookup_invokes_only_smartapi_daily_history(self):
        api = Mock()
        api.searchScrip.return_value={"status":True,"data":[
            {"exchange":"NSE","tradingsymbol":"TCS-EQ","symboltoken":"11536"}]}
        api.getCandleData.return_value={"status":True,"data":[
            ["2026-10-14T09:15:00+05:30",3000,3010,2990,3001.5,5000]]}
        client=AngelHistoricalPrices(client=api)
        q=client.get_daily_close("TCS","2026-10-14")
        self.assertEqual(q["price"],3001.5)
        api.getCandleData.assert_called_once_with({
            "exchange":"NSE","symboltoken":"11536","interval":"ONE_DAY",
            "fromdate":"2026-10-14 09:00","todate":"2026-10-14 15:35"})
        self.assertFalse(api.placeOrder.called)

    def test_daily_close_rejects_stale_bars(self):
        from src.angel_prices import _daily_candle
        with self.assertRaisesRegex(AngelPriceError,"exactly one valid"):
            _daily_candle({"status":True,"data":[
                ["2026-10-13T09:15:00+05:30",100,101,99,100.2,10]
            ]},"TCS","2026-10-14")

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
