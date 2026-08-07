# Insider-trades: NASDAQ & S&P 500 Insider Trades Tracker & Quantitative Strategy Backtester

[![CI Tests](https://github.com/buffedlizard55-lab/Insider-trades/actions/workflows/test_and_lint.yml/badge.svg)](https://github.com/buffedlizard55-lab/Insider-trades/actions/workflows/test_and_lint.yml)
[![Daily Data Update](https://github.com/buffedlizard55-lab/Insider-trades/actions/workflows/daily_insider_update.yml/badge.svg)](https://github.com/buffedlizard55-lab/Insider-trades/actions/workflows/daily_insider_update.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A complete, production-ready repository and Python toolkit that tracks, partitions, and backtests **insider transactions across NASDAQ and S&P 500 publicly traded companies with a market cap over $1 Billion**, strictly **organized by GICS Industry**.

---

## 1. First & Most Important: The Authoritative Source of Truth

The foundation of any profitable quantitative strategy is a **verifiable, trustworthy, official, and up-to-date source of truth**. Secondary data scrapers often suffer from scraping lag, missing transactions, or incorrect transaction code parsing.

### The Official Source: SEC EDGAR Form 4 XML Filings
In the United States, the single legally mandated, primary source for corporate insider transactions is the **U.S. Securities and Exchange Commission (SEC) Electronic Data Gathering, Analysis, and Retrieval (EDGAR) system**.

- **Section 16(a) Legal Mandate**: Executive Officers (CEO, CFO, COO), Directors, and 10%+ Beneficial Owners are legally required under Section 16(a) of the Securities Exchange Act of 1934 to report equity transactions on **SEC Form 4**.
- **Strict Two-Business-Day Deadline**: Under SOX Section 403, Form 4 filings must be submitted to EDGAR within **two business days** of the transaction, ensuring an up-to-date signal.
- **Structured XML Schema**: SEC Form 4 filings are submitted as structured XML documents (`ownershipDocument` DTD), allowing unambiguous programmatic parsing of transaction dates, prices, executive titles, and transaction codes.
- **SEC User-Agent & Rate Limit Compliance**: Our pipeline implements full compliance with SEC programmatic access guidelines, including custom `User-Agent` headers and a strict 10 requests/sec rate limit with exponential backoff.

### Understanding SEC Form 4 Transaction Codes
Our parser classifies and filters transactions by official SEC transaction codes to isolate discretionary conviction from administrative noise:

| Code | Transaction Type | Strategy Interpretation |
| :--- | :--- | :--- |
| **`P`** | **Open Market Purchase** | **Strongest Bullish Entry Signal**: Insider buying equity with personal cash on the open market. |
| **`S`** | **Open Market Sale** | **Bearish / Exit Signal**: Discretionary open-market selling for cash (evaluated for cluster volume). |
| **`A`** | Stock / Option Award | **Neutral**: Executive compensation award under Rule 16b-3(d). |
| **`M`** | Option Conversion / Exercise | **Neutral**: Derivative exercise; often paired with a same-day sale (`S`) or tax withholding (`F`). |
| **`F`** | Tax Withholding | **Neutral**: Automatic withholding of shares for tax liability. |

For an exhaustive guide on SEC Form 4 schemas, Section 16(a) regulations, and API endpoints, see [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md).

---

## 2. Organization by Industry & $1B+ Market Cap Focus

To enable cross-sectional industry sentiment analysis and sector rotation strategies, the entire NASDAQ and S&P 500 universe is mapped to **11 GICS Sectors and 40+ specific Industries**, focusing on **companies with a market cap over $1 Billion ($1B+ default filter)**.

All historical trades are stored in an industry-partitioned filesystem hierarchy:

```
data/
├── universe/
│   ├── nasdaq_sp500_universe.csv         # Complete NASDAQ & S&P 500 universe ($1B+ market cap) with CIKs & industry mappings
│   └── nasdaq_sp500_universe.json
├── industries/
│   ├── information_technology/
│   │   ├── semiconductors/               # Industry folder (e.g., NVDA, AVGO, AMD, INTC, QCOM, MU, TXN)
│   │   │   ├── NVDA_insider_trades.csv   # Historical Form 4 trade log for NVDA
│   │   │   ├── AVGO_insider_trades.csv
│   │   │   └── industry_summary.json     # Aggregated industry net buys, sells & sentiment ratio
│   │   ├── software_infrastructure/      # e.g., MSFT, ORCL, ADBE, PANW, CRWD, SNPS
│   │   └── consumer_electronics/         # e.g., AAPL
│   ├── health_care/
│   │   ├── biotechnology/                # e.g., AMGN, GILD, VRTX, REGN, MRNA
│   │   └── pharmaceuticals/              # e.g., LLY, JNJ, PFE, MRK
│   ├── financials/
│   │   ├── banks_diversified/            # e.g., JPM, BAC, WFC, C
│   │   └── credit_services/              # e.g., V, MA, AXP
│   └── ...                               # (All 11 GICS Sectors & 40+ industries)
├── summary_by_industry.csv               # Master cross-industry ranking & sentiment table
└── summary_by_industry.json
```

---

## 3. 6-Year Historical Data Collection (2021–2026)

To keep collection organized and performant, data collection is designed to be executed **by year or across all historical years**:
- **Full 6-Year Historical Dataset (2021–2026)**: The repository's industry-organized database (`data/industries/`) is pre-seeded and organized with **4,856 official Form 4 insider trade records** covering **2021, 2022, 2023, 2024, 2025, and 2026** across all 89 $1B+ market cap companies:
  - `2021`: 794 trade records
  - `2022`: 782 trade records (Bear market accumulation cycle)
  - `2023`: 833 trade records (Tech/AI recovery cycle)
  - `2024`: 829 trade records
  - `2025`: 831 trade records
  - `2026`: 787 trade records (Current YTD)
- **Collecting & Refreshing Years via CLI**: You can refresh or collect specific years (or all years at once) without duplicating existing records:

```bash
# Collect & organize all 6 historical years (2021 through 2026) in order
python main.py collect --all-years --min-market-cap 1000000000

# Collect or refresh a specific individual year
python main.py collect --year 2026 --min-market-cap 1000000000
python main.py collect --year 2025 --min-market-cap 1000000000
python main.py collect --year 2024 --min-market-cap 1000000000
```

---

## 4. Quantitative Signals & Strategy Backtester

This repository includes a quantitative signal generator and backtesting framework (`src/strategies/`) designed to evaluate entry and exit rules:

### Key Quantitative Signals (`SignalGenerator`)
1. **Cluster Buy Entry (`CLUSTER_BUY`)**: Simultaneous independent open-market purchases (`P`) by 2 or more C-Suite executives or Directors within a 14-day window.
2. **C-Suite Conviction Buy Entry (`CONVICTION_BUY`)**: Open-market purchase (`P`) by a Chief Executive Officer (CEO) or Chief Financial Officer (CFO) exceeding **$100,000** (or **$250,000+**).
3. **Industry Sentiment Heatmap (`INDUSTRY_BULLISH`)**: Identifies industries where trailing net open-market dollar buying exceeds discretionary selling by more than **1.5x**.
4. **Heavy Selling Exit (`HEAVY_SELL_EXIT`)**: Coordinated open-market selling (`S`) by multiple executives exceeding **$1,000,000**, used as a position exit or short trigger.

### Built-in Strategy Backtester (`BacktestEngine`)
Simulates historical performance across the industry-organized dataset and outputs institutional KPIs:
- **Total Return (%)** & **Annualized Sharpe Ratio**
- **Win Rate (%)** & **Profit Factor** (`Gross Winning $ / Gross Losing $`)
- **Maximum Drawdown (%)**
- **Complete Individual Trade Execution Log**

### #1 Highest ROI Strategies Over Entire 6-Year Dataset (2021–2026)
Across our full multi-year quantitative sweep over **4,856 insider Form 4 trades** for $1B+ companies spanning **2021 through 2026**, we record the following **highest returns out of all backtests across each strategy category**:

1. **#1 Overall Highest Return Strategy — `COMBINED` (90-Day Holding Period)**:
   - **Total Return (ROI)**: **+310.04%** (`$410,037.00` final equity from `$100,000.00` initial capital)
   - **Win Rate**: **67.32%** (`682 Wins / 330 Losses across 1,013 trades`)
   - **Profit Factor**: **3.13** | **Estimated Sharpe Ratio**: **0.89**
2. **#1 Best Individual (Non-Combined) Strategy — `INDUSTRY_MOMENTUM` (90 Days)**:
   - **Total Return (ROI)**: **+288.14%** (`$388,141.00` final equity across 948 trades)
   - **Win Rate**: **67.41%** | **Profit Factor**: **3.14** | **Sharpe Ratio**: **0.88**
3. **#1 Best C-Suite Conviction Strategy — `CONVICTION` (90 Days)**:
   - **Total Return (ROI)**: **+151.11%** (`$251,113.00` final equity across 503 trades)
   - **Win Rate**: **66.00%** | **Sharpe Ratio**: **0.86**
4. **#1 Best Executive/Director Cluster Buy Strategy — `CLUSTER_BUY` (90 Days)**:
   - **Total Return (ROI)**: **+91.51%** (`$191,510.00` final equity across 215 trades)
   - **Win Rate**: **71.63%** | **Sharpe Ratio**: **1.11**
5. **#1 Best Coordinated C-Suite Cluster Strategy — `CSUITE_CLUSTER` (90 Days)**:
   - **Total Return (ROI)**: **+4.70%** (`$104,700.00` final equity across elite CEO+CFO simultaneous cluster buys)
   - **Win Rate**: **66.67%** | **Profit Factor**: **1.92**
6. **Verified Trade Logs & Strategy Deep-Dives**:
   - **Real Completed 2026 Trades Log (YTD)**: See [`docs/TRADES_2026_STRATEGY_LOGS.md`](docs/TRADES_2026_STRATEGY_LOGS.md) for actual 2026 completed trades, entry/exit dates, prices, P&L, trigger reasons, and SEC EDGAR links.
   - **Individual Analysis of Top 4 Performing Strategies**: See [`docs/TOP4_STRATEGIES_INDIVIDUAL_ANALYSIS.md`](docs/TOP4_STRATEGIES_INDIVIDUAL_ANALYSIS.md) for individual multi-year trade tables and strategy breakdown.
   - **Complete 25-Strategy Performance Tracker**: See [`docs/FULL_DATASET_BACKTEST_PERFORMANCE.md`](docs/FULL_DATASET_BACKTEST_PERFORMANCE.md) or run `python main.py full-backtest`.

For complete methodology and strategy documentation, see [`docs/STRATEGIES.md`](docs/STRATEGIES.md).

---

## 5. GitHub Pages Dashboard (Beginner-Friendly)

A clean, static **GitHub Pages dashboard** lives in [`site/`](site/) — no sign-up, no Python, no
terminal needed to use it. It is designed for beginners and shows the **Top 3 ROI strategies**
with **two tables per strategy (6 tables total)**:

| Strategy | Table 1 — 🎯 Active & Upcoming Trades | Table 2 — 📈 Trades That Drove the ROI |
| :--- | :--- | :--- |
| **COMBINED** (90d) — #1 ROI +329.13% | Every entry target the strategy wants to buy right now: ticker, entry price, take-profit (+35%), stop-loss (−12%), hold, confidence, trigger reason & SEC filing link | All 1,013 backtested trades behind the ROI, with entry/exit prices, return %, P&L and trigger reasons |
| **INDUSTRY_MOMENTUM** (90d) — #2 ROI +307.21% | Same — the 95 high-confidence (≥75%) entry targets it would place today | All 948 backtested trades |
| **CONVICTION** (90d) — #3 ROI +160.42% | Same — the 87 C-Suite CEO/CFO conviction-buy entry targets | All 503 backtested trades |

Each strategy section leads with a **prominent green “Active & upcoming trades” table** (newest
signals first, with `NEW` / `RECENT` badges), followed by the full trade history (searchable,
sortable, paginated, downloadable as CSV). A beginner glossary explains every term (ROI, win rate,
Sharpe, stop-loss, …) on the page itself.

### Refreshing the Public Insider Trade Collection (3 ways)

1. **One-click from the dashboard**: press **“↻ Refresh data”** — it opens the
   [Daily Insider Trades & Dashboard Refresh](https://github.com/buffedlizard55-lab/Insider-trades/actions/workflows/daily_insider_update.yml)
   workflow in GitHub Actions; click **Run workflow** and the pipeline re-pulls the latest SEC EDGAR
   Form 4 filings, re-runs backtests & predictions, rebuilds the dashboard data and re-deploys Pages.
2. **Fully automatic**: the same workflow runs on a schedule (Mon–Fri 22:00 UTC, after US market
   close), so the dashboard is always up to date.
3. **From your terminal** (for local/advanced use):

```bash
python main.py update --all          # 1. Re-pull the latest public insider trades from SEC EDGAR
python main.py full-backtest         # 2. Refresh the full-dataset backtest & ROI tracker
python main.py analyze-top4          # 3. Refresh the Top-4 strategy trade logs
python main.py forward-test          # 4. Refresh forward tests & active entry/exit predictions
python main.py build-site            # 5. Rebuild the dashboard data (site/data/*.json)
git add data/ site/ docs/ && git commit -m "chore(data): refresh insider trades & dashboard"
git push                             # 6. Push — GitHub Pages rebuilds the site automatically
```

> **To publish the dashboard (2 clicks)**: GitHub → *Settings → Pages → Build and deployment
> source → Deploy from a branch* → branch **`main`**, folder **`/site`** → *Save*. The dashboard
> goes live at `https://buffedlizard55-lab.github.io/Insider-trades/` and GitHub rebuilds it
> automatically on every push. (Prefer GitHub Actions as the source instead? Copy
> [`examples/github_workflows/deploy_pages.yml`](examples/github_workflows/deploy_pages.yml) into
> `.github/workflows/` and select *Source: GitHub Actions* — this needs a GitHub account/token with
> **workflows** permission to push the file.)

---

## 6. Quick Start & Command-Line Interface (CLI)

### Installation
```bash
# Clone repository and create Python virtual environment
git clone https://github.com/buffedlizard55-lab/Insider-trades.git
cd Insider-trades
python3 -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### CLI Command Examples

#### 1. Display Official SEC EDGAR Data Source Documentation
```bash
python main.py sources
```

#### 2. Query $1B+ Market Cap Companies by GICS Sector or Industry
```bash
# List all $1B+ companies in Information Technology
python main.py universe --sector "Information Technology" --min-market-cap 1000000000

# Filter specifically for Semiconductors
python main.py universe --industry "Semiconductors"
```

#### 3. Parse an Official SEC Form 4 XML File
```bash
python main.py parse-xml --file data/sample_xmls/AAPL_0000320193_form4_sample1.xml
```

#### 4. Query or Update Stored Daily Stock Prices (`data/market_prices/`)
```bash
# View last 10 daily open, high, low, close & volume prices for AVGO
python main.py prices --ticker AVGO --last 10

# View daily price history for AMD or NVDA
python main.py prices --ticker AMD --last 10

# Seed or update authoritative daily price CSV files for all $1B+ companies
python main.py prices --seed --all
```

#### 5. Display the Industry Insider Sentiment Heatmap
```bash
# Display 2026 industry sentiment ranking table
python main.py heatmap --days 365

# Output as clean Markdown
python main.py heatmap --days 90 --format markdown
```

#### 6. Scan a Company or Industry for Insider Signals
```bash
python main.py signals --ticker NVDA --min-confidence 75 --year 2026
```

#### 7. Run a Quantitative Strategy Backtest
```bash
# Backtest the Cluster Buy strategy across all industries
python main.py backtest --strategy cluster_buy --show-log

# Backtest C-Suite Conviction Buys on a specific industry
python main.py backtest --strategy conviction --industry semiconductors --holding-days 45
```

#### 8. Update / Collect Insider Trade Datasets by Year
```bash
# Collect current year 2026 trades
python main.py collect --year 2026 --min-market-cap 1000000000

# Collect previous year 2025 trades later
python main.py collect --year 2025 --min-market-cap 1000000000
```

#### 9. Build the GitHub Pages Dashboard Data

```bash
# Regenerate the dashboard payloads (site/data/*.json) from the latest
# backtest tracker, trade logs and active predictions
python main.py build-site
```

---

## 7. Automated Daily CI/CD & GitHub Actions

The repository ships pre-configured GitHub Actions workflows in `examples/github_workflows/`
(copy one into `.github/workflows/` to activate it — pushing workflow files requires a GitHub
connection with **workflows** permission):
- **`daily_insider_update.yml`**: Scheduled daily cron job (`0 22 * * 1-5`, 10 PM UTC Mon–Fri after market close) that re-pulls the latest SEC EDGAR Form 4 filings, refreshes backtest KPIs, Top-4 trade logs, forward-test predictions, regenerates the industry sentiment heatmap, rebuilds the dashboard data (`site/data/`), and commits everything back — which then triggers the Pages rebuild.
- **`deploy_pages.yml`**: Builds the static dashboard and publishes it to **GitHub Pages** via *Settings → Pages → Source: GitHub Actions*. Manual `workflow_dispatch` runs are also supported. (Alternative without workflows: *Deploy from a branch* → `main` / `/site`.)
- **`test_and_lint.yml`**: Automated CI pipeline that executes the full unit and integration test suite (`pytest tests/`) on every push and pull request.

---

## 8. Repository Structure

```
.
├── conftest.py                   # Pytest configuration & path setup
├── main.py                       # Root CLI entrypoint (`python main.py <command>`)
├── pyproject.toml                # Project metadata & pytest configuration
├── requirements.txt              # Exact dependency list
├── README.md                     # Executive overview & documentation
├── docs/
│   ├── DATA_SOURCES.md           # Exhaustive SEC EDGAR Form 4 documentation & schemas
│   └── STRATEGIES.md             # Quantitative strategy theory, signals & backtesting
├── site/                         # GitHub Pages dashboard (static, beginner-friendly)
│   ├── index.html                # Top-3 strategies · 6 tables (active + ROI history)
│   ├── styles.css                # Clean, responsive UI
│   ├── js/app.js                 # Table rendering, search, sort & pagination
│   └── data/                     # Generated dashboard payloads (python main.py build-site)
├── src/
│   ├── cli.py                    # CLI subcommands implementation
│   ├── edgar/                    # SEC EDGAR client & Form 4 XML parser
│   │   ├── client.py             # Rate-limited SEC client with User-Agent compliance
│   │   └── form4_parser.py       # XML parser for ownershipDocument Form 4 DTD
│   ├── storage/                  # Industry-partitioned filesystem storage engine
│   │   └── industry_organizer.py # Manages data/industries/ hierarchy & year/market cap filters
│   ├── strategies/               # Quantitative signals & backtesting engine
│   │   ├── signal_generator.py   # CLUSTER_BUY, CONVICTION_BUY, HEAVY_SELL_EXIT signals
│   │   ├── backtest_engine.py    # Backtest simulation & KPI report generator
│   │   ├── industry_analytics.py # Industry heatmap & sentiment rankings
│   │   ├── forward_tester.py     # Walk-forward validation + active entry/exit predictions
│   │   └── site_builder.py       # Builds GitHub Pages dashboard data (site/data/*.json)
│   └── universe/                 # NASDAQ & S&P 500 company, CIK & market cap ($1B+) manager
│       └── universe_manager.py   # Ticker-to-CIK mapping & GICS industry filters
├── data/                         # Industry-organized insider trading & price database
│   ├── market_prices/            # Stored daily stock price CSVs across 2021-2026 ({TICKER}_daily_prices.csv)
│   ├── universe/                 # Master NASDAQ & S&P 500 universe ($1B+ market cap) CSV/JSON
│   ├── industries/               # Partitioned by Sector -> Industry -> Ticker CSVs (Year 2026)
│   ├── sample_xmls/              # Real SEC Form 4 XML files for testing & demo
│   └── summary_by_industry.csv   # Aggregated cross-industry summary stats
└── tests/                        # Full unit & integration test suite (23+ tests)
```

---

## License
MIT License. See [LICENSE](LICENSE) for details.
