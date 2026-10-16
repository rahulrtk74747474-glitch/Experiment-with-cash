# NSE daily close verification — Angel One SmartAPI only

[Active Trades](ACTIVE_TRADES.md) · [Chartink Scanner](SCANNER_SYMBOLS.md) · [Workflow](.github/workflows/vertex-paper-trading.yml)

**NSE session:** 2026-10-16  
**Checked at (IST):** 16 Oct 2026 08:30 PM  
**Status:** partial  
**Verified:** 6/11  

Chartink supplies stock symbols only. Prices below are Angel One daily candle closes, not an assumption that an order executed at that exact price.

| Symbol | Scanner? | Held? | Angel daily close ₹ | Candle date/time | Status | Error |
| --- | :---: | :---: | ---: | --- | --- | --- |
| CAPLIPOINT | Yes | No | 2301.3 | 2026-10-16T00:00:00+05:30 | verified | — |
| INNOVACAP | Yes | No | 1013.0 | 2026-10-16T00:00:00+05:30 | verified | — |
| XPROINDIA | Yes | No | 975.1 | 2026-10-16T00:00:00+05:30 | verified | — |
| RAJVIR | Yes | Yes | — | — | missing | No exact NSE equity token found in instrument master for RAJVIR |
| FCONSUMER | Yes | Yes | — | — | missing | No exact NSE equity token found in instrument master for FCONSUMER |
| DIL | Yes | Yes | — | — | missing | Expected exactly one valid NSE ONE_DAY bar for DIL on 2026-10-16; got 0 |
| MORARJEE | Yes | Yes | 5.85 | 2026-10-16T00:00:00+05:30 | verified | — |
| NAGAFERT | Yes | Yes | — | — | missing | No exact NSE equity token found in instrument master for NAGAFERT |
| V2RETAIL | No | Yes | 171.9 | 2026-10-16T00:00:00+05:30 | verified | — |
| SETUINFRA | No | Yes | — | — | missing | Expected exactly one valid NSE ONE_DAY bar for SETUINFRA on 2026-10-16; got 0 |
| GENSOL | No | Yes | 10.44 | 2026-10-16T00:00:00+05:30 | verified | — |
