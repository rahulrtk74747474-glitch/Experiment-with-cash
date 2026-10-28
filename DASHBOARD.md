# Experiment with Cash — Latest Dashboard

**This dashboard works on GitHub without GitHub Pages.** This is paper trading only.

## Price-update status

- **Angel One observed NSE session:** 2026-10-28
- **Last attempted price check:** 2026-10-28T22:14:37.719624+05:30
- **Prices independently verified:** 17/24
- **Prices missing:** 7
- **Last successfully processed trade session:** 2026-10-14T02:00:59.959625+05:30
- **Trade-processing status:** outside_market_window

**Important:** The verified close is from Angel One. A missing price stays missing; previous trade prices are NOT marked as current. Total equity and P&L below are from the last *fully processed* session and may be stale.

## Open simulated holdings — last verified NSE close

| Stock | Qty | Buy ₹ | Verified Angel close ₹ | Close date | Verified unrealised ₹ | Status |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| DIL | 7692 | ₹0.65 | — | — | — | **Price unavailable — previous quote stale** |
| FCONSUMER | 22727 | ₹0.22 | — | — | — | **Price unavailable — previous quote stale** |
| GENSOL | 516 | ₹9.68 | ₹10.64 | 2026-10-28 | ₹495.36 | Verified |
| MORARJEE | 734 | ₹6.81 | ₹4.54 | 2026-10-28 | ₹-1,666.18 | Verified |
| NAGAFERT | 3267 | ₹1.53 | — | — | — | **Price unavailable — previous quote stale** |
| RAJVIR | 959 | ₹5.21 | — | — | — | **Price unavailable — previous quote stale** |
| SETUINFRA | 11363 | ₹0.44 | — | — | — | **Price unavailable — previous quote stale** |
| V2RETAIL | 33 | ₹151.45 | ₹155.44 | 2026-10-28 | ₹131.67 | Verified |

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
| SHAKTIPUMP | Yes | No | ₹364.45 | Verified |
| GICHSGFIN | Yes | No | ₹121.95 | Verified |
| KSB | Yes | No | ₹651.00 | Verified |
| JSWDULUX | Yes | No | ₹275.90 | Verified |
| AEGISVOPAK | Yes | No | ₹231.80 | Verified |
| DECCANCE | Yes | No | ₹473.50 | Verified |
| AGSTRA | Yes | No | ₹1.88 | Verified |
| BLUECHIP | Yes | No | ₹1.59 | Verified |
| DELPHIFX | Yes | No | ₹5.78 | Verified |
| ABAN | Yes | No | ₹13.94 | Verified |
| MBECL | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for MBECL on 2026-10-28; got 0 |
| ACSTECH | Yes | No | ₹58.71 | Verified |
| FLEXITUFF | Yes | No | ₹2.45 | Verified |
| SETUINFRA | Yes | Yes | — | Expected exactly one valid NSE ONE_DAY bar for SETUINFRA on 2026-10-28; got 0 |
| FCONSUMER | Yes | Yes | — | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | Yes | Yes | — | Expected exactly one valid NSE ONE_DAY bar for DIL on 2026-10-28; got 0 |
| PKTEA | Yes | No | ₹658.60 | Verified |
| NAGAFERT | Yes | Yes | — | No exact NSE equity token found in instrument master for NAGAFERT |
| LASA | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for LASA on 2026-10-28; got 0 |
| BNAGROCHEM | Yes | No | ₹116.99 | Verified |
| V2RETAIL | No | Yes | ₹155.44 | Verified |
| RAJVIR | No | Yes | — | No exact NSE equity token found in instrument master for RAJVIR |
| MORARJEE | No | Yes | ₹4.54 | Verified |
| GENSOL | No | Yes | ₹10.64 | Verified |

---
[Verified price audit](PRICE_CHECK.md) · [Latest scanner](SCANNER_SYMBOLS.md) · [Trade history](TRADE_HISTORY.md) · [GitHub Actions](../../actions) · [Graphical dashboard setup](README.md)
