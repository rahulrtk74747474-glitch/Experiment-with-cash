# Experiment with Cash — Latest Dashboard

**This dashboard works on GitHub without GitHub Pages.** This is paper trading only.

## Price-update status

- **Angel One observed NSE session:** 2026-10-26
- **Last attempted price check:** 2026-10-26T22:20:54.724898+05:30
- **Prices independently verified:** 24/28
- **Prices missing:** 4
- **Last successfully processed trade session:** 2026-10-14T02:00:59.959625+05:30
- **Trade-processing status:** outside_market_window

**Important:** The verified close is from Angel One. A missing price stays missing; previous trade prices are NOT marked as current. Total equity and P&L below are from the last *fully processed* session and may be stale.

## Open simulated holdings — last verified NSE close

| Stock | Qty | Buy ₹ | Verified Angel close ₹ | Close date | Verified unrealised ₹ | Status |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| DIL | 7692 | ₹0.65 | — | — | — | **Price unavailable — previous quote stale** |
| FCONSUMER | 22727 | ₹0.22 | — | — | — | **Price unavailable — previous quote stale** |
| GENSOL | 516 | ₹9.68 | ₹10.62 | 2026-10-26 | ₹485.04 | Verified |
| MORARJEE | 734 | ₹6.81 | ₹4.55 | 2026-10-26 | ₹-1,658.84 | Verified |
| NAGAFERT | 3267 | ₹1.53 | ₹1.39 | 2026-10-26 | ₹-457.38 | Verified |
| RAJVIR | 959 | ₹5.21 | ₹4.94 | 2026-10-26 | ₹-258.93 | Verified |
| SETUINFRA | 11363 | ₹0.44 | — | — | — | **Price unavailable — previous quote stale** |
| V2RETAIL | 33 | ₹151.45 | ₹161.36 | 2026-10-26 | ₹327.03 | Verified |

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
| TECHNOE | Yes | No | ₹828.90 | Verified |
| PCBL | Yes | No | ₹275.45 | Verified |
| INDRAMEDCO | Yes | No | ₹300.05 | Verified |
| ENDURANCE | Yes | No | ₹2,217.00 | Verified |
| WABAG | Yes | No | ₹1,707.40 | Verified |
| ANANTRAJ | Yes | No | ₹458.85 | Verified |
| GREENPANEL | Yes | No | ₹131.00 | Verified |
| ORCHPHARMA | Yes | No | ₹818.35 | Verified |
| GREAVESCOT | Yes | No | ₹182.32 | Verified |
| SOLEX | Yes | No | ₹526.95 | Verified |
| INA | Yes | No | ₹63.14 | Verified |
| AGSTRA | Yes | No | ₹1.94 | Verified |
| HINDCON | Yes | No | ₹22.50 | Verified |
| FUSION | Yes | No | ₹137.25 | Verified |
| BLUECHIP | Yes | No | ₹1.65 | Verified |
| MBECL | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for MBECL on 2026-10-26; got 0 |
| ACSTECH | Yes | No | ₹59.90 | Verified |
| TITAGARH | Yes | No | ₹649.55 | Verified |
| QUADFUTURE | Yes | No | ₹396.00 | Verified |
| FLFL | Yes | No | ₹0.76 | Verified |
| V2RETAIL | No | Yes | ₹161.36 | Verified |
| RAJVIR | No | Yes | ₹4.94 | Verified |
| SETUINFRA | No | Yes | — | Expected exactly one valid NSE ONE_DAY bar for SETUINFRA on 2026-10-26; got 0 |
| FCONSUMER | No | Yes | — | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | No | Yes | — | Expected exactly one valid NSE ONE_DAY bar for DIL on 2026-10-26; got 0 |
| MORARJEE | No | Yes | ₹4.55 | Verified |
| GENSOL | No | Yes | ₹10.62 | Verified |
| NAGAFERT | No | Yes | ₹1.39 | Verified |

---
[Verified price audit](PRICE_CHECK.md) · [Latest scanner](SCANNER_SYMBOLS.md) · [Trade history](TRADE_HISTORY.md) · [GitHub Actions](../../actions) · [Graphical dashboard setup](README.md)
