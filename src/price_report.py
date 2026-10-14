"""Persistent audit of Angel One daily closes for every Chartink match and held position."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent

def write_price_check(now,session_date,scanner_symbols,held_symbols,quotes,failures):
    target=list(dict.fromkeys(scanner_symbols+held_symbols))
    observations=[]
    for symbol in target:
        q=quotes.get(symbol)
        observations.append({
            "symbol":symbol,
            "scanner_match":symbol in scanner_symbols,
            "held_position":symbol in held_symbols,
            "status":"verified" if q else "missing",
            "daily_close":q["price"] if q else None,
            "source":q["source"] if q else None,
            "candle_timestamp":q["quote_time"] if q else None,
            "error":failures.get(symbol) if not q else None,
        })
    counts={"total":len(target),"verified":len(quotes),"missing":len([x for x in observations if x["status"]=="missing"])}
    status="success" if counts["missing"]==0 else ("partial" if counts["verified"] else "error")
    payload={"status":status,"session_date":session_date,"checked_at":now.isoformat(),
             "source":"Angel One SmartAPI NSE ONE_DAY only","counts":counts,
             "note":"Daily close is a bar value, not an executable price at the candle timestamp.",
             "rows":observations}
    output=ROOT/"docs/data/latest_prices.json"
    output.parent.mkdir(exist_ok=True,parents=True)
    output.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    lines=["# NSE daily close verification — Angel One SmartAPI only","",
          "[Active Trades](ACTIVE_TRADES.md) · [Chartink Scanner](SCANNER_SYMBOLS.md) · "
          "[Workflow](.github/workflows/vertex-paper-trading.yml)","",
          "**NSE session:** "+session_date+"  ",
          "**Checked at (IST):** "+now.strftime("%d %b %Y %I:%M %p")+"  ",
          "**Status:** "+status+"  ",
          "**Verified:** "+str(counts["verified"])+"/"+str(counts["total"])+"  ",
          "","Chartink supplies stock symbols only. Prices below are Angel One daily candle closes, "
          "not an assumption that an order executed at that exact price.","",
          "| Symbol | Scanner? | Held? | Angel daily close ₹ | Candle date/time | Status | Error |",
          "| --- | :---: | :---: | ---: | --- | --- | --- |"]
    for r in observations:
        clean=lambda v:str(v if v is not None else "—").replace("|"," ").replace("\n"," ")
        lines.append("| "+r["symbol"]+" | "+("Yes" if r["scanner_match"] else "No")
          +" | "+("Yes" if r["held_position"] else "No")
          +" | "+clean(r["daily_close"])+" | "+clean(r["candle_timestamp"])
          +" | "+clean(r["status"])+" | "+clean(r["error"])+" |")
    (ROOT/"PRICE_CHECK.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    return payload
