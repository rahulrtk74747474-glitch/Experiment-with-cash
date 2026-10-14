"""Chartink signal scanner + Angel One ONLY daily-close paper trading.

Every invocation scans Chartink and probes exact-date Angel ONE_DAY closing
prices for scanner matches and held symbols. Off-hours code pushes do not
create trades. The paper ledger changes only after all held positions can
be marked from genuine same-session Angel One candles.
"""
import json
import os
import sys
from copy import deepcopy
from datetime import datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from src.engine import new_state, process_session, make_report
from src.market import SCAN_URL, fetch_signal_details
from src.angel_prices import AngelHistoricalPrices, AngelPriceError, configured as angel_configured
from src.report_markdown import write_tables
from src.scan_report import write_scan_status
from src.price_report import write_price_check

IST = ZoneInfo("Asia/Kolkata")
STATE = Path("data/state.json")
REPORT = Path("docs/data/report.json")

def latest_completed_session_date(now):
    """Last possible completed NSE weekday; dated Angel candles verify the session.

    15:45 cutoff allows publication of the full daily candle after 15:30.
    A holiday never counts as a processed session without a same-date bar.
    """
    day = now.date() if now.weekday() < 5 and now.time() >= time(15, 45) else now.date() - timedelta(days=1)
    while day.weekday() >= 5:
        day -= timedelta(days=1)
    return day.isoformat()

def trading_allowed(now, manual):
    return manual or (now.weekday() < 5 and time(15, 45) <= now.time() <= time(18, 0))

def collect_prices(provider, targets, asof_date):
    """Returns successful quotes + errors; every target is attempted independently."""
    found, errors = {}, {}
    for symbol in targets:
        try:
            q = provider.get_daily_close(symbol, asof_date)
            found[symbol] = q
            print("ANGEL_DAILY_CLOSE_OK symbol=" + symbol + " date=" + asof_date
                  + " close=" + str(q["price"]), flush=True)
        except AngelPriceError as exc:
            errors[symbol] = str(exc)
            print("ANGEL_DAILY_CLOSE_FAILED symbol=" + symbol
                  + " reason=" + str(exc), flush=True)
    return found, errors

def save(state, now, status=None, message=None):
    STATE.parent.mkdir(exist_ok=True, parents=True)
    REPORT.parent.mkdir(exist_ok=True, parents=True)
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False)+"\n",encoding="utf-8")
    report=make_report(state, SCAN_URL, now.isoformat(), run_status=status, message=message)
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n",encoding="utf-8")
    write_tables(report)
    print(f"status={report['status']} open={report['summary']['open_count']} "
          f"closed={report['summary']['closed_count']} equity={report['summary']['equity']}",flush=True)

def main():
    now = datetime.now(IST)
    manual = os.getenv("MANUAL_LATEST_SESSION", "").lower() == "true"
    asof_date = latest_completed_session_date(now)
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else new_state()
    scanned = False
    try:
        rows = fetch_signal_details()  # only Chrome scraper, never fallback to HTTP.
        symbols = list(dict.fromkeys(r["symbol"] for r in rows))
        scanned = True
        write_scan_status(symbols, status="success", timestamp=now.isoformat(),
            message="Chartink scan verified; paper entry/exit prices from Angel One NSE ONE_DAY only.",
            rows=rows)
        print(f"BROWSER_SCAN_OK symbols={len(symbols)} source={SCAN_URL}",flush=True)
        targets = list(dict.fromkeys(symbols + list(state["positions"])))
        if not angel_configured():
            write_price_check(now,asof_date,symbols,list(state["positions"]),{},
                {s:"Angel One secrets not configured" for s in targets})
            raise RuntimeError("Angel One credentials not configured; no market prices or simulated trades")
        provider = AngelHistoricalPrices()
        quotes, failures = collect_prices(provider, targets, asof_date)
        write_price_check(now,asof_date,symbols,list(state["positions"]),quotes,failures)

        if asof_date in state["sessions"]:
            save(state,now,"already_processed",
                 f"Scanner refreshed, Angel ONE_DAY checked {len(quotes)}/{len(targets)} stocks; paper session already processed.")
            return 0 if not failures else 1
        if not trading_allowed(now,manual):
            save(state,now,"outside_market_window",
                 f"Read-only Angel ONE_DAY price check: {len(quotes)}/{len(targets)} successful for {asof_date}; "
                 "paper trades not processed outside 15:45–18:00 IST.")
            return 0 if not failures else 1

        missing_owned = [s for s in state["positions"] if s not in quotes]
        if missing_owned:
            raise RuntimeError(
                "No verified Angel ONE_DAY close for held stock(s): "+", ".join(missing_owned)
                +"; refused to change paper portfolio."
            )
        if not quotes:
            raise RuntimeError("Angel One returned no verified daily close; no paper trades")
        # New signals missing a close are skipped by the engine. No guessed prices.
        prices = {sym:q["price"] for sym,q in quotes.items()}
        candidate = deepcopy(state)
        process_session(candidate,asof_date,now.isoformat(),symbols,prices)
        for symbol,position in candidate["positions"].items():
            if symbol in quotes:
                position["last_quote_time"]=quotes[symbol]["quote_time"]
                position["last_quote_source"]=quotes[symbol]["source"]
                if position["buy_time"]==now.isoformat():
                    position["buy_quote_time"]=quotes[symbol]["quote_time"]
                    position["buy_quote_source"]=quotes[symbol]["source"]
        for trade in candidate["closed_trades"]:
            if trade["sell_time"]==now.isoformat() and trade["symbol"] in quotes:
                trade["sell_quote_time"]=quotes[trade["symbol"]]["quote_time"]
                trade["sell_quote_source"]=quotes[trade["symbol"]]["source"]
        state=candidate
        save(state,now,"success",
             f"Chartink symbols={len(symbols)}; verified Angel One daily closes={len(quotes)}/{len(targets)} "
             f"for NSE session {asof_date}; no real orders executed.")
        return 0
    except Exception as exc:
        message=f"{type(exc).__name__}: {exc}"
        if not scanned:
            write_scan_status([],status="error",timestamp=now.isoformat(),message=message)
        state["status"]="error"
        state.setdefault("errors",[]).append({"at":now.isoformat(),"message":message})
        state["errors"]=state["errors"][-30:]
        save(state,now,"error",message)
        print(message,file=sys.stderr,flush=True)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
