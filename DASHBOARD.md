# Experiment with Cash — Latest Dashboard

**This dashboard works on GitHub without GitHub Pages.** This is paper trading only.

## Price-update status

- **Angel One observed NSE session:** 2026-10-19
- **Last attempted price check:** 2026-10-19T22:41:11.782353+05:30
- **Prices independently verified:** 13/16
- **Prices missing:** 3
- **Last successfully processed trade session:** 2026-10-14T02:00:59.959625+05:30
- **Trade-processing status:** outside_market_window

**Important:** The verified close is from Angel One. A missing price stays missing; previous trade prices are NOT marked as current. Total equity and P&L below are from the last *fully processed* session and may be stale.

## Open simulated holdings — last verified NSE close

| Stock | Qty | Buy ₹ | Verified Angel close ₹ | Close date | Verified unrealised ₹ | Status |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| DIL | 7692 | ₹0.65 | — | — | — | **Price unavailable — previous quote stale** |
| FCONSUMER | 22727 | ₹0.22 | — | — | — | **Price unavailable — previous quote stale** |
| GENSOL | 516 | ₹9.68 | ₹10.93 | 2026-10-19 | ₹645.00 | Verified |
| MORARJEE | 734 | ₹6.81 | ₹5.56 | 2026-10-19 | ₹-917.50 | Verified |
| NAGAFERT | 3267 | ₹1.53 | ₹1.46 | 2026-10-19 | ₹-228.69 | Verified |
| RAJVIR | 959 | ₹5.21 | ₹5.20 | 2026-10-19 | ₹-9.59 | Verified |
| SETUINFRA | 11363 | ₹0.44 | — | — | — | **Price unavailable — previous quote stale** |
| V2RETAIL | 33 | ₹151.45 | ₹174.80 | 2026-10-19 | ₹770.55 | Verified |

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
| RAJVIR | Yes | Yes | ₹5.20 | Verified |
| ROHLTD | Yes | No | ₹274.05 | Verified |
| BLUECHIP | Yes | No | ₹1.77 | Verified |
| INNOVACAP | Yes | No | ₹1,001.70 | Verified |
| CAPLIPOINT | Yes | No | ₹2,258.80 | Verified |
| EXIDEIND | Yes | No | ₹360.15 | Verified |
| GOCOLORS | Yes | No | ₹265.40 | Verified |
| TALBROAUTO | Yes | No | ₹353.10 | Verified |
| FCONSUMER | Yes | Yes | — | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | Yes | Yes | — | Expected exactly one valid NSE ONE_DAY bar for DIL on 2026-10-19; got 0 |
| NAGAFERT | Yes | Yes | ₹1.46 | Verified |
| LASA | Yes | No | ₹4.91 | Verified |
| MORARJEE | Yes | Yes | ₹5.56 | Verified |
| V2RETAIL | No | Yes | ₹174.80 | Verified |
| SETUINFRA | No | Yes | — | Expected exactly one valid NSE ONE_DAY bar for SETUINFRA on 2026-10-19; got 0 |
| GENSOL | No | Yes | ₹10.93 | Verified |

---
[Verified price audit](PRICE_CHECK.md) · [Latest scanner](SCANNER_SYMBOLS.md) · [Trade history](TRADE_HISTORY.md) · [GitHub Actions](../../actions) · [Graphical dashboard setup](README.md)
