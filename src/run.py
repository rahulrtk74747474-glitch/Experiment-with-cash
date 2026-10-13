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
from src.market import SCAN_URL, fetch_signals, get_nse_quote
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
    if asof_date in state["sessions"]:
        save(state, now, "already_processed", "NSE session already applied; no duplicate orders")
        return 0
    # GitHub Actions can be late; do not count an unverified / closed market day.
    if not manual_latest and (now.weekday() >= 5 or now.time() < time(15, 20) or now.time() > time(18, 0)):
        save(state, now, "outside_market_window",
             "No trades: run outside 15:20–18:00 IST market-data acceptance window")
        return 0
    scanner_confirmed = False
    try:
        symbols = fetch_signals()
        scanner_confirmed = True
        write_scan_status(symbols, status="success", timestamp=now.isoformat(),
            message="Chartink scan verified. Paper trades require valid Yahoo price observations.")
        owned = list(state["positions"])
        targets = list(dict.fromkeys(owned + symbols))
        quotes = {}
        quote_times = {}
        times = []
        for symbol in targets:
            try:
                q = get_nse_quote(symbol, asof_date)
                quotes[symbol] = q["price"]
                quote_times[symbol] = q["quote_time"]
                times.append(q["quote_time"])
            except Exception as e:
                # If a new signal has no quote skip BUY, but existing holdings require
                # a fresh price or the whole session aborts without an exit.
                if symbol in owned:
                    raise
                print("SKIP signal without quote:", symbol, e, flush=True)
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
                if pos["buy_time"] == now.isoformat():
                    pos["buy_quote_time"] = quote_times[symbol]
        for trade in candidate["closed_trades"]:
            if trade["sell_time"] == now.isoformat() and trade["symbol"] in quote_times:
                trade["sell_quote_time"] = quote_times[trade["symbol"]]
        state = candidate
        save(state, now, "success",
             f"Chartink matched {len(symbols)} symbols; verified Yahoo session {asof_date}; " +
             ("manual after-hours snapshot; scan could differ from historic session" if manual_latest else "daily run"))
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
