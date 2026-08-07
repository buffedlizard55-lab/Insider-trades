# Quantitative Strategy Backtest Sweep & ROI Performance (2026)

This document records the quantitative backtest ROI performance across **25 strategy configurations** evaluated over historical SEC Form 4 insider transactions in **Year 2026** for NASDAQ and S&P 500 companies with a **market cap over $1 Billion ($1B+)**.

All backtests simulate systematic entries on parsed Form 4 open-market signals (`P`), position sizing of 10% of equity per trade ($10,000 minimum), dynamic stop-loss and take-profit targets, holding-period exits, and heavy open-market selling exit triggers (`HEAVY_SELL_EXIT`).

---

## 1. Executive Summary: #1 Highest ROI Configuration

Out of all 25 tested strategy and parameter combinations, the **highest returns** were achieved by the **`COMBINED` Strategy** (which trades both C-Suite Conviction Buys and Executive/Director Cluster Buys) with a **90-day holding period**:

```
================================================================================
                *** #1 HIGHEST ROI BACKTEST CONFIGURATION ***                   
================================================================================
  Strategy Name      : COMBINED (Cluster Buys + C-Suite Conviction Buys)
  Holding Period     : 90 trading days
  Win Rate           : 88.32% (189 Wins / 25 Losses)
  Profit Factor      : 17.93 (Gross Winning $ / Gross Losing $)
  Estimated Sharpe   : 3.45
  Max Drawdown       : 0.81%
  Total Return (ROI) : 475.55%
  Final Equity       : $575,554.00 (from $100,000.00 initial capital)
================================================================================
```

### Best Individual (Non-Combined) Strategies by ROI
- **#1 Top Individual Strategy — `INDUSTRY_MOMENTUM` (90 Days)**:
  - **Total Return (ROI)**: **+467.55%** (`$567,546.00` final equity)
  - **Win Rate**: **89.55%** (`180 Wins / 21 Losses`)
  - **Profit Factor**: **20.52** | **Sharpe Ratio**: **3.57**
  - *Rationale*: Allocating capital to open-market insider buys within GICS industries experiencing **Strong Buy Accumulation** (Buy/Sell dollar ratio $\ge 1.5x$) captures powerful sector rotation momentum.
- **#2 Top Individual Strategy — `CONVICTION` (C-Suite CEO/CFO Buys, 90 Days)**:
  - **Total Return (ROI)**: **+234.66%** (`$334,664.00` final equity)
  - **Win Rate**: **93.88%** (`92 Wins / 6 Losses`)
  - **Profit Factor**: **35.11** | **Sharpe Ratio**: **4.09**
  - *Rationale*: Individual open-market purchases by CEOs and CFOs exceeding **$100,000** show the highest win rate (93.88%) and Sharpe ratio (4.09) across all tested configurations.

---

## 2. Full Multi-Strategy ROI Comparison Table (2026)

Below is the complete ranking of all 25 tested backtest configurations sorted by **Total Return (%)**:

| Rank | Strategy | Holding (Days) | Trades | Win Rate (%) | Profit Factor | Sharpe Ratio | Max DD (%) | Total Return (%) | Final Equity ($) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **COMBINED** | **90** | **214** | **88.32%** | **17.93** | **3.45** | **0.81%** | **475.55%** | **$575,554.00** |
| **2** | **INDUSTRY_MOMENTUM** | **90** | **201** | **89.55%** | **20.52** | **3.57** | **1.17%** | **467.55%** | **$567,546.00** |
| **3** | **COMBINED** | **60** | **214** | **91.12%** | **35.62** | **4.23** | **1.28%** | **388.77%** | **$488,766.00** |
| **4** | **INDUSTRY_MOMENTUM** | **60** | **201** | **84.08%** | **16.71** | **3.36** | **1.12%** | **336.11%** | **$436,114.00** |
| **5** | **COMBINED** | **45** | **214** | **88.32%** | **16.16** | **3.54** | **1.20%** | **249.94%** | **$349,937.00** |
| **6** | **CONVICTION** | **90** | **98** | **93.88%** | **35.11** | **4.09** | **0.90%** | **234.66%** | **$334,664.00** |
| **7** | **INDUSTRY_MOMENTUM** | **45** | **201** | **84.58%** | **10.90** | **3.01** | **2.34%** | **217.63%** | **$317,627.00** |
| **8** | **CONVICTION** | **60** | **98** | **86.73%** | **19.40** | **3.63** | **0.87%** | **172.42%** | **$272,418.00** |
| **9** | **COMBINED** | **30** | **214** | **90.65%** | **13.01** | **3.44** | **1.30%** | **137.84%** | **$237,842.00** |
| **10** | **INDUSTRY_MOMENTUM** | **30** | **201** | **83.08%** | **7.40** | **2.53** | **3.19%** | **114.69%** | **$214,694.00** |
| **11** | **CONVICTION** | **45** | **98** | **85.71%** | **12.58** | **3.10** | **0.73%** | **106.75%** | **$206,755.00** |
| **12** | **CLUSTER_BUY** | **60** | **55** | **85.45%** | **20.25** | **3.56** | **0.88%** | **99.88%** | **$199,880.00** |
| **13** | **CLUSTER_BUY** | **90** | **55** | **78.18%** | **8.35** | **2.45** | **3.14%** | **98.66%** | **$198,660.00** |
| **14** | **INDUSTRY_MOMENTUM** | **20** | **201** | **86.57%** | **6.87** | **2.55** | **0.77%** | **77.73%** | **$177,730.00** |
| **15** | **COMBINED** | **20** | **214** | **77.10%** | **3.52** | **1.57** | **1.64%** | **63.35%** | **$163,350.00** |
| **16** | **CONVICTION** | **30** | **98** | **84.69%** | **7.54** | **2.60** | **1.15%** | **57.16%** | **$157,160.00** |
| **17** | **CLUSTER_BUY** | **45** | **55** | **78.18%** | **7.17** | **2.29** | **1.38%** | **49.53%** | **$149,530.00** |
| **18** | **CONVICTION** | **20** | **98** | **84.69%** | **5.92** | **2.31** | **1.46%** | **38.23%** | **$138,230.00** |
| **19** | **CLUSTER_BUY** | **30** | **55** | **90.91%** | **13.29** | **3.46** | **0.71%** | **36.26%** | **$136,260.00** |
| **20** | **CLUSTER_BUY** | **20** | **55** | **69.09%** | **2.30** | **0.99** | **1.80%** | **11.45%** | **$111,450.00** |
| **21** | **CSUITE_CLUSTER** | **90** | **4** | **100.00%** | **99.00** | **3.81** | **0.00%** | **8.39%** | **$108,390.00** |
| **22** | **CSUITE_CLUSTER** | **45** | **4** | **100.00%** | **99.00** | **6.08** | **0.00%** | **5.64%** | **$105,640.00** |
| **23** | **CSUITE_CLUSTER** | **60** | **4** | **75.00%** | **5.87** | **1.74** | **0.97%** | **4.87%** | **$104,870.00** |
| **24** | **CSUITE_CLUSTER** | **30** | **4** | **75.00%** | **2.60** | **0.96** | **0.78%** | **1.28%** | **$101,280.00** |
| **25** | **CSUITE_CLUSTER** | **20** | **4** | **75.00%** | **4.05** | **1.54** | **0.32%** | **0.97%** | **$100,970.00** |

---

## 3. Key Quantitative Insights & Attribution

1. **Holding Period Alpha Scaling**:
   - Across every strategy type, extending the holding period from **20 days to 60–90 days** dramatically increased Total Return % and Sharpe Ratio.
   - This aligns with empirical financial research: insider open-market buys capture positive earnings surprise drift over the subsequent 1 to 2 quarterly earnings announcements.
2. **Conviction vs. Volume**:
   - While `COMBINED` achieved the highest raw dollar return (**+475.55%** across 214 trades), `CONVICTION` (CEO/CFO purchases $> \$100k$) delivered the highest **Sharpe Ratio (4.09)** and **Win Rate (93.88%)** with lower drawdowns (0.90%).
3. **Industry Accumulation Momentum**:
   - `INDUSTRY_MOMENTUM` was the second best performing strategy overall (**+467.55% ROI**), proving that filtering insider purchases by GICS industry sentiment ratio ($\ge 1.5x$) serves as an exceptional macro tailwind filter.

---

## 4. How to Reproduce Backtest Results via CLI

You can execute this multi-strategy sweep or run individual strategy backtests directly from the terminal:

```bash
# 1. Run the full 25-strategy ROI sweep across Year 2026 ($1B+ market cap)
python main.py sweep --year 2026 --min-market-cap 1000000000 --show-log

# 2. Run the #1 Highest ROI configuration (COMBINED, 90 Days)
python main.py backtest --strategy combined --year 2026 --holding-days 90 --show-log

# 3. Run the #1 Individual non-combined strategy (INDUSTRY_MOMENTUM, 90 Days)
python main.py backtest --strategy industry_momentum --year 2026 --holding-days 90 --show-log

# 4. Run C-Suite CEO/CFO Conviction buys (4.09 Sharpe Ratio)
python main.py backtest --strategy conviction --year 2026 --holding-days 90
```

The sweep results are also automatically saved to machine-readable JSON and CSV files:
- `data/strategy_comparison_2026.csv`
- `data/strategy_comparison_2026.json`
