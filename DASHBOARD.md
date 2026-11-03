# Experiment with Cash — Latest Dashboard

**This dashboard works on GitHub without GitHub Pages.** This is paper trading only.

## Price-update status

- **Angel One observed NSE session:** 2026-11-03
- **Last attempted price check:** 2026-11-04T00:09:36.968788+05:30
- **Prices independently verified:** 19/27
- **Prices missing:** 8
- **Last successfully processed trade session:** 2026-10-14T02:00:59.959625+05:30
- **Trade-processing status:** outside_market_window

**Important:** The verified close is from Angel One. A missing price stays missing; previous trade prices are NOT marked as current. Total equity and P&L below are from the last *fully processed* session and may be stale.

## Open simulated holdings — last verified NSE close

| Stock | Qty | Buy ₹ | Verified Angel close ₹ | Close date | Verified unrealised ₹ | Status |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| DIL | 7692 | ₹0.65 | — | — | — | **Price unavailable — previous quote stale** |
| FCONSUMER | 22727 | ₹0.22 | — | — | — | **Price unavailable — previous quote stale** |
| GENSOL | 516 | ₹9.68 | ₹9.56 | 2026-11-03 | ₹-61.92 | Verified |
| MORARJEE | 734 | ₹6.81 | ₹4.13 | 2026-11-03 | ₹-1,967.12 | Verified |
| NAGAFERT | 3267 | ₹1.53 | — | — | — | **Price unavailable — previous quote stale** |
| RAJVIR | 959 | ₹5.21 | — | — | — | **Price unavailable — previous quote stale** |
| SETUINFRA | 11363 | ₹0.44 | — | — | — | **Price unavailable — previous quote stale** |
| V2RETAIL | 33 | ₹151.45 | ₹164.62 | 2026-11-03 | ₹434.61 | Verified |

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
| JSWDULUX | Yes | No | ₹260.25 | Verified |
| ANSALAPI | Yes | No | ₹3.14 | Verified |
| VIVIMEDLAB | Yes | No | ₹5.32 | Verified |
| MBECL | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for MBECL on 2026-11-03; got 0 |
| VELJAN | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for VELJAN on 2026-11-03; got 0 |
| BLUECHIP | Yes | No | ₹1.47 | Verified |
| SILVERCASE | Yes | No | ₹17.66 | Verified |
| SILVER1 | Yes | No | ₹16.92 | Verified |
| SBISILVER | Yes | No | ₹171.35 | Verified |
| SILVERAXIS | Yes | No | ₹173.81 | Verified |
| SILVERADD | Yes | No | ₹16.75 | Verified |
| SILVER | Yes | No | ₹174.26 | Verified |
| SILVERIETF | Yes | No | ₹174.00 | Verified |
| ESILVER | Yes | No | ₹174.68 | Verified |
| SILVERBEES | Yes | No | ₹166.81 | Verified |
| GROWWSLVR | Yes | No | ₹17.11 | Verified |
| SILVERAG | Yes | No | ₹170.18 | Verified |
| SILVERBETA | Yes | No | ₹168.31 | Verified |
| NAGAFERT | Yes | Yes | — | No exact NSE equity token found in instrument master for NAGAFERT |
| LASA | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for LASA on 2026-11-03; got 0 |
| V2RETAIL | No | Yes | ₹164.62 | Verified |
| RAJVIR | No | Yes | — | No exact NSE equity token found in instrument master for RAJVIR |
| SETUINFRA | No | Yes | — | Expected exactly one valid NSE ONE_DAY bar for SETUINFRA on 2026-11-03; got 0 |
| FCONSUMER | No | Yes | — | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | No | Yes | — | No exact NSE equity token found in instrument master for DIL |
| MORARJEE | No | Yes | ₹4.13 | Verified |
| GENSOL | No | Yes | ₹9.56 | Verified |

---
[Verified price audit](PRICE_CHECK.md) · [Latest scanner](SCANNER_SYMBOLS.md) · [Trade history](TRADE_HISTORY.md) · [GitHub Actions](../../actions) · [Graphical dashboard setup](README.md)
