# Experiment with Cash — Latest Dashboard

**This dashboard works on GitHub without GitHub Pages.** This is paper trading only.

## Price-update status

- **Angel One observed NSE session:** 2026-11-26
- **Last attempted price check:** 2026-11-27T01:20:21.924516+05:30
- **Prices independently verified:** 10/17
- **Prices missing:** 7
- **Last successfully processed trade session:** 2026-10-14T02:00:59.959625+05:30
- **Trade-processing status:** outside_market_window

**Important:** The verified close is from Angel One. A missing price stays missing; previous trade prices are NOT marked as current. Total equity and P&L below are from the last *fully processed* session and may be stale.

## Open simulated holdings — last verified NSE close

| Stock | Qty | Buy ₹ | Verified Angel close ₹ | Close date | Verified unrealised ₹ | Status |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| DIL | 7692 | ₹0.65 | — | — | — | **Price unavailable — previous quote stale** |
| FCONSUMER | 22727 | ₹0.22 | — | — | — | **Price unavailable — previous quote stale** |
| GENSOL | 516 | ₹9.68 | ₹9.27 | 2026-11-26 | ₹-211.56 | Verified |
| MORARJEE | 734 | ₹6.81 | ₹5.84 | 2026-11-26 | ₹-711.98 | Verified |
| NAGAFERT | 3267 | ₹1.53 | — | — | — | **Price unavailable — previous quote stale** |
| RAJVIR | 959 | ₹5.21 | — | — | — | **Price unavailable — previous quote stale** |
| SETUINFRA | 11363 | ₹0.44 | — | — | — | **Price unavailable — previous quote stale** |
| V2RETAIL | 33 | ₹151.45 | ₹142.26 | 2026-11-26 | ₹-303.27 | Verified |

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
| SHANKESH | Yes | No | ₹73.10 | Verified |
| CRISIL | Yes | No | ₹3,977.20 | Verified |
| ARROWGREEN | Yes | No | ₹625.95 | Verified |
| BLEL | Yes | No | ₹371.40 | Verified |
| UTLSOLAR | Yes | No | ₹272.40 | Verified |
| ICDSLTD | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for ICDSLTD on 2026-11-26; got 0 |
| PARSVNATH | Yes | No | ₹2.31 | Verified |
| VALIANTLAB | Yes | No | ₹89.34 | Verified |
| LASA | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for LASA on 2026-11-26; got 0 |
| RAJVIR | Yes | Yes | — | No exact NSE equity token found in instrument master for RAJVIR |
| V2RETAIL | No | Yes | ₹142.26 | Verified |
| SETUINFRA | No | Yes | — | Expected exactly one valid NSE ONE_DAY bar for SETUINFRA on 2026-11-26; got 0 |
| FCONSUMER | No | Yes | — | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | No | Yes | — | Expected exactly one valid NSE ONE_DAY bar for DIL on 2026-11-26; got 0 |
| MORARJEE | No | Yes | ₹5.84 | Verified |
| GENSOL | No | Yes | ₹9.27 | Verified |
| NAGAFERT | No | Yes | — | No exact NSE equity token found in instrument master for NAGAFERT |

---
[Verified price audit](PRICE_CHECK.md) · [Latest scanner](SCANNER_SYMBOLS.md) · [Trade history](TRADE_HISTORY.md) · [GitHub Actions](../../actions) · [Graphical dashboard setup](README.md)
