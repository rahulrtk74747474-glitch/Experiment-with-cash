"""Scheduled run: fetch saved Chartink scan, mark open holdings, apply paper rules.

Run from repository root: python -m src.run
The scan must succeed AND prices must be from the same NSE session.
"""
import json
import os
import sys
from copy import deepcopy
from datetime import datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from src.engine import new_state, process_session, make_report
from src.market import SCAN_URL, fetch_signal_details, get_nse_quote
from src.angel_prices import AngelHistoricalPrices, AngelPriceError, configured as angel_configured
from src.report_markdown import write_tables
from src.scan_report import write_scan_status

IST = ZoneInfo("Asia/Kolkata")
STATE = Path("data/state.json")
REPORT = Path("docs/data/report.json")

def latest_completed_session_date(now):
    """Use the last trading weekday after its 15:29 cut-off.

    Exact exchange holidays are validated by availability of dated Yahoo bars.
    Returns no fabricated session if NSE was shut that day.
    """
    day = now.date() if now.weekday() < 5 and now.time() >= time(15, 29) else now.date() - timedelta(days=1)
    while day.weekday() >= 5:
        day -= timedelta(days=1)
    return day.isoformat()

def save(state, now, status=None, message=None):
    STATE.parent.mkdir(exist_ok=True, parents=True)
    REPORT.parent.mkdir(exist_ok=True, parents=True)
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report = make_report(state, SCAN_URL, now.isoformat(), run_status=status, message=message)
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_tables(report)
    print(f"status={report['status']} open={report['summary']['open_count']} "
          f"closed={report['summary']['closed_count']} equity={report['summary']['equity']}")

def main():
    now = datetime.now(IST)
    today = now.date().isoformat()
    manual_latest = os.environ.get("MANUAL_LATEST_SESSION", "").lower() == "true"
    asof_date = latest_completed_session_date(now) if manual_latest else today
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else new_state()
    # Every workflow invocation first runs real-browser scanning, even if the
    # paper-trading session is already processed or we are outside market hours.
    scanner_confirmed = False
    try:
        scanner_rows = fetch_signal_details()
        symbols = [item["symbol"] for item in scanner_rows]
        scanner_prices = {item["symbol"]: float(item["close"])
                          for item in scanner_rows if item.get("close") is not None
                          and float(item["close"]) > 0}
        scanner_confirmed = True
        write_scan_status(symbols, status="success", timestamp=now.isoformat(),
            message="Chartink scan complete; result prices are observed scanner quotes.",
            rows=scanner_rows)
        print(f"BROWSER_SCAN_OK symbols={len(symbols)} source={SCAN_URL}", flush=True)
        if asof_date in state["sessions"]:
            save(state, now, "already_processed", "Browser scanner refreshed; paper session already applied")
            return 0
        # GitHub Actions cron can start late. Do not simulate purchases based on
        # a non-trading day, but retain the freshly scraped symbol list.
        if not manual_latest and (now.weekday() >= 5 or now.time() < time(15, 20) or now.time() > time(18, 0)):
            save(state, now, "outside_market_window",
                 "Browser scanner refreshed; no paper trades outside 15:20–18:00 IST")
            return 0
        owned = list(state["positions"])
        targets = list(dict.fromkeys(owned + symbols))
        quotes = {}
        quote_times = {}
        quote_sources = {}
        times = []
        angel_prices = AngelHistoricalPrices() if angel_configured() else None
        for symbol in targets:
            # The saved scanner itself supplies the current displayed Close for
            # every matched stock. Use this first for responsive paper entries.
            # Quotes for old positions absent from today's scanner use Yahoo.
            if symbol in scanner_prices:
                quotes[symbol] = scanner_prices[symbol]
                quote_times[symbol] = now.isoformat()
                quote_sources[symbol] = "Chartink scanner Close (fetch-time)"
                times.append(now.isoformat())
                continue
            try:
                q = get_nse_quote(symbol, asof_date)
                quotes[symbol] = q["price"]
                quote_times[symbol] = q["quote_time"]
                quote_sources[symbol] = q["source"]
                times.append(q["quote_time"])
            except Exception as yahoo_error:
                # Yahoo 429 or a missing price: retry via authenticated Angel One
                # historical candles, but only if this repository has credentials.
                # No positions are sold from stale or guessed prices.
                if angel_prices is not None:
                    try:
                        q = angel_prices.get_nse_quote(symbol, asof_date)
                        quotes[symbol] = q["price"]
                        quote_times[symbol] = q["quote_time"]
                        quote_sources[symbol] = q["source"]
                        times.append(q["quote_time"])
                        print("ANGEL_PRICE_FALLBACK_OK symbol=" + symbol
                              + " candle=" + q["quote_time"], flush=True)
                        continue
                    except AngelPriceError as angel_error:
                        print("ANGEL_PRICE_FALLBACK_FAILED symbol=" + symbol
                              + " reason=" + str(angel_error), flush=True)
                if symbol in owned:
                    raise RuntimeError(
                        f"No verified {asof_date} price for open holding {symbol}. "
                        f"Yahoo: {type(yahoo_error).__name__}. "
                        f"Angel One: {'failed/unavailable' if angel_prices is not None else 'not configured'}."
                    ) from None
                print("SKIP signal without a verified Yahoo/Angel price:", symbol, flush=True)
        if not targets:
            # Zero signals, zero holdings is valid ONLY after verified Chartink JSON.
            print("Verified Chartink scan returned 0 symbols; no positions")
        elif not times:
            raise RuntimeError("Scan returned symbols but Yahoo returned no fresh prices")
        # Write only after a successfully completed, all-or-nothing state change.
        candidate = deepcopy(state)
        process_session(candidate, asof_date, now.isoformat(), symbols, quotes)
        for symbol, pos in candidate["positions"].items():
            if symbol in quote_times:
                pos["last_quote_time"] = quote_times[symbol]
                pos["last_quote_source"] = quote_sources[symbol]
                if pos["buy_time"] == now.isoformat():
                    pos["buy_quote_time"] = quote_times[symbol]
                    pos["buy_quote_source"] = quote_sources[symbol]
        for trade in candidate["closed_trades"]:
            if trade["sell_time"] == now.isoformat() and trade["symbol"] in quote_times:
                trade["sell_quote_time"] = quote_times[trade["symbol"]]
                trade["sell_quote_source"] = quote_sources[trade["symbol"]]
        state = candidate
        save(state, now, "success",
             f"Chartink matched {len(symbols)} symbols; session label {asof_date}. "
             f"Quotes: {sum(1 for v in quote_sources.values() if v.startswith('Yahoo'))} Yahoo, "
             f"{sum(1 for v in quote_sources.values() if v.startswith('Angel'))} Angel One, "
             f"{sum(1 for v in quote_sources.values() if v.startswith('Chartink'))} Chartink. " +
             ("Manual after-hours scan; scanner close observed at fetch time, not a historical execution."
              if manual_latest else "Daily paper trading. No real orders executed."))
        return 0
    except Exception as exc:
        message = f"{type(exc).__name__}: {exc}"
        if not scanner_confirmed:
            write_scan_status([], status="error", timestamp=now.isoformat(), message=message)
        state["status"] = "error"
        state.setdefault("errors", []).append({"at": now.isoformat(), "message": message})
        state["errors"] = state["errors"][-30:]
        save(state, now, "error", message)
        print(message, file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
