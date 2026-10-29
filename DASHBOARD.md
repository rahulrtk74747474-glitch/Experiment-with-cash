# Experiment with Cash — Latest Dashboard

**This dashboard works on GitHub without GitHub Pages.** This is paper trading only.

## Price-update status

- **Angel One observed NSE session:** 2026-10-29
- **Last attempted price check:** 2026-10-29T22:29:22.910852+05:30
- **Prices independently verified:** 12/19
- **Prices missing:** 7
- **Last successfully processed trade session:** 2026-10-14T02:00:59.959625+05:30
- **Trade-processing status:** outside_market_window

**Important:** The verified close is from Angel One. A missing price stays missing; previous trade prices are NOT marked as current. Total equity and P&L below are from the last *fully processed* session and may be stale.

## Open simulated holdings — last verified NSE close

| Stock | Qty | Buy ₹ | Verified Angel close ₹ | Close date | Verified unrealised ₹ | Status |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| DIL | 7692 | ₹0.65 | — | — | — | **Price unavailable — previous quote stale** |
| FCONSUMER | 22727 | ₹0.22 | — | — | — | **Price unavailable — previous quote stale** |
| GENSOL | 516 | ₹9.68 | ₹10.24 | 2026-10-29 | ₹288.96 | Verified |
| MORARJEE | 734 | ₹6.81 | ₹4.31 | 2026-10-29 | ₹-1,835.00 | Verified |
| NAGAFERT | 3267 | ₹1.53 | — | — | — | **Price unavailable — previous quote stale** |
| RAJVIR | 959 | ₹5.21 | — | — | — | **Price unavailable — previous quote stale** |
| SETUINFRA | 11363 | ₹0.44 | — | — | — | **Price unavailable — previous quote stale** |
| V2RETAIL | 33 | ₹151.45 | ₹154.71 | 2026-10-29 | ₹107.58 | Verified |

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
| JSWDULUX | Yes | No | ₹276.20 | Verified |
| DECCANCE | Yes | No | ₹469.00 | Verified |
| BLUECHIP | Yes | No | ₹1.56 | Verified |
| DELPHIFX | Yes | No | ₹5.67 | Verified |
| VELJAN | Yes | No | ₹2,091.50 | Verified |
| MBECL | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for MBECL on 2026-10-29; got 0 |
| SETUINFRA | Yes | Yes | — | Expected exactly one valid NSE ONE_DAY bar for SETUINFRA on 2026-10-29; got 0 |
| ASTEC | Yes | No | ₹581.05 | Verified |
| FCONSUMER | Yes | Yes | — | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | Yes | Yes | — | Expected exactly one valid NSE ONE_DAY bar for DIL on 2026-10-29; got 0 |
| GATEWAY | Yes | No | ₹43.84 | Verified |
| NAGAFERT | Yes | Yes | — | No exact NSE equity token found in instrument master for NAGAFERT |
| LASA | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for LASA on 2026-10-29; got 0 |
| BNAGROCHEM | Yes | No | ₹111.15 | Verified |
| RAJVIR | Yes | Yes | — | No exact NSE equity token found in instrument master for RAJVIR |
| GRADIENTE | Yes | No | ₹1.71 | Verified |
| V2RETAIL | No | Yes | ₹154.71 | Verified |
| MORARJEE | No | Yes | ₹4.31 | Verified |
| GENSOL | No | Yes | ₹10.24 | Verified |

---
[Verified price audit](PRICE_CHECK.md) · [Latest scanner](SCANNER_SYMBOLS.md) · [Trade history](TRADE_HISTORY.md) · [GitHub Actions](../../actions) · [Graphical dashboard setup](README.md)
