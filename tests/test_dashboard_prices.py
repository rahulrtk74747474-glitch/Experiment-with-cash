"""GitHub dashboard always distinguishes observed prices from stale portfolio state."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from src.dashboard_markdown import render_dashboard, write_dashboard

class TestDashboardPrices(unittest.TestCase):
    def test_partial_price_quotes_do_not_fabricate_prices_or_current_equity(self):
        report={"summary":{"cash":60000,"equity":100000,"total_profit":0,"open_count":2,"closed_count":0},
                "status":"outside_market_window","last_successful_run":"2026-10-13",
                "positions":[{"symbol":"V2RETAIL","buy_price":151.45,"quantity":4},
                             {"symbol":"RAJVIR","buy_price":5.2,"quantity":10}]}
        price={"session_date":"2026-10-14","checked_at":"2026-10-15T04:00:00+05:30",
               "counts":{"total":2,"verified":1,"missing":1},"rows":[
              {"symbol":"V2RETAIL","status":"verified","daily_close":170.64,
               "candle_timestamp":"2026-10-14T00:00:00+05:30",
               "scanner_match":False,"held_position":True},
              {"symbol":"RAJVIR","status":"missing","daily_close":None,"candle_timestamp":None,
               "scanner_match":True,"held_position":True,"error":"No token"}]}
        s=render_dashboard(report,price)
        self.assertIn("₹170.64",s)
        self.assertIn("4",s)
        self.assertIn("Price unavailable — previous quote stale",s)
        self.assertIn("Portfolio equity (NOT current)",s)
        self.assertIn("1/2",s)
    def test_empty_price_data_not_marked_current(self):
        s=render_dashboard({"summary":{},"positions":[]},None)
        self.assertIn("0/0",s)
        self.assertNotIn("Verified Angel close ₹ | 2026",s)
