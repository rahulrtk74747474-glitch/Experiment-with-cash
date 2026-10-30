# Experiment with Cash — Latest Dashboard

**This dashboard works on GitHub without GitHub Pages.** This is paper trading only.

## Price-update status

- **Angel One observed NSE session:** 2026-10-30
- **Last attempted price check:** 2026-10-30T22:19:55.768411+05:30
- **Prices independently verified:** 15/22
- **Prices missing:** 7
- **Last successfully processed trade session:** 2026-10-14T02:00:59.959625+05:30
- **Trade-processing status:** outside_market_window

**Important:** The verified close is from Angel One. A missing price stays missing; previous trade prices are NOT marked as current. Total equity and P&L below are from the last *fully processed* session and may be stale.

## Open simulated holdings — last verified NSE close

| Stock | Qty | Buy ₹ | Verified Angel close ₹ | Close date | Verified unrealised ₹ | Status |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| DIL | 7692 | ₹0.65 | — | — | — | **Price unavailable — previous quote stale** |
| FCONSUMER | 22727 | ₹0.22 | — | — | — | **Price unavailable — previous quote stale** |
| GENSOL | 516 | ₹9.68 | ₹9.99 | 2026-10-30 | ₹159.96 | Verified |
| MORARJEE | 734 | ₹6.81 | ₹4.11 | 2026-10-30 | ₹-1,981.80 | Verified |
| NAGAFERT | 3267 | ₹1.53 | — | — | — | **Price unavailable — previous quote stale** |
| RAJVIR | 959 | ₹5.21 | — | — | — | **Price unavailable — previous quote stale** |
| SETUINFRA | 11363 | ₹0.44 | — | — | — | **Price unavailable — previous quote stale** |
| V2RETAIL | 33 | ₹151.45 | ₹147.47 | 2026-10-30 | ₹-131.34 | Verified |

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
| DECCANCE | Yes | No | ₹467.05 | Verified |
| GRADIENTE | Yes | No | ₹1.76 | Verified |
| BNAGROCHEM | Yes | No | ₹116.60 | Verified |
| BLUECHIP | Yes | No | ₹1.53 | Verified |
| VIVIMEDLAB | Yes | No | ₹5.53 | Verified |
| VELJAN | Yes | No | ₹2,049.70 | Verified |
| MBECL | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for MBECL on 2026-10-30; got 0 |
| GATEWAY | Yes | No | ₹42.87 | Verified |
| KOTIC | Yes | No | ₹104.98 | Verified |
| JSWDULUX | Yes | No | ₹264.40 | Verified |
| DYCL | Yes | No | ₹318.25 | Verified |
| FCONSUMER | Yes | Yes | — | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | Yes | Yes | — | Expected exactly one valid NSE ONE_DAY bar for DIL on 2026-10-30; got 0 |
| NAGAFERT | Yes | Yes | — | No exact NSE equity token found in instrument master for NAGAFERT |
| LASA | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for LASA on 2026-10-30; got 0 |
| RAJVIR | Yes | Yes | — | No exact NSE equity token found in instrument master for RAJVIR |
| ASTEC | Yes | No | ₹545.55 | Verified |
| GENESYS | Yes | No | ₹171.15 | Verified |
| V2RETAIL | No | Yes | ₹147.47 | Verified |
| SETUINFRA | No | Yes | — | Expected exactly one valid NSE ONE_DAY bar for SETUINFRA on 2026-10-30; got 0 |
| MORARJEE | No | Yes | ₹4.11 | Verified |
| GENSOL | No | Yes | ₹9.99 | Verified |

---
[Verified price audit](PRICE_CHECK.md) · [Latest scanner](SCANNER_SYMBOLS.md) · [Trade history](TRADE_HISTORY.md) · [GitHub Actions](../../actions) · [Graphical dashboard setup](README.md)
