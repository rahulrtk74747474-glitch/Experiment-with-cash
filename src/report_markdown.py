"""Render mobile-accessible tables directly on GitHub (no Pages required)."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
IST = ZoneInfo("Asia/Kolkata")

def _money(x):
    return "₹{:,.2f}".format(float(x or 0))

def _percent(x):
    return "{:+.2f}%".format(float(x or 0))

def _time(x):
    if not x:
        return "—"
    try:
        dt = datetime.fromisoformat(str(x).replace("Z", "+00:00")).astimezone(IST)
        return dt.strftime("%d %b %Y %I:%M %p")
    except ValueError:
        return str(x)

def _safe(x):
    return str(x if x is not None else "—").replace("|", "\\|").replace("\n", " ")

def _table(headers, rows):
    result = ["| " + " | ".join(headers) + " |",
              "| " + " | ".join("---" for _ in headers) + " |"]
    result.extend("| " + " | ".join(_safe(v) for v in row) + " |" for row in rows)
    if not rows:
        result.append("| No trades yet |" + " |" * (len(headers) - 1))
    return "\n".join(result) + "\n"

def write_tables(report):
    summary = report["summary"]
    status = report.get("status", "unknown")
    updated_at = _time(report.get("updated_at"))
    last_success = _time(report.get("last_successful_run"))
    header = (
        "> **PAPER TRADES ONLY — NOT LIVE ORDERS**\n\n"
        f"**System status:** {_safe(status)}  \n"
        f"**Last attempt (IST):** {updated_at}  \n"
        f"**Last successful run (IST):** {last_success}  \n"
        f"**Note:** {_safe(report.get('message', '') or 'Awaiting first verified session')}\n\n"
    )
    stats = (
        f"**Demo capital:** {_money(summary['initial_cash'])} • "
        f"**Cash available:** {_money(summary['cash'])} • "
        f"**Portfolio value:** {_money(summary['equity'])} • "
        f"**Total P&L:** {_money(summary['total_profit'])} "
        f"({_percent(summary['return_pct'])})  \n"
        f"**Realised P&L:** {_money(summary['realised_profit'])} • "
        f"**Unrealised P&L:** {_money(summary['unrealised_profit'])} • "
        f"**Portfolio max drawdown:** {_percent(summary['max_portfolio_drawdown_pct'])}\n\n"
    )
    open_rows = []
    for p in report.get("positions", []):
        open_rows.append([
            p["symbol"], int(p["quantity"]), _time(p["buy_time"]),
            _money(p["buy_price"]), _money(p["current_price"]),
            _money(p["invested"]), _money(p["market_value"]),
            _money(p["unrealised_profit"]), _percent(p["unrealised_pct"]),
            _money(p["max_unrealised_profit"]), _percent(p["max_drawdown_pct"]),
            int(p["sessions_elapsed"])
        ])
    active = (
        "# Active Paper Trades\n\n"
        "[Trade History](TRADE_HISTORY.md) · [Dashboard source](docs/index.html) · "
        "[GitHub Actions](../../actions)\n\n"
        + header + stats
        + f"## Open positions ({len(open_rows)})\n\n"
        + _table(
            ["Symbol", "Qty", "Bought (IST)", "Entry price", "Last price",
             "Invested", "Market value", "Unreal. ₹", "Unreal. %",
             "Max unreal. ₹", "Max DD %", "Sessions held"], open_rows)
        + "\n*The max unrealised return and drawdown use observed daily price samples, "
          "not intraday extremes. Brokerage/slippage excluded.*\n"
    )
    closed_rows = []
    for p in report.get("closed_trades", []):
        closed_rows.append([
            p["symbol"], int(p["quantity"]), _time(p["buy_time"]), _time(p["sell_time"]),
            _money(p["buy_price"]), _money(p["sell_price"]), _money(p["invested"]),
            _money(p["proceeds"]), _money(p["realised_profit"]), _percent(p["return_pct"]),
            _money(p["max_unrealised_profit"]), _percent(p["max_drawdown_pct"]),
            p["exit_reason"]
        ])
    history = (
        "# Closed Paper Trades\n\n"
        "[Active Trades](ACTIVE_TRADES.md) · [Dashboard source](docs/index.html)\n\n"
        + header + stats
        + f"## Completed transactions ({len(closed_rows)})\n\n"
        + _table(
            ["Symbol", "Qty", "Buy time (IST)", "Sell time (IST)", "Buy price",
             "Sell price", "Invested", "Proceeds", "Profit ₹", "Return %",
             "Peak unreal. ₹", "Max DD %", "Reason"], closed_rows)
        + "\n*P&L excludes brokerage, taxes and slippage.*\n"
    )
    (ROOT / "ACTIVE_TRADES.md").write_text(active, encoding="utf-8")
    (ROOT / "TRADE_HISTORY.md").write_text(history, encoding="utf-8")
