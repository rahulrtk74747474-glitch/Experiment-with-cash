# NSE daily close verification — Angel One SmartAPI only

[Active Trades](ACTIVE_TRADES.md) · [Chartink Scanner](SCANNER_SYMBOLS.md) · [Workflow](.github/workflows/vertex-paper-trading.yml)

**NSE session:** 2026-11-06  
**Checked at (IST):** 06 Nov 2026 11:25 PM  
**Status:** partial  
**Verified:** 5/12  

Chartink supplies stock symbols only. Prices below are Angel One daily candle closes, not an assumption that an order executed at that exact price.

| Symbol | Scanner? | Held? | Angel daily close ₹ | Candle date/time | Status | Error |
| --- | :---: | :---: | ---: | --- | --- | --- |
| GKSL | Yes | No | 157.79 | 2026-11-06T00:00:00+05:30 | verified | — |
| MBECL | Yes | No | — | — | missing | Expected exactly one valid NSE ONE_DAY bar for MBECL on 2026-11-06; got 0 |
| ANKITMETAL | Yes | No | 1.97 | 2026-11-06T00:00:00+05:30 | verified | — |
| NAGAFERT | Yes | Yes | — | — | missing | No exact NSE equity token found in instrument master for NAGAFERT |
| FCONSUMER | Yes | Yes | — | — | missing | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | Yes | Yes | — | — | missing | No exact NSE equity token found in instrument master for DIL |
| LASA | Yes | No | — | — | missing | Expected exactly one valid NSE ONE_DAY bar for LASA on 2026-11-06; got 0 |
| RAJVIR | Yes | Yes | — | — | missing | No exact NSE equity token found in instrument master for RAJVIR |
| V2RETAIL | No | Yes | 173.5 | 2026-11-06T00:00:00+05:30 | verified | — |
| SETUINFRA | No | Yes | — | — | missing | Expected exactly one valid NSE ONE_DAY bar for SETUINFRA on 2026-11-06; got 0 |
| MORARJEE | No | Yes | 3.91 | 2026-11-06T00:00:00+05:30 | verified | — |
| GENSOL | No | Yes | 9.76 | 2026-11-06T00:00:00+05:30 | verified | — |
