# NSE daily close verification — Angel One SmartAPI only

[Active Trades](ACTIVE_TRADES.md) · [Chartink Scanner](SCANNER_SYMBOLS.md) · [Workflow](.github/workflows/vertex-paper-trading.yml)

**NSE session:** 2026-11-12  
**Checked at (IST):** 12 Nov 2026 11:56 PM  
**Status:** partial  
**Verified:** 6/12  

Chartink supplies stock symbols only. Prices below are Angel One daily candle closes, not an assumption that an order executed at that exact price.

| Symbol | Scanner? | Held? | Angel daily close ₹ | Candle date/time | Status | Error |
| --- | :---: | :---: | ---: | --- | --- | --- |
| ANKITMETAL | Yes | No | 1.85 | 2026-11-12T00:00:00+05:30 | verified | — |
| NAGAFERT | Yes | Yes | — | — | missing | No exact NSE equity token found in instrument master for NAGAFERT |
| ORTEL | Yes | No | 1.5 | 2026-11-12T00:00:00+05:30 | verified | — |
| LASA | Yes | No | — | — | missing | Expected exactly one valid NSE ONE_DAY bar for LASA on 2026-11-12; got 0 |
| SPELS | Yes | No | 82.88 | 2026-11-12T00:00:00+05:30 | verified | — |
| RAJVIR | Yes | Yes | — | — | missing | No exact NSE equity token found in instrument master for RAJVIR |
| V2RETAIL | No | Yes | 186.11 | 2026-11-12T00:00:00+05:30 | verified | — |
| SETUINFRA | No | Yes | — | — | missing | Expected exactly one valid NSE ONE_DAY bar for SETUINFRA on 2026-11-12; got 0 |
| FCONSUMER | No | Yes | — | — | missing | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | No | Yes | — | — | missing | Expected exactly one valid NSE ONE_DAY bar for DIL on 2026-11-12; got 0 |
| MORARJEE | No | Yes | 4.73 | 2026-11-12T00:00:00+05:30 | verified | — |
| GENSOL | No | Yes | 10.2 | 2026-11-12T00:00:00+05:30 | verified | — |
