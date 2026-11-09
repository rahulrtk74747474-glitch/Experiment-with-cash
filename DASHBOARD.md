# Experiment with Cash — Latest Dashboard

**This dashboard works on GitHub without GitHub Pages.** This is paper trading only.

## Price-update status

- **Angel One observed NSE session:** 2026-11-09
- **Last attempted price check:** 2026-11-10T03:08:32.770722+05:30
- **Prices independently verified:** 9/12
- **Prices missing:** 3
- **Last successfully processed trade session:** 2026-10-14T02:00:59.959625+05:30
- **Trade-processing status:** outside_market_window

**Important:** The verified close is from Angel One. A missing price stays missing; previous trade prices are NOT marked as current. Total equity and P&L below are from the last *fully processed* session and may be stale.

## Open simulated holdings — last verified NSE close

| Stock | Qty | Buy ₹ | Verified Angel close ₹ | Close date | Verified unrealised ₹ | Status |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| DIL | 7692 | ₹0.65 | — | — | — | **Price unavailable — previous quote stale** |
| FCONSUMER | 22727 | ₹0.22 | — | — | — | **Price unavailable — previous quote stale** |
| GENSOL | 516 | ₹9.68 | ₹9.96 | 2026-11-09 | ₹144.48 | Verified |
| MORARJEE | 734 | ₹6.81 | ₹4.30 | 2026-11-09 | ₹-1,842.34 | Verified |
| NAGAFERT | 3267 | ₹1.53 | ₹1.27 | 2026-11-09 | ₹-849.42 | Verified |
| RAJVIR | 959 | ₹5.21 | — | — | — | **Price unavailable — previous quote stale** |
| SETUINFRA | 11363 | ₹0.44 | ₹0.42 | 2026-11-09 | ₹-227.26 | Verified |
| V2RETAIL | 33 | ₹151.45 | ₹168.89 | 2026-11-09 | ₹575.52 | Verified |

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
| ANKITMETAL | Yes | No | ₹1.91 | Verified |
| VIJIFIN | Yes | No | ₹13.05 | Verified |
| NAGAFERT | Yes | Yes | ₹1.27 | Verified |
| LASA | Yes | No | ₹4.22 | Verified |
| SPELS | Yes | No | ₹91.83 | Verified |
| RAJVIR | Yes | Yes | — | Expected exactly one valid NSE ONE_DAY bar for RAJVIR on 2026-11-09; got 0 |
| V2RETAIL | No | Yes | ₹168.89 | Verified |
| SETUINFRA | No | Yes | ₹0.42 | Verified |
| FCONSUMER | No | Yes | — | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | No | Yes | — | No exact NSE equity token found in instrument master for DIL |
| MORARJEE | No | Yes | ₹4.30 | Verified |
| GENSOL | No | Yes | ₹9.96 | Verified |

---
[Verified price audit](PRICE_CHECK.md) · [Latest scanner](SCANNER_SYMBOLS.md) · [Trade history](TRADE_HISTORY.md) · [GitHub Actions](../../actions) · [Graphical dashboard setup](README.md)
