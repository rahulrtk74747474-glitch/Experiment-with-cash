"""Scheduled run: fetch saved Chartink scan, mark open holdings, apply paper rules.

Run from repository root: python -m src.run
The scan must succeed AND prices must be from the same NSE session.
"""
import json
import os
import sys
from datetime import datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

from src.engine import new_state, process_session, make_report
from src.market import SCAN_URL, fetch_signals, get_nse_quote

IST = ZoneInfo("Asia/Kolkata")
STATE = Path("data/state.json")
REPORT = Path("docs/data/report.json")

def save(state, now, status=None, message=None):
    STATE.parent.mkdir(exist_ok=True, parents=True)
    REPORT.parent.mkdir(exist_ok=True, parents=True)
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report = make_report(state, SCAN_URL, now.isoformat(), run_status=status, message=message)
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"status={report['status']} open={report['summary']['open_count']} "
          f"closed={report['summary']['closed_count']} equity={report['summary']['equity']}")

def main():
    now = datetime.now(IST)
    today = now.date().isoformat()
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else new_state()
    if today in state["sessions"]:
        save(state, now, "already_processed", "NSE session already applied; no duplicate orders")
        return 0
    # GitHub Actions can be late; do not count an unverified / closed market day.
    if now.weekday() >= 5 or now.time() < time(15, 20) or now.time() > time(18, 0):
        save(state, now, "outside_market_window",
             "No trades: run outside 15:20–18:00 IST market-data acceptance window")
        return 0
    try:
        symbols = fetch_signals()
        owned = list(state["positions"])
        targets = list(dict.fromkeys(owned + symbols))
        quotes = {}
        times = []
        for symbol in targets:
            try:
                q = get_nse_quote(symbol, today)
                quotes[symbol] = q["price"]
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
        process_session(state, today, now.isoformat(), symbols, quotes)
        save(state, now, "success",
             f"Chartink matched {len(symbols)} symbols; prices from today's Yahoo minute bars")
        return 0
    except Exception as exc:
        message = f"{type(exc).__name__}: {exc}"
        state["status"] = "error"
        state.setdefault("errors", []).append({"at": now.isoformat(), "message": message})
        state["errors"] = state["errors"][-30:]
        save(state, now, "error", message)
        print(message, file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
