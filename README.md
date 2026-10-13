# Experiment with Cash — Vertex Paper Trading

A fully unattended **paper-only** Indian stock screener portfolio. The scanner is [vertex-signal-lue-line](https://chartink.com/screener/vertex-signal-lue-line); no live brokerage orders and no need to open ChatGPT every day.

## View current trades directly on GitHub

- **[Verified scanner symbols and retrieval status](SCANNER_SYMBOLS.md)**
- **[Active positions — live Markdown table](ACTIVE_TRADES.md)**
- **[Closed trades and profit history](TRADE_HISTORY.md)**
- [Latest machine-readable dashboard data](docs/data/report.json)

These GitHub tables do not require GitHub Pages. They update when GitHub Actions completes a run. If the workflow is disabled or has not run, data remains unchanged.

## Dashboard

Open the source at [docs/index.html](docs/index.html). To publish as a website, in GitHub select **Settings → Pages → Deploy from a branch → main → /docs → Save**. Once Pages finishes publishing, the public dashboard URL will follow the pattern \`https://rahulrtk74747474-glitch.github.io/Experiment-with-cash/\`. This URL is not live until Pages is enabled. The browser fetches its JSON from \`docs/data/report.json\`, updated by GitHub Actions.

Shows portfolio equity curve, portfolio drawdown chart, realised/unrealised P&L chart, symbol P&L chart, tables of open positions, closed trade history, buy/ignored/skip events, CSV exports, max unrealised profit and maximum position drawdown.

## Automated schedule

[GitHub Actions workflow](.github/workflows/vertex-paper-trading.yml) runs **Monday–Friday at 3:29 PM IST** (\`59 9 * * 1-5\` UTC). The workflow also supports **Actions → Vertex Paper Trading → Run workflow** and runs once on code pushes. GitHub **does not guarantee exact cron execution time**: scheduled jobs can start late or be skipped when GitHub is congested. The system allows a delayed session attempt until 6 PM IST and accepts only prices from the current NSE trading session.

To do a manual run **outside market hours**, use **Actions → Vertex Paper Trading → Run workflow**. This attempts to capture the current scanner list at run time and values it using the latest completed NSE weekday's Yahoo price observations; it does not pretend these are 3:29 PM trades placed today. If scanner output or dated prices cannot be verified, it fails safely rather than making up holdings. If markets are open, wait until the current session ends before manually capturing a completed-session snapshot. 

A fresh clone works as-is: GitHub-hosted runner installs Python dependencies and Chromium for Chartink's newer JavaScript UI. Workflow needs GitHub Actions enabled and **Read/write permissions** for \`GITHUB_TOKEN\` (workflow requests \`contents: write\`). It commits portfolio state after every run. **Do not delete** \`data/state.json\`.

## Position accounting

- Initial simulated cash: **₹100,000**. Never use margin. No real brokerage execution.
- Every selected NSE stock gets **integer whole shares**, costing **≤ ₹5,000**, also bounded by available cash. No borrowing. If there are more than 20 matches, first symbols returned by the scanner take precedence.
- Buy signals are de-duplicated inside the same day.
- Example: Monday initial BUY, Tuesday same symbol **IGNORE**, Wednesday same symbol **SELL then BUY again** (a new, max-₹5k position), Thursday **IGNORE**. This is a rollover, not an additional buy beyond ₹5k. The fresh buy price resets P&L and the 3-session timer.
- A holding expires after **three subsequently processed NSE trading sessions** without a qualifying repeat. Thus a Monday buy with no repeats exits Thursday, not calendar Wednesday. NSE holidays/non-working days don't increment the counter if no verified price-and-scan session completes.
- Each successful session marks every open position to a fresh Yahoo Finance NSE minute-close price, independently of whether today's Chartink screener contains it. Max unrealised profit and max peak-to-trough drawdown update on those **observed prices** only, **not tick-by-tick/intraday extrema**. Portfolio drawdown also uses daily observed equity snapshots.
- The system records amounts and returns **before brokerage fees, taxes and slippage**; zero fees are assumed. Scan results and quote timestamps can be delayed, and 3:29 PM is not necessarily the real close or executable bid/ask.
- A Chartink login-wall/block, malformed JSON or lack of a fresh quote for an existing holding **aborts the day's simulation** with an error rather than converting data absence into sell/buy signals. New signals without a Yahoo quote are skipped.

## Files

| Path | Purpose |
|---|---|
| \`src/market.py\` | Fetch saved Chartink scan (session CSRF + Chromium fallback), Yahoo NSE quotes |
| \`src/engine.py\` | Deterministic buy/ignore/rollover/expiry, cash and P&L accounting |
| \`src/run.py\` | Trade-session orchestration, fail-safe state/report persistence |
| \`data/state.json\` | **Source of truth** for wallet, positions, trade ledger and sessions |
| \`docs/data/report.json\` | Dashboard view of the latest stored state |
| \`docs/index.html\` | Mobile/tablet-friendly dashboard with tables and charts |
| \`tests/test_engine.py\` | Repeat signal, expiry, MDD and risk-limit unit tests |

## Manual check

\`\`\`bash
pip install -r requirements.txt playwright
python -m playwright install chromium
python -m unittest discover -s tests -v
python -m src.run
\`\`\`

If your saved Chartink scan relies on a **private/custom indicator**, public scraping may not be sufficient. Do not assume a successful run without the GitHub Actions log confirming the data was fetched. Scraping is best-effort and may require Chartink account authorization or an officially supported data feed if access changes.

**Educational demo only, not trading advice.**

## Separate-repository scraper reuse (October 2026)

This project **does not fetch from, commit to, dispatch, or depend on** the
\`Scraping_and_testing\` repository at runtime. Its working browser-based scanner
was copied into \`src/chartink_browser.py\` as a standalone module, then adapted
to **this project's** \`vertex-signal-lue-line\` scanner and its own trade rules.
The other repository's scanner URL, ₹10,000 sizing, workflows, state and trades
are not imported.

The scraper opens the scan in headless Chromium, authenticates when needed,
reads the actual results-grid Symbol/Close/Volume cells and follows pagination.
Chartink's **Backtest "matched 0 stocks" text is not treated as evidence
that the live stock-result grid is empty**.

In this repository only, under **Settings → Secrets and variables → Actions**,
add either \`CHARTINK_COOKIE\` or \`CHARTINK_USER\` and
\`CHARTINK_PASSWORD\` if the scanner requires authentication. Secrets from
the separate repository are **not shared automatically**. Never commit
credentials to a public file.

**Price policy:** current scanner matches use the fetched scanner's displayed
Close as a paper observation with its actual fetch time; held stocks absent from
today's scan are valued using a dated Yahoo Finance minute quote. The
simulated trade date may be the prior completed market session when a manual
night-time run is requested; this is explicitly a retrospective paper
snapshot, **not a claim that an order was executed at that earlier time**.

The [scanner result table](SCANNER_SYMBOLS.md) publishes each parsed symbol,
stock name, scanner Close, percent change, and volume from a verified fetch.
Entries and exits follow the separately implemented ₹5,000-per-stock and
three-session rules. A missing or blocked scanner leaves prior trades unchanged.

**Execution status:** Code pushed via a GitHub integration does not guarantee
GitHub Actions will start. Verify actual runs under the
[Actions tab](../../actions). A manual workflow_dispatch run can be started
there; without any recorded run the system still shows an empty demo ledger.

## Scanner troubleshooting and proof of retrieval

The app first tries a Chartink session with CSRF/XSRF credentials and a form-encoded POST. If that fails, Chromium captures the scanner network response; for sites rendering tables without the legacy endpoint, it looks for a table with explicit **Symbol** and **Close** headers. See [source](src/market.py).

The updated [scanner symbol table](SCANNER_SYMBOLS.md) distinguishes a verified result from a failed fetch. Data at [latest_scan.json](docs/data/latest_scan.json) includes the URL, timestamp, result count, status and the exact symbols. A successfully fetched scanner list can be published even if Yahoo Finance cannot price a particular stock. An error never silently means zero matches. The four symbols in the user screenshot are used in [offline regression tests](tests/test_market.py) only; they are not treated as a live result.

**To verify:** open [Actions](../../actions), enable Actions if required, and run **Vertex Paper Trading - 3:29 PM IST → Run workflow**. Check logs for Chartink failures. The linked table updates only after the workflow has executed and committed data; merely adding code does not mean it has run.
