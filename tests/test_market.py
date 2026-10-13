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

if __name__ == "__main__":
    unittest.main()
