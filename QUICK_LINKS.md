# Experiment with Cash — All Important Links

> **Paper trading only.** These are simulated trades, not brokerage orders.
>
> **Last verified result:** Run #1 completed successfully at 02:01 AM IST on 14 October 2026, capturing **8 Chartink scanner symbols** and recording **8 active demo positions**. This information is a snapshot; use the live data links below for future updates.

## Main control centre

| Purpose | Link | What to do |
| --- | --- | --- |
| Repository | [Experiment-with-cash](https://github.com/rahulrtk74747474-glitch/Experiment-with-cash) | Source code and files |
| **Run scanner now** | [Vertex Paper Trading workflow](https://github.com/rahulrtk74747474-glitch/Experiment-with-cash/actions/workflows/vertex-paper-trading.yml) | Tap **Run workflow**, select **main**, tap green **Run workflow** |
| All workflow executions | [Actions history](https://github.com/rahulrtk74747474-glitch/Experiment-with-cash/actions) | Check success, warnings, failures |
| First verified successful run | [Run #1](https://github.com/rahulrtk74747474-glitch/Experiment-with-cash/actions/runs/38463353965) | Full logs and test results |
| **Active simulated trades** | [ACTIVE_TRADES.md](ACTIVE_TRADES.md) | Current positions and unrealised profit |
| **Angel One daily-close verification** | [PRICE_CHECK.md](PRICE_CHECK.md) | All scanned stocks + held stocks; verified NSE daily closes and missing prices |
| **Latest Chartink symbols** | [SCANNER_SYMBOLS.md](SCANNER_SYMBOLS.md) | Verified stock symbols, scanner close, change and volume |
| Closed trade history | [TRADE_HISTORY.md](TRADE_HISTORY.md) | Completed transactions and realised profit |
| Portfolio machine-readable report | [report.json](docs/data/report.json) | Full summary, charts data and all trades |
| Scanner machine-readable snapshot | [latest_scan.json](docs/data/latest_scan.json) | Last fetch, count, symbols and source |
| Trading state | [state.json](data/state.json) | Authoritative paper portfolio state |
| Dashboard HTML source | [docs/index.html](docs/index.html) | Actual graphical dashboard source code |
| **Graphical dashboard website** | [GitHub Pages](https://rahulrtk74747474-glitch.github.io/Experiment-with-cash/) | Requires a successful publishing deployment |
| **Publish graphical dashboard** | [Publish Trading Dashboard workflow](https://github.com/rahulrtk74747474-glitch/Experiment-with-cash/actions/workflows/deploy-dashboard.yml) | **Run workflow** after enabling Pages; automatically republishes after trading runs |
| **Enable dashboard website** | [Pages Settings](https://github.com/rahulrtk74747474-glitch/Experiment-with-cash/settings/pages) | Choose **Build and deployment → Source: GitHub Actions** |
| Actions settings | [Actions Settings](https://github.com/rahulrtk74747474-glitch/Experiment-with-cash/settings/actions) | Check Actions permissions if a workflow cannot start |
| Main setup and trading rules | [README.md](README.md) | Strategy, constraints, authentication |

## How to run the scanner manually

1. Open [Vertex Paper Trading](https://github.com/rahulrtk74747474-glitch/Experiment-with-cash/actions/workflows/vertex-paper-trading.yml).
2. Click **Run workflow** on the workflow page (not the three-dot **Create status badge** menu).
3. Select `main` and click the green **Run workflow** button.
4. Open [Actions](https://github.com/rahulrtk74747474-glitch/Experiment-with-cash/actions) and check the new run; open its `simulate` job if any step fails.
5. After completion, read [Scanner Symbols](SCANNER_SYMBOLS.md) for the **actual verified symbol count**, and [Active Trades](ACTIVE_TRADES.md) for simulated trades.

## Schedule, behavior and safety

The workflow has a primary run at **3:51 PM India time, Monday–Friday**, and fallback attempts at **4:11 PM, 4:41 PM and 5:11 PM IST**. These are retry opportunities, not additional simulated trading sessions; the engine applies each NSE session only once. GitHub's scheduled execution can start late or be dropped. On every run, Playwright/Chromium opens the Chartink `vertex-signal-lue-line` scanner and records the results. It processes trades only in an eligible session or a manual retrospective paper snapshot. Missing browser access results in an error and does **not** mean zero matched stocks.

Chartink login secrets (if needed) must be set separately in **this** repository. `Scraping_and_testing` remains a separate repository and is not modified by these workflows.

The graphical website works only after Pages is enabled under **Source: GitHub Actions** and the **Publish Trading Dashboard** workflow finishes successfully. Afterwards it automatically republishes when the trading workflow completes. The active trades and scanner Markdown tables can always be viewed on GitHub.

Updated links index: 14 October 2026.

## Daily NSE close price policy

Chartink is used for **stock symbols only**. All prices for simulated
BUY, SELL, daily valuation and trade exits now come exclusively from
Angel One SmartAPI **NSE ONE_DAY** candles. No Yahoo or Chartink price
is substituted. The complete scanner-stock price check is in
[PRICE_CHECK.md](PRICE_CHECK.md) and
[latest_prices.json](docs/data/latest_prices.json).

Trading is scheduled after the market has closed, starting at
**3:51 PM IST, Monday–Friday**, with backups at
**4:11, 4:41 and 5:11 PM IST**. The workflow will stop rather than
invent a quote for a held position. Code-push executions outside the
market window test prices but do not alter demo trades.

**Note:** Angel API secrets are encrypted repository Actions secrets
and are never printed or copied to another repository.
