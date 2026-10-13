import unittest
from src.engine import new_state, process_session, make_report

def run(s, day, signals, prices):
    process_session(s, f"2026-10-{day:02d}", f"2026-10-{day:02d}T15:29:00+05:30", signals, prices)

class TradingTests(unittest.TestCase):
    def test_next_day_ignored_day_after_roll(self):
        s = new_state()
        run(s, 5, ["TCS"], {"TCS": 100})
        self.assertEqual(s["positions"]["TCS"]["quantity"], 50)
        run(s, 6, ["TCS"], {"TCS": 110})
        self.assertEqual(s["positions"]["TCS"]["buy_price"], 100)
        run(s, 7, ["TCS"], {"TCS": 120})
        self.assertEqual(len(s["closed_trades"]), 1)
        self.assertEqual(s["closed_trades"][0]["realised_profit"], 1000)
        self.assertEqual(s["positions"]["TCS"]["buy_price"], 120)
        self.assertLessEqual(s["positions"]["TCS"]["invested"], 5000)

    def test_exit_three_sessions_and_no_duplicate_day(self):
        s = new_state()
        run(s, 5, ["INFY"], {"INFY": 100})
        run(s, 6, [], {"INFY": 101})
        run(s, 7, [], {"INFY": 102})
        self.assertIn("INFY", s["positions"])
        run(s, 8, [], {"INFY": 103})
        self.assertNotIn("INFY", s["positions"])
        self.assertEqual(s["closed_trades"][0]["realised_profit"], 150)
        count = len(s["closed_trades"])
        run(s, 8, [], {"INFY": 104})
        self.assertEqual(len(s["closed_trades"]), count)

    def test_drawdown_unrealized_and_cash(self):
        s = new_state()
        run(s, 5, ["SBIN"], {"SBIN": 100})
        run(s, 6, [], {"SBIN": 140})
        run(s, 7, [], {"SBIN": 70})
        p=s["positions"]["SBIN"]
        self.assertAlmostEqual(p["max_drawdown_pct"], -50)
        self.assertEqual(p["max_unrealised_profit"], 2000)
        self.assertEqual(p["min_unrealised_profit"], -1500)
        report=make_report(s, "url", "now")
        self.assertEqual(report["summary"]["unrealised_profit"], -1500)

    def test_insufficient_cash_and_missing_price_safe(self):
        s = new_state()
        symbols=[f"ST{i}" for i in range(25)]
        run(s, 5, symbols, {x: 100 for x in symbols})
        self.assertEqual(sum(p["invested"] for p in s["positions"].values()), 100000)
        self.assertEqual(s["cash"], 0)
        before=list(s["sessions"])
        with self.assertRaises(ValueError):
            run(s, 6, [], {})
        self.assertEqual(s["sessions"], before)

    def test_unavailable_price_does_not_invent_buy(self):
        s=new_state()
        run(s, 5, ["A","B"], {"A": 100})
        self.assertEqual(set(s["positions"]), {"A"})
if __name__=="__main__":
    unittest.main()
