# Experiment with Cash — Latest Dashboard

**This dashboard works on GitHub without GitHub Pages.** This is paper trading only.

## Price-update status

- **Angel One observed NSE session:** 2026-10-21
- **Last attempted price check:** 2026-10-21T21:07:34.362012+05:30
- **Prices independently verified:** 17/23
- **Prices missing:** 6
- **Last successfully processed trade session:** 2026-10-14T02:00:59.959625+05:30
- **Trade-processing status:** outside_market_window

**Important:** The verified close is from Angel One. A missing price stays missing; previous trade prices are NOT marked as current. Total equity and P&L below are from the last *fully processed* session and may be stale.

## Open simulated holdings — last verified NSE close

| Stock | Qty | Buy ₹ | Verified Angel close ₹ | Close date | Verified unrealised ₹ | Status |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| DIL | 7692 | ₹0.65 | — | — | — | **Price unavailable — previous quote stale** |
| FCONSUMER | 22727 | ₹0.22 | — | — | — | **Price unavailable — previous quote stale** |
| GENSOL | 516 | ₹9.68 | ₹11.30 | 2026-10-21 | ₹835.92 | Verified |
| MORARJEE | 734 | ₹6.81 | ₹5.29 | 2026-10-21 | ₹-1,115.68 | Verified |
| NAGAFERT | 3267 | ₹1.53 | — | — | — | **Price unavailable — previous quote stale** |
| RAJVIR | 959 | ₹5.21 | — | — | — | **Price unavailable — previous quote stale** |
| SETUINFRA | 11363 | ₹0.44 | — | — | — | **Price unavailable — previous quote stale** |
| V2RETAIL | 33 | ₹151.45 | ₹167.64 | 2026-10-21 | ₹534.27 | Verified |

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
| RAJVIR | Yes | Yes | — | No exact NSE equity token found in instrument master for RAJVIR |
| EXIDEIND | Yes | No | ₹358.20 | Verified |
| GOCOLORS | Yes | No | ₹266.90 | Verified |
| ENTERO | Yes | No | ₹1,507.00 | Verified |
| CAPLIPOINT | Yes | No | ₹2,221.60 | Verified |
| BLUECHIP | Yes | No | ₹1.74 | Verified |
| STYL | Yes | No | ₹307.00 | Verified |
| GREENPANEL | Yes | No | ₹137.43 | Verified |
| INNOVACAP | Yes | No | ₹980.20 | Verified |
| BANSALWIRE | Yes | No | ₹61.15 | Verified |
| TALBROAUTO | Yes | No | ₹343.95 | Verified |
| MANINFRA | Yes | No | ₹106.75 | Verified |
| FCONSUMER | Yes | Yes | — | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | Yes | Yes | — | Expected exactly one valid NSE ONE_DAY bar for DIL on 2026-10-21; got 0 |
| SRGHFL | Yes | No | ₹106.00 | Verified |
| NAGAFERT | Yes | Yes | — | No exact NSE equity token found in instrument master for NAGAFERT |
| LASA | Yes | No | — | No exact NSE equity token found in instrument master for LASA |
| MORARJEE | Yes | Yes | ₹5.29 | Verified |
| INA | Yes | No | ₹67.02 | Verified |
| ALPINETEX | Yes | No | ₹38.20 | Verified |
| V2RETAIL | No | Yes | ₹167.64 | Verified |
| SETUINFRA | No | Yes | — | Expected exactly one valid NSE ONE_DAY bar for SETUINFRA on 2026-10-21; got 0 |
| GENSOL | No | Yes | ₹11.30 | Verified |

---
[Verified price audit](PRICE_CHECK.md) · [Latest scanner](SCANNER_SYMBOLS.md) · [Trade history](TRADE_HISTORY.md) · [GitHub Actions](../../actions) · [Graphical dashboard setup](README.md)
