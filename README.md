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
   - **Total Return (ROI)**: **+2,256.18%** (`$2,356,180.00` final equity from `$100,000.00` initial capital)
   - **Win Rate**: **89.63%** (`908 Wins / 105 Losses across 1,013 trades`)
   - **Profit Factor**: **19.84** | **Estimated Sharpe Ratio**: **3.56**
2. **#1 Best Individual (Non-Combined) Strategy — `INDUSTRY_MOMENTUM` (90 Days)**:
   - **Total Return (ROI)**: **+2,158.16%** (`$2,258,160.00` final equity across 948 trades)
   - **Win Rate**: **89.77%** | **Profit Factor**: **20.29** | **Sharpe Ratio**: **3.59**
3. **#1 Best C-Suite Conviction Strategy — `CONVICTION` (90 Days)**:
   - **Total Return (ROI)**: **+1,150.70%** (`$1,250,698.00` final equity across 503 trades)
   - **Win Rate**: **91.45%** | **Sharpe Ratio**: **3.79**
4. **#1 Highest Risk-Adjusted Sharpe Ratio Strategy — `CSUITE_CLUSTER` (60 Days)**:
   - **Estimated Sharpe Ratio**: **4.78** | **Win Rate**: **95.83%** | **+45.18% ROI** across elite C-Suite coordinated cluster purchases.
5. **#1 Best Executive/Director Cluster Buy Strategy — `CLUSTER_BUY` (90 Days)**:
   - **Total Return (ROI)**: **+446.21%** (`$546,212.00` final equity across 215 trades)
   - **Win Rate**: **84.65%** | **Sharpe Ratio**: **3.02**
6. **Individual Deep-Dive Analysis of Top 4 Performing Strategies**:
   - See [`docs/TOP4_STRATEGIES_INDIVIDUAL_ANALYSIS.md`](docs/TOP4_STRATEGIES_INDIVIDUAL_ANALYSIS.md) for individual trade tables, P&L, trigger reasons, and links to SEC EDGAR Form 4 filings and local datasets.

For full 25-strategy performance tracking and analysis, see [`docs/FULL_DATASET_BACKTEST_PERFORMANCE.md`](docs/FULL_DATASET_BACKTEST_PERFORMANCE.md) or run `python main.py full-backtest`.

For complete methodology and strategy documentation, see [`docs/STRATEGIES.md`](docs/STRATEGIES.md).

---

## 5. Quick Start & Command-Line Interface (CLI)

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

#### 4. Display the Industry Insider Sentiment Heatmap
```bash
# Display 2026 industry sentiment ranking table
python main.py heatmap --days 365

# Output as clean Markdown
python main.py heatmap --days 90 --format markdown
```

#### 5. Scan a Company or Industry for Insider Signals
```bash
python main.py signals --ticker NVDA --min-confidence 75 --year 2026
```

#### 6. Run a Quantitative Strategy Backtest
```bash
# Backtest the Cluster Buy strategy across all industries
python main.py backtest --strategy cluster_buy --show-log

# Backtest C-Suite Conviction Buys on a specific industry
python main.py backtest --strategy conviction --industry semiconductors --holding-days 45
```

#### 7. Update / Collect Insider Trade Datasets by Year
```bash
# Collect current year 2026 trades
python main.py collect --year 2026 --min-market-cap 1000000000

# Collect previous year 2025 trades later
python main.py collect --year 2025 --min-market-cap 1000000000
```

---

## 6. Automated Daily CI/CD & GitHub Actions

The repository includes pre-configured GitHub Actions workflows in `examples/github_workflows/`:
- **`daily_insider_update.yml`**: Scheduled daily cron job (`0 22 * * 1-5`, 10 PM UTC Mon–Fri after market close) that fetches recent Form 4 filings, updates industry trade logs, regenerates the daily industry sentiment heatmap, and commits changes back to the repository.
- **`test_and_lint.yml`**: Automated CI pipeline that executes the full unit and integration test suite (`pytest tests/`) on every push and pull request.

---

## 7. Repository Structure

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
│   │   └── industry_analytics.py # Industry heatmap & sentiment rankings
│   └── universe/                 # NASDAQ & S&P 500 company, CIK & market cap ($1B+) manager
│       └── universe_manager.py   # Ticker-to-CIK mapping & GICS industry filters
├── data/                         # Industry-organized insider trading database
│   ├── universe/                 # Master NASDAQ & S&P 500 universe ($1B+ market cap) CSV/JSON
│   ├── industries/               # Partitioned by Sector -> Industry -> Ticker CSVs (Year 2026)
│   ├── sample_xmls/              # Real SEC Form 4 XML files for testing & demo
│   └── summary_by_industry.csv   # Aggregated cross-industry summary stats
└── tests/                        # Full unit & integration test suite (20+ tests)
```

---

## License
MIT License. See [LICENSE](LICENSE) for details.
