from __future__ import annotations

import os
import re
from http.cookies import SimpleCookie
from typing import Any

from playwright.sync_api import BrowserContext, Page, TimeoutError as PlaywrightTimeoutError, sync_playwright


DEFAULT_SCAN_URL = "https://chartink.com/screener/vertex-signal-lue-line"
DEFAULT_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0 Safari/537.36"
)


class ChartinkError(RuntimeError):
    pass


def _number(value: str | None, default: float = 0.0) -> float:
    if value is None:
        return default
    cleaned = re.sub(r"[^0-9.\-]", "", value.replace(",", ""))
    try:
        return float(cleaned)
    except (TypeError, ValueError):
        return default


def _normalise_header(value: str) -> str:
    return re.sub(r"[^a-z0-9%]+", " ", value.lower()).strip()


def _add_cookie_header(context: BrowserContext, raw_cookie: str) -> None:
    jar = SimpleCookie()
    try:
        jar.load(raw_cookie)
    except Exception as exc:
        raise ChartinkError("CHARTINK_COOKIE is not a valid Cookie header.") from exc
    cookies = []
    for key, morsel in jar.items():
        cookies.append(
            {
                "name": key,
                "value": morsel.value,
                "domain": ".chartink.com",
                "path": "/",
                "secure": True,
            }
        )
    if cookies:
        context.add_cookies(cookies)


def _first_visible(page: Page, selectors: list[str]):
    for selector in selectors:
        locator = page.locator(selector)
        for i in range(locator.count()):
            item = locator.nth(i)
            try:
                if item.is_visible():
                    return item
            except Exception:
                continue
    return None


def _login(page: Page, user: str, password: str, timeout_ms: int) -> None:
    page.goto("https://chartink.com/login", wait_until="domcontentloaded", timeout=timeout_ms)

    user_input = _first_visible(
        page,
        [
            "input[name='email']",
            "input[type='email']",
            "#email",
            "input[name='username']",
            "input[name='login']",
        ],
    )
    password_input = _first_visible(
        page,
        ["input[name='password']", "input[type='password']", "#password"],
    )
    if user_input is None or password_input is None:
        raise ChartinkError("Could not locate Chartink login fields. The login page may have changed.")

    user_input.fill(user)
    password_input.fill(password)

    submit = _first_visible(
        page,
        [
            "button[type='submit']",
            "input[type='submit']",
            "button:has-text('Sign In')",
            "button:has-text('Login')",
            "button:has-text('Log In')",
        ],
    )
    if submit is None:
        raise ChartinkError("Could not locate the Chartink login button.")

    submit.click()
    try:
        page.wait_for_load_state("domcontentloaded", timeout=timeout_ms)
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(1200)

    # A visible password field after submission is the most reliable generic sign
    # that authentication did not complete (bad credentials, captcha, or UI change).
    password_still_visible = _first_visible(page, ["input[type='password']", "input[name='password']"])
    if "/login" in page.url.lower() and password_still_visible is not None:
        message = "Chartink login did not complete. Check CHARTINK_USER/CHARTINK_PASSWORD."
        body = page.locator("body").inner_text(timeout=5000).lower()
        if "captcha" in body or "verify" in body:
            message += " Chartink may also be requesting browser verification/captcha."
        raise ChartinkError(message)


def _click_run_scan_if_present(page: Page) -> None:
    selectors = [
        "button:has-text('Run Scan')",
        "a:has-text('Run Scan')",
        "button:has-text('Run scan')",
        "input[value='Run Scan']",
        "input[value='Run scan']",
    ]
    button = _first_visible(page, selectors)
    if button is None:
        return
    try:
        button.click(timeout=5000)
    except Exception:
        return


def _find_results_table(page: Page):
    tables = page.locator("table")
    for i in range(tables.count()):
        table = tables.nth(i)
        try:
            headers = [
                _normalise_header(x)
                for x in table.locator("thead th").all_inner_texts()
            ]
        except Exception:
            continue
        joined = " | ".join(headers)
        # Chartink has several tables. The stock-result table consistently exposes
        # Symbol plus market columns such as close / % change / volume.
        if "symbol" in joined and any(token in joined for token in ("close", "volume", "% change", "%_change")):
            return table
    return None


def _scrape_table(page: Page, timeout_ms: int) -> list[dict[str, Any]]:
    deadline_steps = max(1, timeout_ms // 1000)
    table = None
    for _ in range(deadline_steps):
        table = _find_results_table(page)
        if table is not None:
            rows = table.locator("tbody tr")
            if rows.count() > 0:
                break
        body = page.locator("body").inner_text(timeout=5000).lower()
        if "no stocks present" in body or "matched 0 stocks" in body or "no matched stocks" in body:
            return []
        page.wait_for_timeout(1000)

    if table is None:
        raise ChartinkError("Could not find Chartink results table after the scanner page loaded.")

    raw_headers = table.locator("thead th").all_inner_texts()
    headers = [_normalise_header(x) for x in raw_headers]

    def idx(*names: str) -> int | None:
        for name in names:
            name = _normalise_header(name)
            for i, header in enumerate(headers):
                if header == name or name in header:
                    return i
        return None

    symbol_idx = idx("symbol")
    name_idx = idx("stock name", "stock")
    close_idx = idx("close")
    change_idx = idx("% change", "%_change", "change")
    volume_idx = idx("volume")

    if symbol_idx is None:
        raise ChartinkError(f"Chartink result table did not contain a Symbol column. Headers: {raw_headers}")

    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    rows = table.locator("tbody tr")
    for row_no in range(rows.count()):
        cells = [text.strip() for text in rows.nth(row_no).locator("td").all_inner_texts()]
        if not cells or symbol_idx >= len(cells):
            continue
        symbol = cells[symbol_idx].strip().upper()
        if not symbol or symbol in seen:
            continue
        if not re.fullmatch(r"[A-Z0-9&._\-]+", symbol):
            continue
        seen.add(symbol)

        name = symbol
        if name_idx is not None and name_idx < len(cells) and cells[name_idx]:
            name = cells[name_idx]
        close = _number(cells[close_idx]) if close_idx is not None and close_idx < len(cells) else 0.0
        change_pct = _number(cells[change_idx]) if change_idx is not None and change_idx < len(cells) else None
        volume = _number(cells[volume_idx]) if volume_idx is not None and volume_idx < len(cells) else None

        raw = {raw_headers[i].strip() or f"column_{i}": value for i, value in enumerate(cells) if i < len(raw_headers)}
        out.append(
            {
                "symbol": symbol,
                "name": name,
                "close": close,
                "change_pct": change_pct,
                "volume": volume,
                "raw": raw,
            }
        )
    return out


def fetch_chartink_signals(
    scan_url: str | None = None,
    raw_cookie: str | None = None,
    timeout: int = 45,
) -> list[dict[str, Any]]:
    """Scrape a saved Chartink scanner with a real headless Chromium browser.

    The browser always tries the scanner directly first.
    If Chartink requires authentication, it then uses:
      1. CHARTINK_COOKIE, when supplied.
      2. CHARTINK_USER + CHARTINK_PASSWORD.
    Public scanners therefore need no credentials.

    This implementation intentionally does not use Chartink's /screener/process API
    or require a scan_clause.
    """
    scan_url = (scan_url or os.getenv("CHARTINK_SCAN_URL") or DEFAULT_SCAN_URL).strip()
    raw_cookie = raw_cookie or os.getenv("CHARTINK_COOKIE", "")
    user = (os.getenv("CHARTINK_USER") or os.getenv("CHARTINK_EMAIL") or "").strip()
    password = os.getenv("CHARTINK_PASSWORD", "")
    timeout_ms = int(timeout * 1000)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-dev-shm-usage", "--no-sandbox"],
        )
        context = browser.new_context(
            user_agent=DEFAULT_UA,
            viewport={"width": 1440, "height": 1200},
            locale="en-IN",
            timezone_id="Asia/Kolkata",
        )
        context.set_default_timeout(timeout_ms)

        try:
            # Prefer direct browser scraping first. Only authenticate if Chartink
            # actually redirects this scanner to login. This lets public scanners
            # work even when old login secrets are present in GitHub.
            if raw_cookie:
                _add_cookie_header(context, raw_cookie)

            page = context.new_page()
            page.goto(scan_url, wait_until="domcontentloaded", timeout=timeout_ms)
            page.wait_for_timeout(1500)

            if "/login" in page.url.lower() or _first_visible(page, ["input[type='password']"]) is not None:
                if not (user and password):
                    raise ChartinkError(
                        "This Chartink scanner requires login. Add CHARTINK_USER and "
                        "CHARTINK_PASSWORD as GitHub Actions secrets, or add CHARTINK_COOKIE."
                    )
                _login(page, user, password, timeout_ms)
                page.goto(scan_url, wait_until="domcontentloaded", timeout=timeout_ms)
                page.wait_for_timeout(1500)

            _click_run_scan_if_present(page)
            page.wait_for_timeout(1500)
            return _scrape_table(page, timeout_ms)
        finally:
            context.close()
            browser.close()
