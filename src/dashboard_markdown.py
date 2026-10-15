"""GitHub-native dashboard with independently verified Angel daily close prices.

This deliberately DOES NOT change trading state or combine stale/missing
prices into a fictitious current portfolio valuation.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def render_dashboard(report: dict, price: dict | None) -> str:
    summary=report.get("summary") or {}
    positions=report.get("positions") or []
    valid=(price or {}).get("rows") or []
    by_symbol={x.get("symbol"):x for x in valid if isinstance(x,dict)}
    date=(price or {}).get("session_date") or "not yet verified"
    counts=(price or {}).get("counts") or {}
    def rupee(x):
        return "₹"+format(float(x),",.2f")
    def safe(x):
        return str(x or "—").replace("|","/").replace("\n"," ").replace("\r"," ")
    lines=["# Experiment with Cash — Latest Dashboard","",
      "**This dashboard works on GitHub without GitHub Pages.** This is paper trading only.",
      "",
      "## Price-update status","",
      "- **Angel One observed NSE session:** "+date,
      "- **Last attempted price check:** "+safe((price or {}).get("checked_at")),
      "- **Prices independently verified:** "+str(counts.get("verified",0))+"/"+str(counts.get("total",0)),
      "- **Prices missing:** "+str(counts.get("missing",0)),
      "- **Last successfully processed trade session:** "+safe(report.get("last_successful_run")),
      "- **Trade-processing status:** "+safe(report.get("status")),
      "",
      "**Important:** The verified close is from Angel One. A missing price stays missing; "
      "previous trade prices are NOT marked as current. Total equity and P&L below "
      "are from the last *fully processed* session and may be stale.",
      "",
      "## Open simulated holdings — last verified NSE close","",
      "| Stock | Qty | Buy ₹ | Verified Angel close ₹ | Close date | Verified unrealised ₹ | Status |",
      "| --- | ---: | ---: | ---: | --- | ---: | --- |"]
    for p in positions:
        sym=p["symbol"]
        q=by_symbol.get(sym,{})
        verified=(q.get("status")=="verified" and q.get("daily_close") is not None
                  and str(q.get("candle_timestamp","")).startswith(date))
        close=float(q["daily_close"]) if verified else None
        pnl=(close-float(p["buy_price"]))*int(p["quantity"]) if verified else None
        lines.append("| "+safe(sym)+" | "+str(p["quantity"])+" | "+rupee(p["buy_price"])
            +" | "+(rupee(close) if verified else "—")
            +" | "+(date if verified else "—")
            +" | "+(rupee(pnl) if verified else "—")
            +" | "+("Verified" if verified else "**Price unavailable — previous quote stale**")+" |")
    if not positions:lines.append("| — | — | — | — | — | — | No positions yet |")
    lines.extend(["","## Previous fully processed ledger (historical)","",
        "| Metric | Historical value |","| --- | ---: |",
        "| Cash | "+rupee(summary.get("cash",0))+" |",
        "| Portfolio equity (NOT current) | "+rupee(summary.get("equity",0))+" |",
        "| Last processed P&L | "+rupee(summary.get("total_profit",0))+" |",
        "| Open trades | "+str(summary.get("open_count",0))+" |",
        "| Closed trades | "+str(summary.get("closed_count",0))+" |",
        "",
        "## All scanned symbols and Angel One price checks","",
        "| Symbol | Scanner | Existing holding | Angel close ₹ | Status / reason |",
        "| --- | :---: | :---: | ---: | --- |"])
    for q in valid:
        verified=q.get("status")=="verified" and q.get("daily_close") is not None
        lines.append("| "+safe(q.get("symbol"))+" | "+("Yes" if q.get("scanner_match") else "No")
          +" | "+("Yes" if q.get("held_position") else "No")
          +" | "+(rupee(q["daily_close"]) if verified else "—")
          +" | "+("Verified" if verified else safe(q.get("error") or "Not available"))+" |")
    lines.extend(["","---","[Verified price audit](PRICE_CHECK.md) · "
      "[Latest scanner](SCANNER_SYMBOLS.md) · "
      "[Trade history](TRADE_HISTORY.md) · "
      "[GitHub Actions](../../actions) · "
      "[Graphical dashboard setup](README.md)",""])
    return "\n".join(lines)

def write_dashboard(report:dict,price_file:Path=ROOT/"docs/data/latest_prices.json"):
    price=None
    if price_file.exists():
        try:
            price=json.loads(price_file.read_text(encoding="utf-8"))
        except (ValueError,OSError):
            pass
    (ROOT/"DASHBOARD.md").write_text(render_dashboard(report,price),encoding="utf-8")
