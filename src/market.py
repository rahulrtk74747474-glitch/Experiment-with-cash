"""Chartink screener collector and Yahoo Finance NSE paper-price adapter.

Never infer a zero-result screener from an HTTP error, login wall or missing token.
If Chartink changes its frontend, a visible failure prevents invented trades.
"""
import html
import json
import re
from urllib.parse import unquote
from datetime import datetime, time
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup

IST = ZoneInfo("Asia/Kolkata")
SCAN_URL = "https://chartink.com/screener/vertex-signal-lue-line"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
           "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8"}

def normalise(symbol):
    symbol = str(symbol or "").strip().upper().replace("NSE:", "").removesuffix(".NS")
    return symbol if re.fullmatch(r"[A-Z0-9&_.-]{1,35}", symbol) else ""

def _extract_clause(page):
    soup = BeautifulSoup(page, "html.parser")
    field = soup.select_one('[name="scan_clause"], #scan_clause, [data-scan-clause]')
    if field:
        value = field.get("value") or field.get("data-scan-clause") or field.get_text()
        if value.strip():
            return html.unescape(value)
    # Old Chartink pages embed the saved scan as JSON or a JS string.
    for pattern in (r"""["']scan_clause["']\s*:\s*("(?:\\.|[^"\\])*")""",
                    r"""scan_clause\s*=\s*("(?:\\.|[^"\\])*")""",
                    r"""["']scanClause["']\s*:\s*("(?:\\.|[^"\\])*")"""):
        m = re.search(pattern, page, re.I)
        if m:
            try:
                value = json.loads(m.group(1))
                if "{cash}" in value or "{" in value:
                    return html.unescape(value)
            except (ValueError, TypeError):
                pass
    return ""

def _parse_rendered_table(page_html):
    """Parse the actual Symbol column of a rendered Chartink scan grid.

    Only accept tables where both Symbol and Close headers exist, preventing
    accidental capture of symbols from navigation, saved filters, or examples.
    This handles a browser that renders the scan via a non-legacy API.
    """
    soup = BeautifulSoup(page_html, "html.parser")
    for table in soup.find_all("table"):
        headers = [node.get_text(" ", strip=True).lower().replace("_", " ")
                   for node in table.select("thead tr:first-child th")]
        symbol_index = next((i for i, text in enumerate(headers)
                             if text in ("symbol", "nsecode", "nse code", "ticker")), None)
        if symbol_index is None or not any(h in ("close", "ltp", "last traded price") for h in headers):
            continue
        rows = []
        for tr in table.select("tbody tr"):
            cells = tr.find_all("td", recursive=False)
            if symbol_index >= len(cells):
                continue
            symbol = normalise(cells[symbol_index].get_text(" ", strip=True))
            if symbol and symbol not in rows:
                rows.append(symbol)
        if rows:
            return rows
    return None

def _parse_scan(data):
    if not isinstance(data, dict) or not isinstance(data.get("data"), list):
        raise RuntimeError("Chartink returned no valid screener 'data' array")
    result = []
    for entry in data["data"]:
        sym = normalise(entry.get("nsecode") or entry.get("symbol") or entry.get("ticker"))
        if sym and sym not in result:
            result.append(sym)
    if data["data"] and not result:
        raise RuntimeError("Chartink returned rows but no recognizable NSE symbols")
    return result

def scan_via_http():
    s = requests.Session()
    s.headers.update(HEADERS)
    r = s.get(SCAN_URL, timeout=35)
    r.raise_for_status()
    if "captcha" in r.url.lower() or r.status_code == 403:
        raise RuntimeError("Chartink is blocking automated requests")
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.select_one('meta[name="csrf-token"]')
    clause = _extract_clause(r.text)
    if not clause:
        raise RuntimeError("Saved scan clause not present in HTTP page; browser fallback needed")
    if not token or not token.get("content"):
        raise RuntimeError("Chartink CSRF token unavailable")
    s.headers.update({"x-csrf-token": token["content"],
                      "X-Requested-With": "XMLHttpRequest",
                      "Referer": SCAN_URL})
    xsrf = s.cookies.get("XSRF-TOKEN")
    if xsrf:
        s.headers["X-XSRF-TOKEN"] = unquote(xsrf)
    result = s.post("https://chartink.com/screener/process",
                    data={"scan_clause": clause}, timeout=45)
    result.raise_for_status()
    return _parse_scan(result.json())

def scan_via_browser():
    # Real Chromium fallback for SPA scanner pages and auto-loaded result tables.
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Install playwright and Chromium for Chartink SPA fallback") from exc
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        try:
            page = browser.new_page(user_agent=HEADERS["User-Agent"], timezone_id="Asia/Kolkata")
            def capture(response):
                if "/screener/process" in response.url and response.ok:
                    try:
                        payload = response.json()
                        if isinstance(payload, dict) and isinstance(payload.get("data"), list):
                            results.append(payload)
                    except Exception:
                        pass
            page.on("response", capture)
            page.goto(SCAN_URL, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(5500)
            for name in ("Run Scan", "Scan", "Run"):
                if results:
                    break
                try:
                    btn = page.get_by_role("button", name=name, exact=True)
                    if btn.count() and btn.first.is_visible():
                        btn.first.click(timeout=4500)
                        page.wait_for_timeout(7000)
                except Exception:
                    continue
            if not results:
                rendered = _parse_rendered_table(page.content())
                if rendered is not None:
                    return rendered
                # On older frontend, capture rendered scan clause and submit through session.
                clause = _extract_clause(page.content())
                if clause:
                    token_node = page.locator('meta[name="csrf-token"]')
                    token = token_node.first.get_attribute("content") if token_node.count() else None
                    response = page.request.post("https://chartink.com/screener/process",
                        form={"scan_clause": clause},
                        headers={"x-csrf-token": token or "", "X-Requested-With": "XMLHttpRequest"},
                        timeout=45000)
                    if response.ok:
                        return _parse_scan(response.json())
            if not results:
                raise RuntimeError(
                    "Chartink did not return a valid /screener/process JSON response "
                    "or a rendered Symbol/Close result table (possible block or changed UI)")
            return _parse_scan(results[-1])
        finally:
            browser.close()

def fetch_signals():
    try:
        return scan_via_http()
    except Exception as first:
        try:
            return scan_via_browser()
        except Exception as second:
            raise RuntimeError(f"Chartink unavailable. HTTP: {first}; Chromium: {second}") from second

def get_nse_quote(symbol, expected_date):
    ticker = normalise(symbol)
    if not ticker:
        raise ValueError("Invalid NSE symbol " + str(symbol))
    last_error = None
    for hostname in ("query1.finance.yahoo.com", "query2.finance.yahoo.com"):
        try:
            url = f"https://{hostname}/v8/finance/chart/{ticker}.NS"
            r = requests.get(url, params={"interval": "1m", "range": "5d"}, headers=HEADERS, timeout=25)
            r.raise_for_status()
            result = r.json()["chart"]["result"][0]
            ticks = result.get("timestamp") or []
            close = result["indicators"]["quote"][0].get("close", [])
            candidates = [(datetime.fromtimestamp(t, IST), float(price))
                          for t, price in zip(ticks, close) if price is not None and float(price) > 0]
            today = [(dt, price) for dt, price in candidates
                     if dt.date().isoformat() == expected_date
                     and time(14, 45) <= dt.time() <= time(15, 28, 59)]
            if not today:
                raise RuntimeError(f"No recent pre-3:29 PM {expected_date} Yahoo minute bar for {ticker}")
            dt, price = today[-1]
            return {"price": round(price, 4), "quote_time": dt.isoformat(), "source": "Yahoo Finance NSE 1m"}
        except Exception as exc:
            last_error = exc
    raise RuntimeError(f"Cannot obtain fresh Yahoo price for {ticker}: {last_error}")
