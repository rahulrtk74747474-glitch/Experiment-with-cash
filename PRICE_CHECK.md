# NSE daily close verification — Angel One SmartAPI only

[Active Trades](ACTIVE_TRADES.md) · [Chartink Scanner](SCANNER_SYMBOLS.md) · [Workflow](.github/workflows/vertex-paper-trading.yml)

**NSE session:** 2026-11-05  
**Checked at (IST):** 05 Nov 2026 11:47 PM  
**Status:** partial  
**Verified:** 5/12  

Chartink supplies stock symbols only. Prices below are Angel One daily candle closes, not an assumption that an order executed at that exact price.

| Symbol | Scanner? | Held? | Angel daily close ₹ | Candle date/time | Status | Error |
| --- | :---: | :---: | ---: | --- | --- | --- |
| BLUECHIP | Yes | No | 1.45 | 2026-11-05T00:00:00+05:30 | verified | — |
| ANKITMETAL | Yes | No | 2.01 | 2026-11-05T00:00:00+05:30 | verified | — |
| MBECL | Yes | No | — | — | missing | Expected exactly one valid NSE ONE_DAY bar for MBECL on 2026-11-05; got 0 |
| NAGAFERT | Yes | Yes | — | — | missing | No exact NSE equity token found in instrument master for NAGAFERT |
| FCONSUMER | Yes | Yes | — | — | missing | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | Yes | Yes | — | — | missing | Expected exactly one valid NSE ONE_DAY bar for DIL on 2026-11-05; got 0 |
| LASA | Yes | No | — | — | missing | Expected exactly one valid NSE ONE_DAY bar for LASA on 2026-11-05; got 0 |
| RAJVIR | Yes | Yes | — | — | missing | No exact NSE equity token found in instrument master for RAJVIR |
| V2RETAIL | No | Yes | 161.34 | 2026-11-05T00:00:00+05:30 | verified | — |
| SETUINFRA | No | Yes | — | — | missing | Expected exactly one valid NSE ONE_DAY bar for SETUINFRA on 2026-11-05; got 0 |
| MORARJEE | No | Yes | 3.96 | 2026-11-05T00:00:00+05:30 | verified | — |
| GENSOL | No | Yes | 9.73 | 2026-11-05T00:00:00+05:30 | verified | — |
