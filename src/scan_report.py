"""Audit independent Chartink scanner results without inventing trades."""
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parent.parent
URL="https://chartink.com/screener/vertex-signal-lue-line"

def write_scan_status(symbols, status, timestamp, message="", rows=None):
    values=list(dict.fromkeys(str(x).strip().upper() for x in symbols if str(x).strip()))
    verified=status=="success"
    rows_by_symbol = {str(r.get("symbol", "")).strip().upper(): r
                      for r in (rows or []) if isinstance(r, dict)}
    details = [{"symbol": sym,
                "name": rows_by_symbol.get(sym, {}).get("name") or sym,
                "close": rows_by_symbol.get(sym, {}).get("close"),
                "change_pct": rows_by_symbol.get(sym, {}).get("change_pct"),
                "volume": rows_by_symbol.get(sym, {}).get("volume")}
               for sym in values]
    output={"status":status,"source":URL,"fetched_at":timestamp,"count":len(values),
            "rows":details,
            "symbols":values,"message":message,"is_verified_live_scan":verified}
    dest=ROOT/"docs/data/latest_scan.json"
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    try:
        displayed=datetime.fromisoformat(timestamp).astimezone(ZoneInfo("Asia/Kolkata")).strftime("%d %b %Y %I:%M %p IST")
    except (ValueError,TypeError):
        displayed="Unknown"
    lines=["# Latest Chartink Scanner Symbols","",
           "[Active Trades](ACTIVE_TRADES.md) · [Trade History](TRADE_HISTORY.md) · [Actions](../../actions)","",
           "**Status:** "+status+"  ","**Last fetch:** "+displayed+"  ",
           "**Symbols:** "+str(len(values))+"  ","**Message:** "+str(message or "—"),""]
    if not verified:
        lines += ["**Not verified:** A failed scan does not mean zero scanner matches.",""]
    elif values:
        lines += ["| # | Symbol | Stock | Scanner close ₹ | % Change | Volume |",
                  "| ---: | --- | --- | ---: | ---: | ---: |"]
        for i, sym in enumerate(values, 1):
            info = rows_by_symbol.get(sym, {})
            clean = lambda v: str(v if v is not None else "—").replace("|", " ").replace("\n", " ")
            lines.append("| " + str(i) + " | " + sym + " | "
                         + clean(info.get("name")) + " | "
                         + clean(info.get("close")) + " | "
                         + clean(info.get("change_pct")) + " | "
                         + clean(info.get("volume")) + " |")
    else:
        lines += ["Verified scanner response contained no symbols."]
    (ROOT/"SCANNER_SYMBOLS.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
