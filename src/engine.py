"""Deterministic, long-only paper-trading engine. No network calls here."""
from __future__ import annotations

import math
from datetime import datetime

INITIAL_CASH = 100_000.0
MAX_PER_SYMBOL = 5_000.0
HOLD_SESSIONS = 3  # T+3 successfully observed NSE trading sessions
REBUY_GAP = 2      # T+1 ignore, T+2 or later qualifies

def new_state():
    return {"version": 1, "initial_cash": INITIAL_CASH, "cash": INITIAL_CASH,
            "positions": {}, "closed_trades": [], "events": [], "equity_curve": [],
            "sessions": [], "next_trade_id": 1, "last_run": None, "status": "not_started", "errors": []}

def round2(x):
    return round(float(x) + 1e-10, 2)

def _mark(position, price):
    """Track per-trade observed peak-to-trough MDD and best unrealised profits."""
    price = float(price)
    if price <= 0:
        return
    position["last_price"] = price
    position["peak_price"] = max(position["peak_price"], price)
    position["trough_price"] = min(position["trough_price"], price)
    dd = (price / position["peak_price"] - 1) * 100
    position["max_drawdown_pct"] = min(position["max_drawdown_pct"], round2(dd))
    unreal = (price - position["buy_price"]) * position["quantity"]
    position["max_unrealised_profit"] = max(position["max_unrealised_profit"], round2(unreal))
    position["min_unrealised_profit"] = min(position["min_unrealised_profit"], round2(unreal))
    position["max_unrealised_pct"] = max(position["max_unrealised_pct"],
                                          round2((price / position["buy_price"] - 1) * 100))

def _sell(state, symbol, price, asof, reason):
    p = state["positions"].pop(symbol)
    invested = round2(p["buy_price"] * p["quantity"])
    proceeds = round2(price * p["quantity"])
    profit = round2(proceeds - invested)
    trade = {**p, "sell_time": asof, "sell_price": round2(price),
             "exit_reason": reason, "proceeds": proceeds,
             "realised_profit": profit, "return_pct": round2(profit / invested * 100)}
    state["closed_trades"].append(trade)
    state["cash"] = round2(state["cash"] + proceeds)
    state["events"].append({"date": asof, "symbol": symbol, "action": "SELL",
                            "quantity": p["quantity"], "price": round2(price),
                            "profit": profit, "reason": reason})

def _buy(state, symbol, price, asof, session_index):
    budget = min(MAX_PER_SYMBOL, state["cash"])
    qty = math.floor(round(budget / price, 10))
    if qty < 1:
        state["events"].append({"date": asof, "symbol": symbol, "action": "SKIPPED",
                                "reason": "Insufficient cash or price exceeds ₹5,000"})
        return
    invested = round2(qty * price)
    if invested > budget + 0.001:
        qty -= 1
        invested = round2(qty * price)
    if qty < 1:
        return
    state["cash"] = round2(state["cash"] - invested)
    trade_id = state["next_trade_id"]
    state["next_trade_id"] += 1
    state["positions"][symbol] = {
        "trade_id": trade_id, "symbol": symbol, "buy_time": asof,
        "buy_price": round2(price), "quantity": qty, "invested": invested,
        "last_price": round2(price), "peak_price": round2(price),
        "trough_price": round2(price), "max_drawdown_pct": 0.0,
        "max_unrealised_profit": 0.0, "min_unrealised_profit": 0.0,
        "max_unrealised_pct": 0.0, "buy_session_index": session_index}
    state["events"].append({"date": asof, "symbol": symbol, "action": "BUY",
                            "quantity": qty, "price": round2(price), "invested": invested})

def process_session(state, date, asof, symbols, quotes):
    """Process one *successful* trading session exactly once.

    symbols: ordered Chartink symbols. quotes: {NSE_symbol: positive price}.
    Fail CLOSED when an existing position lacks a quote: no guessed sale.
    Rebuy means sell and repurchase (new trade) on T+2 onward; never pyramid
    beyond ₹5,000 per symbol. Expiry is T+3 without a qualifying repeat.
    """
    if date in state["sessions"]:
        return state  # idempotent even if rerun by GitHub Actions
    symbols = list(dict.fromkeys(s.strip().upper().removesuffix(".NS") for s in symbols if s.strip()))
    quote = {str(k).upper().removesuffix(".NS"): float(v)
             for k, v in quotes.items() if v is not None and float(v) > 0}
    missing_owned = [sym for sym in state["positions"] if sym not in quote]
    if missing_owned:
        raise ValueError("Prices missing for open holdings; skipped safely: " + ", ".join(missing_owned))
    state["sessions"].append(date)
    index = len(state["sessions"]) - 1
    for sym, pos in state["positions"].items():
        _mark(pos, quote[sym])
    # Close positions that did not receive a timely qualifying repeat.
    for sym, pos in list(state["positions"].items()):
        age = index - pos["buy_session_index"]
        if age >= HOLD_SESSIONS and (sym not in symbols or sym not in quote):
            _sell(state, sym, quote[sym], asof, "3_SESSIONS_NO_REBUY")
    # The exact Chartink order controls priority when all ₹100k is invested.
    for sym in symbols:
        if sym not in quote:
            state["events"].append({"date": asof, "symbol": sym, "action": "SKIPPED",
                                    "reason": "No valid market quote"})
            continue
        price = quote[sym]
        if sym in state["positions"]:
            age = index - state["positions"][sym]["buy_session_index"]
            if age < REBUY_GAP:
                state["events"].append({"date": asof, "symbol": sym, "action": "IGNORED",
                                        "reason": "Consecutive-session signal ignored"})
                continue
            # Sell + fresh ₹5k-capped buy resets three-session clock.
            _sell(state, sym, price, asof, "QUALIFIED_REBUY")
        _buy(state, sym, price, asof, index)
    total_invested = sum(p["invested"] for p in state["positions"].values())
    market_value = sum(p["quantity"] * p["last_price"] for p in state["positions"].values())
    equity = round2(state["cash"] + market_value)
    previous_peak = max((r["equity"] for r in state["equity_curve"]), default=state["initial_cash"])
    peak = max(previous_peak, state["initial_cash"], equity)
    drawdown = round2((equity / peak - 1) * 100)
    previous_dd = min((r["drawdown_pct"] for r in state["equity_curve"]), default=0.0)
    state["equity_curve"].append({"date": date, "equity": equity,
                                  "cash": state["cash"], "invested_cost": round2(total_invested),
                                  "drawdown_pct": drawdown,
                                  "max_drawdown_pct": min(previous_dd, drawdown)})
    state["last_run"] = asof
    state["status"] = "success"
    state["errors"] = []
    return state

def make_report(state, source_url, updated_at, run_status=None, message=None):
    positions = []
    for p in state["positions"].values():
        current_value = round2(p["quantity"] * p["last_price"])
        pnl = round2(current_value - p["invested"])
        positions.append({**p, "current_price": p["last_price"], "market_value": current_value,
                          "unrealised_profit": pnl,
                          "unrealised_pct": round2(pnl / p["invested"] * 100),
                          "sessions_elapsed": max(0, len(state["sessions"]) - 1 - p["buy_session_index"])})
    realised = round2(sum(p["realised_profit"] for p in state["closed_trades"]))
    unrealised = round2(sum(p["unrealised_profit"] for p in positions))
    equity = round2(state["cash"] + sum(p["market_value"] for p in positions))
    closed = state["closed_trades"]
    wins = sum(1 for t in closed if t["realised_profit"] > 0)
    return {
        "source": source_url, "updated_at": updated_at,
        "last_successful_run": state["last_run"], "status": run_status or state["status"],
        "message": message or "", "sessions": len(state["sessions"]),
        "summary": {"initial_cash": state["initial_cash"], "cash": state["cash"],
                    "equity": equity, "invested_cost": round2(sum(p["invested"] for p in positions)),
                    "market_value": round2(sum(p["market_value"] for p in positions)),
                    "total_profit": round2(equity - state["initial_cash"]),
                    "return_pct": round2((equity / state["initial_cash"] - 1) * 100),
                    "realised_profit": realised, "unrealised_profit": unrealised,
                    "open_count": len(positions), "closed_count": len(closed),
                    "win_rate_pct": round2(wins / len(closed) * 100) if closed else 0,
                    "max_portfolio_drawdown_pct":
                        min((x["drawdown_pct"] for x in state["equity_curve"]), default=0.0)},
        "positions": sorted(positions, key=lambda p: p["symbol"]),
        "closed_trades": list(reversed(closed)),
        "equity_curve": state["equity_curve"],
        "events": list(reversed(state["events"][-150:])),
    }
