# Experiment with Cash — Latest Dashboard

**This dashboard works on GitHub without GitHub Pages.** This is paper trading only.

## Price-update status

- **Angel One observed NSE session:** 2026-10-20
- **Last attempted price check:** 2026-10-20T20:53:05.181497+05:30
- **Prices independently verified:** 0/16
- **Prices missing:** 16
- **Last successfully processed trade session:** 2026-10-14T02:00:59.959625+05:30
- **Trade-processing status:** outside_market_window

**Important:** The verified close is from Angel One. A missing price stays missing; previous trade prices are NOT marked as current. Total equity and P&L below are from the last *fully processed* session and may be stale.

## Open simulated holdings — last verified NSE close

| Stock | Qty | Buy ₹ | Verified Angel close ₹ | Close date | Verified unrealised ₹ | Status |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| DIL | 7692 | ₹0.65 | — | — | — | **Price unavailable — previous quote stale** |
| FCONSUMER | 22727 | ₹0.22 | — | — | — | **Price unavailable — previous quote stale** |
| GENSOL | 516 | ₹9.68 | — | — | — | **Price unavailable — previous quote stale** |
| MORARJEE | 734 | ₹6.81 | — | — | — | **Price unavailable — previous quote stale** |
| NAGAFERT | 3267 | ₹1.53 | — | — | — | **Price unavailable — previous quote stale** |
| RAJVIR | 959 | ₹5.21 | — | — | — | **Price unavailable — previous quote stale** |
| SETUINFRA | 11363 | ₹0.44 | — | — | — | **Price unavailable — previous quote stale** |
| V2RETAIL | 33 | ₹151.45 | — | — | — | **Price unavailable — previous quote stale** |

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
| ROHLTD | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for ROHLTD on 2026-10-20; got 0 |
| BLUECHIP | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for BLUECHIP on 2026-10-20; got 0 |
| INNOVACAP | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for INNOVACAP on 2026-10-20; got 0 |
| CAPLIPOINT | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for CAPLIPOINT on 2026-10-20; got 0 |
| EXIDEIND | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for EXIDEIND on 2026-10-20; got 0 |
| GOCOLORS | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for GOCOLORS on 2026-10-20; got 0 |
| TALBROAUTO | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for TALBROAUTO on 2026-10-20; got 0 |
| FCONSUMER | Yes | Yes | — | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | Yes | Yes | — | Expected exactly one valid NSE ONE_DAY bar for DIL on 2026-10-20; got 0 |
| NAGAFERT | Yes | Yes | — | No exact NSE equity token found in instrument master for NAGAFERT |
| LASA | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for LASA on 2026-10-20; got 0 |
| MORARJEE | Yes | Yes | — | Expected exactly one valid NSE ONE_DAY bar for MORARJEE on 2026-10-20; got 0 |
| V2RETAIL | No | Yes | — | Expected exactly one valid NSE ONE_DAY bar for V2RETAIL on 2026-10-20; got 0 |
| SETUINFRA | No | Yes | — | Expected exactly one valid NSE ONE_DAY bar for SETUINFRA on 2026-10-20; got 0 |
| GENSOL | No | Yes | — | Expected exactly one valid NSE ONE_DAY bar for GENSOL on 2026-10-20; got 0 |

---
[Verified price audit](PRICE_CHECK.md) · [Latest scanner](SCANNER_SYMBOLS.md) · [Trade history](TRADE_HISTORY.md) · [GitHub Actions](../../actions) · [Graphical dashboard setup](README.md)
