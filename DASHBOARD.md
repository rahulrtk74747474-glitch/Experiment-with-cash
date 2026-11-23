# Experiment with Cash — Latest Dashboard

**This dashboard works on GitHub without GitHub Pages.** This is paper trading only.

## Price-update status

- **Angel One observed NSE session:** 2026-11-23
- **Last attempted price check:** 2026-11-24T03:44:15.166013+05:30
- **Prices independently verified:** 11/14
- **Prices missing:** 3
- **Last successfully processed trade session:** 2026-10-14T02:00:59.959625+05:30
- **Trade-processing status:** outside_market_window

**Important:** The verified close is from Angel One. A missing price stays missing; previous trade prices are NOT marked as current. Total equity and P&L below are from the last *fully processed* session and may be stale.

## Open simulated holdings — last verified NSE close

| Stock | Qty | Buy ₹ | Verified Angel close ₹ | Close date | Verified unrealised ₹ | Status |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| DIL | 7692 | ₹0.65 | — | — | — | **Price unavailable — previous quote stale** |
| FCONSUMER | 22727 | ₹0.22 | — | — | — | **Price unavailable — previous quote stale** |
| GENSOL | 516 | ₹9.68 | ₹9.06 | 2026-11-23 | ₹-319.92 | Verified |
| MORARJEE | 734 | ₹6.81 | ₹5.83 | 2026-11-23 | ₹-719.32 | Verified |
| NAGAFERT | 3267 | ₹1.53 | ₹1.39 | 2026-11-23 | ₹-457.38 | Verified |
| RAJVIR | 959 | ₹5.21 | — | — | — | **Price unavailable — previous quote stale** |
| SETUINFRA | 11363 | ₹0.44 | ₹0.41 | 2026-11-23 | ₹-340.89 | Verified |
| V2RETAIL | 33 | ₹151.45 | ₹151.61 | 2026-11-23 | ₹5.28 | Verified |

## Previous fully processed ledger (historical)

| Metric | Historical value |
| --- | ---: |
| Cash | ₹60,014.37 |
| Portfolio equity (NOT current) | ₹100,000.00 |
| Last processed P&L | ₹0.00 |
| Open trades | 8 |
| Closed trades | 0 |

## All scanned symbols and Angel One price checks

| Symbol | Scanner | Existing holding | Angel close ₹ | Status / reason |
| --- | :---: | :---: | ---: | --- |
| SILVER001 | Yes | No | ₹15.55 | Verified |
| CRISIL | Yes | No | ₹4,034.80 | Verified |
| PARSVNATH | Yes | No | ₹2.39 | Verified |
| ICDSLTD | Yes | No | ₹42.48 | Verified |
| VALIANTLAB | Yes | No | ₹93.02 | Verified |
| LASA | Yes | No | ₹3.81 | Verified |
| RAJVIR | Yes | Yes | — | Expected exactly one valid NSE ONE_DAY bar for RAJVIR on 2026-11-23; got 0 |
| V2RETAIL | No | Yes | ₹151.61 | Verified |
| SETUINFRA | No | Yes | ₹0.41 | Verified |
| FCONSUMER | No | Yes | — | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | No | Yes | — | No exact NSE equity token found in instrument master for DIL |
| MORARJEE | No | Yes | ₹5.83 | Verified |
| GENSOL | No | Yes | ₹9.06 | Verified |
| NAGAFERT | No | Yes | ₹1.39 | Verified |

---
[Verified price audit](PRICE_CHECK.md) · [Latest scanner](SCANNER_SYMBOLS.md) · [Trade history](TRADE_HISTORY.md) · [GitHub Actions](../../actions) · [Graphical dashboard setup](README.md)
