# Experiment with Cash — Latest Dashboard

**This dashboard works on GitHub without GitHub Pages.** This is paper trading only.

## Price-update status

- **Angel One observed NSE session:** 2026-10-23
- **Last attempted price check:** 2026-10-23T21:32:46.969928+05:30
- **Prices independently verified:** 19/26
- **Prices missing:** 7
- **Last successfully processed trade session:** 2026-10-14T02:00:59.959625+05:30
- **Trade-processing status:** outside_market_window

**Important:** The verified close is from Angel One. A missing price stays missing; previous trade prices are NOT marked as current. Total equity and P&L below are from the last *fully processed* session and may be stale.

## Open simulated holdings — last verified NSE close

| Stock | Qty | Buy ₹ | Verified Angel close ₹ | Close date | Verified unrealised ₹ | Status |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| DIL | 7692 | ₹0.65 | — | — | — | **Price unavailable — previous quote stale** |
| FCONSUMER | 22727 | ₹0.22 | — | — | — | **Price unavailable — previous quote stale** |
| GENSOL | 516 | ₹9.68 | ₹11.39 | 2026-10-23 | ₹882.36 | Verified |
| MORARJEE | 734 | ₹6.81 | ₹4.78 | 2026-10-23 | ₹-1,490.02 | Verified |
| NAGAFERT | 3267 | ₹1.53 | — | — | — | **Price unavailable — previous quote stale** |
| RAJVIR | 959 | ₹5.21 | — | — | — | **Price unavailable — previous quote stale** |
| SETUINFRA | 11363 | ₹0.44 | — | — | — | **Price unavailable — previous quote stale** |
| V2RETAIL | 33 | ₹151.45 | ₹162.81 | 2026-10-23 | ₹374.88 | Verified |

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
| SRGHFL | Yes | No | ₹101.96 | Verified |
| RAJVIR | Yes | Yes | — | No exact NSE equity token found in instrument master for RAJVIR |
| MEDANTA | Yes | No | ₹1,185.00 | Verified |
| PAR | Yes | No | ₹104.99 | Verified |
| NIFTYMIDSMLHLTH | Yes | No | — | No exact NSE equity token found in instrument master for NIFTYMIDSMLHLTH |
| SANOFICONR | Yes | No | ₹3,209.00 | Verified |
| BLUECHIP | Yes | No | ₹1.68 | Verified |
| RAMASTEEL | Yes | No | ₹3.66 | Verified |
| AGSTRA | Yes | No | ₹1.97 | Verified |
| MBECL | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for MBECL on 2026-10-23; got 0 |
| ANANTRAJ | Yes | No | ₹460.40 | Verified |
| SANGHVIMOV | Yes | No | ₹320.35 | Verified |
| ICICIAMC | Yes | No | ₹2,651.80 | Verified |
| KALYANIFRG | Yes | No | ₹717.50 | Verified |
| SETUINFRA | Yes | Yes | — | Expected exactly one valid NSE ONE_DAY bar for SETUINFRA on 2026-10-23; got 0 |
| MANINFRA | Yes | No | ₹102.50 | Verified |
| MOSCHIP | Yes | No | ₹164.75 | Verified |
| HINDCON | Yes | No | ₹22.95 | Verified |
| MAITHANALL | Yes | No | ₹798.80 | Verified |
| WELINV | Yes | No | ₹1,600.00 | Verified |
| V2RETAIL | No | Yes | ₹162.81 | Verified |
| FCONSUMER | No | Yes | — | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | No | Yes | — | No exact NSE equity token found in instrument master for DIL |
| MORARJEE | No | Yes | ₹4.78 | Verified |
| GENSOL | No | Yes | ₹11.39 | Verified |
| NAGAFERT | No | Yes | — | No exact NSE equity token found in instrument master for NAGAFERT |

---
[Verified price audit](PRICE_CHECK.md) · [Latest scanner](SCANNER_SYMBOLS.md) · [Trade history](TRADE_HISTORY.md) · [GitHub Actions](../../actions) · [Graphical dashboard setup](README.md)
