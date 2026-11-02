# Experiment with Cash — Latest Dashboard

**This dashboard works on GitHub without GitHub Pages.** This is paper trading only.

## Price-update status

- **Angel One observed NSE session:** 2026-11-02
- **Last attempted price check:** 2026-11-03T02:22:44.768457+05:30
- **Prices independently verified:** 11/17
- **Prices missing:** 6
- **Last successfully processed trade session:** 2026-10-14T02:00:59.959625+05:30
- **Trade-processing status:** outside_market_window

**Important:** The verified close is from Angel One. A missing price stays missing; previous trade prices are NOT marked as current. Total equity and P&L below are from the last *fully processed* session and may be stale.

## Open simulated holdings — last verified NSE close

| Stock | Qty | Buy ₹ | Verified Angel close ₹ | Close date | Verified unrealised ₹ | Status |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| DIL | 7692 | ₹0.65 | — | — | — | **Price unavailable — previous quote stale** |
| FCONSUMER | 22727 | ₹0.22 | — | — | — | **Price unavailable — previous quote stale** |
| GENSOL | 516 | ₹9.68 | ₹9.88 | 2026-11-02 | ₹103.20 | Verified |
| MORARJEE | 734 | ₹6.81 | ₹3.94 | 2026-11-02 | ₹-2,106.58 | Verified |
| NAGAFERT | 3267 | ₹1.53 | ₹1.33 | 2026-11-02 | ₹-653.40 | Verified |
| RAJVIR | 959 | ₹5.21 | — | — | — | **Price unavailable — previous quote stale** |
| SETUINFRA | 11363 | ₹0.44 | — | — | — | **Price unavailable — previous quote stale** |
| V2RETAIL | 33 | ₹151.45 | ₹161.26 | 2026-11-02 | ₹323.73 | Verified |

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
| ANSALAPI | Yes | No | ₹3.19 | Verified |
| JSWDULUX | Yes | No | ₹261.25 | Verified |
| BLUECHIP | Yes | No | ₹1.50 | Verified |
| VIVIMEDLAB | Yes | No | ₹5.42 | Verified |
| VELJAN | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for VELJAN on 2026-11-02; got 0 |
| MBECL | Yes | No | — | Expected exactly one valid NSE ONE_DAY bar for MBECL on 2026-11-02; got 0 |
| MODISONLTD | Yes | No | ₹331.75 | Verified |
| NAGAFERT | Yes | Yes | ₹1.33 | Verified |
| FCONSUMER | Yes | Yes | — | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | Yes | Yes | — | Expected exactly one valid NSE ONE_DAY bar for DIL on 2026-11-02; got 0 |
| KOTIC | Yes | No | ₹100.03 | Verified |
| LASA | Yes | No | ₹4.44 | Verified |
| RAJVIR | Yes | Yes | — | Expected exactly one valid NSE ONE_DAY bar for RAJVIR on 2026-11-02; got 0 |
| V2RETAIL | No | Yes | ₹161.26 | Verified |
| SETUINFRA | No | Yes | — | Expected exactly one valid NSE ONE_DAY bar for SETUINFRA on 2026-11-02; got 0 |
| MORARJEE | No | Yes | ₹3.94 | Verified |
| GENSOL | No | Yes | ₹9.88 | Verified |

---
[Verified price audit](PRICE_CHECK.md) · [Latest scanner](SCANNER_SYMBOLS.md) · [Trade history](TRADE_HISTORY.md) · [GitHub Actions](../../actions) · [Graphical dashboard setup](README.md)
