"""No-network regression checks: every pricing path uses Angel ONE_DAY."""
import unittest
from unittest.mock import Mock

from src.run import collect_prices, trading_allowed, latest_completed_session_date
from datetime import datetime
from zoneinfo import ZoneInfo
from src.angel_prices import AngelPriceError

IST=ZoneInfo("Asia/Kolkata")

class TestDailyPricePolicy(unittest.TestCase):
    def test_read_only_scanner_probe_uses_angel_for_every_symbol(self):
        provider=Mock()
        provider.get_daily_close.side_effect=lambda symbol, d: {
            "price":100 if symbol=="V2RETAIL" else 200,
            "quote_time":d+"T09:15:00+05:30",
            "source":"Angel One SmartAPI NSE ONE_DAY daily close"}
        results, errors=collect_prices(provider,["V2RETAIL","RELIANCE"],"2026-10-14")
        self.assertFalse(errors)
        self.assertEqual(set(results),{"V2RETAIL","RELIANCE"})
        self.assertEqual(provider.get_daily_close.call_count,2)

    def test_missing_price_cannot_be_substituted(self):
        provider=Mock()
        provider.get_daily_close.side_effect=AngelPriceError("No matching NSE candle")
        results,errors=collect_prices(provider,["V2RETAIL"],"2026-10-14")
        self.assertEqual(results,{})
        self.assertIn("V2RETAIL",errors)

    def test_schedule_requires_completed_daily_candle(self):
        self.assertFalse(trading_allowed(datetime(2026,10,15,15,29,tzinfo=IST),False))
        self.assertTrue(trading_allowed(datetime(2026,10,15,15,51,tzinfo=IST),False))
        self.assertEqual(latest_completed_session_date(datetime(2026,10,15,3,0,tzinfo=IST)),"2026-10-14")

if __name__=="__main__":
    unittest.main()
