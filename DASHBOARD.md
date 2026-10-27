# Experiment with Cash — Latest Dashboard

**This dashboard works on GitHub without GitHub Pages.** This is paper trading only.

## Price-update status

- **Angel One observed NSE session:** 2026-10-27
- **Last attempted price check:** 2026-10-27T22:24:46.514136+05:30
- **Prices independently verified:** 14/21
- **Prices missing:** 7
- **Last successfully processed trade session:** 2026-10-14T02:00:59.959625+05:30
- **Trade-processing status:** outside_market_window

**Important:** The verified close is from Angel One. A missing price stays missing; previous trade prices are NOT marked as current. Total equity and P&L below are from the last *fully processed* session and may be stale.

## Open simulated holdings — last verified NSE close

| Stock | Qty | Buy ₹ | Verified Angel close ₹ | Close date | Verified unrealised ₹ | Status |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| DIL | 7692 | ₹0.65 | — | — | — | **Price unavailable — previous quote stale** |
| FCONSUMER | 22727 | ₹0.22 | — | — | — | **Price unavailable — previous quote stale** |
| GENSOL | 516 | ₹9.68 | ₹10.64 | 2026-10-27 | ₹495.36 | Verified |
| MORARJEE | 734 | ₹6.81 | ₹4.33 | 2026-10-27 | ₹-1,820.32 | Verified |
| NAGAFERT | 3267 | ₹1.53 | — | — | — | **Price unavailable — previous quote stale** |
| RAJVIR | 959 | ₹5.21 | — | — | — | **Price unavailable — previous quote stale** |
| SETUINFRA | 11363 | ₹0.44 | — | — | — | **Price unavailable — previous quote stale** |
| V2RETAIL | 33 | ₹151.45 | ₹157.57 | 2026-10-27 | ₹201.96 | Verified |

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
| JSWDULUX | Yes | No | ₹280.40 | Verified |
| ACSTECH | Yes | No | ₹59.90 | Verified |
| GREAVESCOT | Yes | No | ₹181.68 | Verified |
| DECCANCE | Yes | No | ₹480.00 | Verified |
| FUSION | Yes | No | ₹135.82 | Verified |
| FLFL | Yes | No | ₹0.74 | Verified |
| AGSTRA | Yes | No | ₹1.91 | Verified |
| BLUECHIP | Yes | No | ₹1.62 | Verified |
| MBECL | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for MBECL on 2026-10-27; got 0 |
| AEGISVOPAK | Yes | No | ₹235.10 | Verified |
| SETUINFRA | Yes | Yes | — | Expected exactly one valid NSE ONE_DAY bar for SETUINFRA on 2026-10-27; got 0 |
| FCONSUMER | Yes | Yes | — | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | Yes | Yes | — | Expected exactly one valid NSE ONE_DAY bar for DIL on 2026-10-27; got 0 |
| NAGAFERT | Yes | Yes | — | No exact NSE equity token found in instrument master for NAGAFERT |
| MORARJEE | Yes | Yes | ₹4.33 | Verified |
| LASA | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for LASA on 2026-10-27; got 0 |
| BNAGROCHEM | Yes | No | ₹123.14 | Verified |
| RAJVIR | Yes | Yes | — | No exact NSE equity token found in instrument master for RAJVIR |
| SUYOG | Yes | No | ₹442.70 | Verified |
| V2RETAIL | No | Yes | ₹157.57 | Verified |
| GENSOL | No | Yes | ₹10.64 | Verified |

---
[Verified price audit](PRICE_CHECK.md) · [Latest scanner](SCANNER_SYMBOLS.md) · [Trade history](TRADE_HISTORY.md) · [GitHub Actions](../../actions) · [Graphical dashboard setup](README.md)
