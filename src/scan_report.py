"""Audit independent Chartink scanner results without inventing trades."""
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parent.parent
URL="https://chartink.com/screener/vertex-signal-lue-line"

def write_scan_status(symbols, status, timestamp, message=""):
    values=list(dict.fromkeys(str(x).strip().upper() for x in symbols if str(x).strip()))
    verified=status=="success"
    output={"status":status,"source":URL,"fetched_at":timestamp,"count":len(values),
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
        lines += ["| # | Symbol |","| ---: | --- |"] + ["| "+str(i)+" | "+sym+" |" for i,sym in enumerate(values,1)]
    else:
        lines += ["Verified scanner response contained no symbols."]
    (ROOT/"SCANNER_SYMBOLS.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
