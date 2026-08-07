# Quantitative Insider Trading Strategies: Entries & Exits

This document outlines the quantitative research foundation, signal generation mechanics, and backtesting methodologies implemented in the repository for trading S&P 500 and NASDAQ equities based on insider transactions.

---

## 1. Why Insider Trading Signals Work

Corporate insiders—specifically Executive Officers (CEO, CFO, COO) and Directors—possess deep information advantages regarding their company's operational performance, order pipelines, profit margins, and long-term strategic positioning. 

While academic and industry research shows that **insider selling (`S`) is often noisy** (since executives sell shares for diversification, liquidity, taxes, or scheduled estate planning), **open-market insider buying (`P`) represents an unambiguous signal**: an insider is voluntarily committing personal capital to buy equity on the open market.

---

## 2. Quantitative Entry & Exit Signals Implemented

Our framework evaluates parsed SEC Form 4 open-market transactions (`P` and `S`) and generates standardized trading signals with confidence scores (`0-100%`).

### 2.1 Bullish Entry Signals

#### A. The Cluster Buy Signal (`CLUSTER_BUY`)
- **Definition**: Multiple distinct insiders (at least 2 Executive Officers or Directors) independently buying shares on the open market (Code `P`) within a **14-calendar-day window**.
- **Quantitative Rationale**: A single insider buy could reflect personal optimism, but simultaneous independent purchases across the C-Suite or Board indicate systematic internal conviction.
- **Confidence Scoring**:
  - Baseline score: `75%` for 2 distinct insiders.
  - Adds `10%` for each additional insider (e.g., 3 insiders = `85%`, 4+ = `95%`).
  - Adds `5%` if the CEO or CFO is one of the buyers.

#### B. The C-Suite Conviction Buy Signal (`CONVICTION_BUY`)
- **Definition**: An individual open-market purchase (Code `P`) by the **Chief Executive Officer (CEO)** or **Chief Financial Officer (CFO)** with a total transaction value exceeding **$100,000** (or **$250,000** for large-cap equities).
- **Quantitative Rationale**: CEOs and CFOs have the highest informational visibility into quarterly earnings and cash flows. Substantial capital commitments signal asymmetric upside potential.
- **Confidence Scoring**:
  - `$100k - $250k`: `70%`
  - `$250k - $500k`: `80%`
  - `$500k - $1M`: `90%`
  - `> $1M`: `95%`

#### C. Industry-Wide Insider Heatmap Signal (`INDUSTRY_BULLISH`)
- **Definition**: The net insider buying-to-selling dollar ratio across all tickers in a specific GICS Industry over a **30-day or 90-day window** exceeds **1.5x** (more than $1.50 of insider open-market buying for every $1.00 of discretionary selling).
- **Quantitative Rationale**: Detects macro-level industry bottoms and sector rotation opportunities before institutional analyst upgrades occur.

---

### 2.2 Bearish / Exit Signals

#### A. Heavy Open-Market Selling Exit (`HEAVY_SELL_EXIT`)
- **Definition**: Aggregate open-market selling (Code `S`) by multiple C-Suite officers within a **14-day window** exceeding **$1,000,000** in total value, unsupported by matching option exercises (`M`).
- **Quantitative Rationale**: While routine selling is ignored, heavy coordinated liquidation by executives serves as an effective early exit signal or short trigger.

#### B. Risk Management & Holding Period Exits
In quantitative backtesting, entry signals are paired with systematic exit rules:
1. **Holding Period Exit**: Exit position after `N` trading days (default: `60` days).
2. **Trailing Stop-Loss**: Exit if the equity price drops more than `X%` below the highest peak since entry (default: `10%`).
3. **Signal Reversal Exit**: Exit long position immediately upon triggering a `HEAVY_SELL_EXIT` signal.

---

## 3. Backtesting Methodology & Performance Evaluation

The built-in `BacktestEngine` (`src/strategies/backtest_engine.py`) allows researchers to backtest entry and exit rules across the industry-organized historical Form 4 dataset.

### 3.1 Key Performance Indicators (KPIs)
The engine generates comprehensive performance reports including:
- **Total Return (%)**: Overall capital appreciation over the backtest window.
- **Win Rate (%)**: Percentage of completed trades that closed with a positive net profit.
- **Profit Factor**: Ratio of gross winning dollars to gross losing dollars (`Gross Profit / Gross Loss`).
- **Average Win vs. Average Loss**: Expectancy ratio per trade.
- **Maximum Drawdown (%)**: Largest peak-to-trough decline in portfolio equity.
- **Trade Log**: Detailed execution log showing Ticker, Industry, Entry Date, Entry Signal, Entry Price, Exit Date, Exit Reason, Exit Price, and PnL.

---

## 4. How to Run Backtests via CLI

You can execute quantitative backtests directly from the command line:

```bash
# Backtest the Cluster Buy strategy across all Information Technology semiconductors
python main.py backtest --strategy cluster_buy --industry semiconductors --holding-days 60

# Backtest C-Suite Conviction buys on AAPL or NVDA
python main.py backtest --strategy conviction --ticker NVDA --holding-days 45

# View the cross-industry insider sentiment heatmap
python main.py heatmap --days 90
```
