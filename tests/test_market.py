import unittest
from unittest.mock import Mock, patch
from src.market import _parse_rendered_table, _parse_scan, scan_via_http

EXPECTED = ["V2RETAIL", "RAJVIR", "SETUINFRA", "FCONSUMER"]

class TestScanner(unittest.TestCase):
    def test_screenshot_shaped_table(self):
        names = ["V2 Retail Limited", "Rajvir Industries Limited", "Setubandhan Infrastructure Ltd", "Future Consumer Limited"]
        prices = [151.45, 5.21, 0.44, 0.22]
        html = '<table><thead><tr><th>Sr.</th><th>Stock Name</th><th>Symbol</th><th>Close</th><th>%_change</th><th>Volume</th></tr></thead><tbody>'
        for i, (name, symbol, price) in enumerate(zip(names, EXPECTED, prices), 1):
            html += f"<tr><td>{i}</td><td>{name}</td><td>{symbol}</td><td>{price}</td><td>-2%</td><td>100</td></tr>"
        html += '</tbody></table>'
        self.assertEqual(_parse_rendered_table(html), EXPECTED)

    def test_ignore_unrelated_symbols(self):
        html = '<div>NSE:RELIANCE</div><table><thead><tr><th>Symbol</th><th>Volume</th></tr></thead><tbody><tr><td>FAKE</td><td>11</td></tr></tbody></table>'
        self.assertIsNone(_parse_rendered_table(html))

    def test_json_scan(self):
        self.assertEqual(_parse_scan({"data": [{"nsecode": s} for s in EXPECTED]}), EXPECTED)

    def test_http_uses_requests_data_keyword(self):
        page = '<html><meta name="csrf-token" content="token"><input name="scan_clause" value="( {cash} ( latest close &gt; 0 ) )"></html>'
        fake = Mock()
        fake.headers = {}
        fake.cookies.get.return_value = None
        fake.get.return_value = Mock(text=page, url="https://chartink.com/screener/vertex-signal-lue-line")
        fake.post.return_value.json.return_value = {"data": [{"nsecode": s} for s in EXPECTED]}
        with patch("src.market.requests.Session", return_value=fake):
            self.assertEqual(scan_via_http(), EXPECTED)
        kwargs = fake.post.call_args.kwargs
        self.assertEqual(kwargs["data"]["scan_clause"], "( {cash} ( latest close > 0 ) )")
        self.assertNotIn("form", kwargs)

    def test_failed_json_cannot_masquerade_as_zero_matches(self):
        with self.assertRaises(RuntimeError):
            _parse_scan({"error": "blocked"})


    def test_browser_adapter_returns_all_four_chartink_rows(self):
        from src.market import fetch_signal_details
        fixture = [
            {"symbol": "V2RETAIL", "name": "V2 Retail Limited", "close": 151.45,
             "change_pct": -1.41, "volume": 1129342},
            {"symbol": "RAJVIR", "name": "Rajvir Industries Limited", "close": 5.21,
             "change_pct": -2.07, "volume": 16},
            {"symbol": "SETUINFRA", "name": "Setubandhan Infrastructure Ltd",
             "close": 0.44, "change_pct": -2.22, "volume": 4384},
            {"symbol": "FCONSUMER", "name": "Future Consumer Limited",
             "close": 0.22, "change_pct": -4.35, "volume": 36892674},
        ]
        with patch("src.chartink_browser.fetch_chartink_signals", return_value=fixture):
            rows = fetch_signal_details()
        self.assertEqual([x["symbol"] for x in rows], EXPECTED)
        self.assertEqual([x["close"] for x in rows], [151.45, 5.21, .44, .22])

    def test_scanner_rows_do_not_depend_on_yahoo(self):
        from src.engine import new_state, process_session
        portfolio = new_state()
        snapshot = dict(zip(EXPECTED, [151.45, 5.21, 0.44, 0.22]))
        process_session(portfolio, "2026-10-13", "2026-10-14T01:00:00+05:30",
                        EXPECTED, snapshot)
        self.assertEqual(set(portfolio["positions"]), set(EXPECTED))
        self.assertEqual(portfolio["cash"], 100000 - sum(
            p["invested"] for p in portfolio["positions"].values()))
        self.assertTrue(all(p["invested"] <= 5000 for p in portfolio["positions"].values()))

if __name__ == "__main__":
    unittest.main()
