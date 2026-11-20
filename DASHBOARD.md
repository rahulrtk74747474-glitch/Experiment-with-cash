# Experiment with Cash — Latest Dashboard

**This dashboard works on GitHub without GitHub Pages.** This is paper trading only.

## Price-update status

- **Angel One observed NSE session:** 2026-11-20
- **Last attempted price check:** 2026-11-21T00:10:30.273478+05:30
- **Prices independently verified:** 9/15
- **Prices missing:** 6
- **Last successfully processed trade session:** 2026-10-14T02:00:59.959625+05:30
- **Trade-processing status:** outside_market_window

**Important:** The verified close is from Angel One. A missing price stays missing; previous trade prices are NOT marked as current. Total equity and P&L below are from the last *fully processed* session and may be stale.

## Open simulated holdings — last verified NSE close

| Stock | Qty | Buy ₹ | Verified Angel close ₹ | Close date | Verified unrealised ₹ | Status |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| DIL | 7692 | ₹0.65 | — | — | — | **Price unavailable — previous quote stale** |
| FCONSUMER | 22727 | ₹0.22 | — | — | — | **Price unavailable — previous quote stale** |
| GENSOL | 516 | ₹9.68 | ₹9.53 | 2026-11-20 | ₹-77.40 | Verified |
| MORARJEE | 734 | ₹6.81 | ₹6.12 | 2026-11-20 | ₹-506.46 | Verified |
| NAGAFERT | 3267 | ₹1.53 | — | — | — | **Price unavailable — previous quote stale** |
| RAJVIR | 959 | ₹5.21 | — | — | — | **Price unavailable — previous quote stale** |
| SETUINFRA | 11363 | ₹0.44 | — | — | — | **Price unavailable — previous quote stale** |
| V2RETAIL | 33 | ₹151.45 | ₹162.06 | 2026-11-20 | ₹350.13 | Verified |

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
| ICDSLTD | Yes | No | ₹43.34 | Verified |
| PARSVNATH | Yes | No | ₹2.43 | Verified |
| ANKITMETAL | Yes | No | ₹1.67 | Verified |
| GANGAFORGE | Yes | No | ₹1.04 | Verified |
| VALIANTLAB | Yes | No | ₹94.91 | Verified |
| LASA | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for LASA on 2026-11-20; got 0 |
| PASHUPATI | Yes | No | ₹27.18 | Verified |
| RAJVIR | Yes | Yes | — | No exact NSE equity token found in instrument master for RAJVIR |
| V2RETAIL | No | Yes | ₹162.06 | Verified |
| SETUINFRA | No | Yes | — | Expected exactly one valid NSE ONE_DAY bar for SETUINFRA on 2026-11-20; got 0 |
| FCONSUMER | No | Yes | — | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | No | Yes | — | Expected exactly one valid NSE ONE_DAY bar for DIL on 2026-11-20; got 0 |
| MORARJEE | No | Yes | ₹6.12 | Verified |
| GENSOL | No | Yes | ₹9.53 | Verified |
| NAGAFERT | No | Yes | — | No exact NSE equity token found in instrument master for NAGAFERT |

---
[Verified price audit](PRICE_CHECK.md) · [Latest scanner](SCANNER_SYMBOLS.md) · [Trade history](TRADE_HISTORY.md) · [GitHub Actions](../../actions) · [Graphical dashboard setup](README.md)
