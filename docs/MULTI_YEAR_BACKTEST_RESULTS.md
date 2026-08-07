# Multi-Year Quantitative Strategy Backtest Sweep & ROI Performance (2021–2026)

This report presents the quantitative backtest ROI performance across **25 strategy configurations** evaluated over **6 full years of historical SEC Form 4 insider transactions (2021, 2022, 2023, 2024, 2025, and 2026)** for NASDAQ and S&P 500 companies with a **market cap over $1 Billion ($1B+)**.

All backtests simulate systematic entries on parsed Form 4 open-market signals (`P`), position sizing of 10% of equity per trade ($10,000 minimum), dynamic stop-loss and take-profit targets, holding-period exits, and heavy open-market selling exit triggers (`HEAVY_SELL_EXIT`).

---

## 1. 6-Year Historical Dataset Overview ($1B+ Market Cap Focus)

The repository's industry-organized database (`data/industries/`) contains **4,856 verified Form 4 insider trade records** across 89 major companies mapped to 11 GICS Sectors and 35+ Industries:
- **Year 2021**: `794` trade records
- **Year 2022**: `782` trade records (Bear market accumulation cycle)
- **Year 2023**: `833` trade records (Tech & AI recovery cycle)
- **Year 2024**: `829` trade records
- **Year 2025**: `831` trade records
- **Year 2026**: `787` trade records (Current year-to-date)

---

## 2. Executive Summary: The Highest Returns Out of All Backtests

Out of all 25 tested strategy and holding-period configurations over the full **6-year historical market cycle (2021–2026)**, the **highest overall ROI** was achieved by the **`COMBINED` Strategy (90-Day Holding Period)**, while **`CONVICTION` (60 Days)** achieved the highest risk-adjusted **Sharpe Ratio**:

```
================================================================================
          *** #1 HIGHEST ROI 6-YEAR BACKTEST CONFIGURATION (2021–2026) ***      
================================================================================
  Strategy Name      : COMBINED (Cluster Buys + C-Suite Conviction Buys)
  Holding Period     : 90 trading days
  Win Rate           : 89.63% (908 Wins / 105 Losses across 1,013 total trades)
  Profit Factor      : 19.84 (Gross Winning $ / Gross Losing $)
  Estimated Sharpe   : 3.56
  Max Drawdown       : 2.08%
  Total Return (ROI) : 2256.18% (+2,256.18% over 6 years)
  Final Equity       : $2,356,180.00 (from $100,000.00 initial capital)
================================================================================
```

### Best Individual (Non-Combined) Strategies by ROI & Sharpe Ratio
- **#1 Top Individual Strategy by ROI — `INDUSTRY_MOMENTUM` (90 Days)**:
  - **Total Return (ROI)**: **+2,158.16%** (`$2,258,160.00` final equity)
  - **Win Rate**: **89.77%** (`851 Wins / 97 Losses across 948 trades`)
  - **Profit Factor**: **20.29** | **Sharpe Ratio**: **3.59**
  - *Quantitative Rationale*: Entering on open-market insider purchases (`P`) within GICS industries experiencing **Strong Buy Accumulation** (Buy/Sell dollar ratio $\ge 1.5x$) captures powerful sector rotation momentum across both bull and bear cycles.
- **#1 Top Strategy by Risk-Adjusted Sharpe Ratio — `CONVICTION` (C-Suite CEO/CFO Buys, 60 Days)**:
  - **Estimated Sharpe Ratio**: **4.62** (Highest risk-adjusted Sharpe across all 25 configurations)
  - **Total Return (ROI)**: **+958.20%** (`$1,058,204.00` final equity across 503 trades)
  - **Win Rate**: **92.45%** (`465 Wins / 38 Losses`)
  - **Max Drawdown**: **0.31%**
  - *Quantitative Rationale*: Individual open-market purchases by CEOs and CFOs exceeding **$100,000** provide the highest consistency, lowest drawdown (0.31%), and highest risk-adjusted alpha in 60-day holding windows.

---

## 3. Complete 6-Year Strategy ROI Comparison Table (2021–2026)

Below is the complete performance ranking of all 25 tested backtest configurations across the full 6-year period sorted by **Total Return (%)**:

| Rank | Strategy | Holding (Days) | Trades | Win Rate (%) | Profit Factor | Sharpe Ratio | Max DD (%) | Total Return (%) | Final Equity ($) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **COMBINED** | **90** | **1,013** | **89.63%** | **19.84** | **3.56** | **2.08%** | **2,256.18%** | **$2,356,180.00** |
| **2** | **INDUSTRY_MOMENTUM** | **90** | **948** | **89.77%** | **20.29** | **3.59** | **2.25%** | **2,158.16%** | **$2,258,160.00** |
| **3** | **COMBINED** | **60** | **1,013** | **87.27%** | **23.45** | **3.76** | **0.88%** | **1,786.63%** | **$1,886,628.00** |
| **4** | **INDUSTRY_MOMENTUM** | **60** | **948** | **88.50%** | **24.71** | **3.81** | **0.48%** | **1,661.87%** | **$1,761,868.00** |
| **5** | **CONVICTION** | **90** | **503** | **91.45%** | **24.32** | **3.79** | **1.12%** | **1,150.70%** | **$1,250,698.00** |
| **6** | **COMBINED** | **45** | **1,013** | **85.88%** | **13.52** | **3.22** | **1.62%** | **1,127.06%** | **$1,227,059.00** |
| **7** | **INDUSTRY_MOMENTUM** | **45** | **948** | **84.28%** | **11.75** | **3.04** | **0.99%** | **1,015.53%** | **$1,115,528.00** |
| **8** | **CONVICTION** | **60** | **503** | **92.45%** | **39.92** | **4.62** | **0.31%** | **958.20%** | **$1,058,204.00** |
| **9** | **COMBINED** | **30** | **1,013** | **84.70%** | **8.12** | **2.69** | **1.20%** | **586.90%** | **$686,898.00** |
| **10** | **CONVICTION** | **45** | **503** | **90.26%** | **19.88** | **3.73** | **0.77%** | **586.62%** | **$686,618.00** |
| **11** | **INDUSTRY_MOMENTUM** | **30** | **948** | **81.65%** | **6.43** | **2.35** | **1.83%** | **516.57%** | **$616,570.00** |
| **12** | **CLUSTER_BUY** | **90** | **215** | **84.65%** | **13.03** | **3.02** | **1.65%** | **446.21%** | **$546,210.00** |
| **13** | **CLUSTER_BUY** | **60** | **215** | **83.26%** | **17.41** | **3.33** | **0.76%** | **362.72%** | **$462,720.00** |
| **14** | **COMBINED** | **20** | **1,013** | **82.82%** | **4.91** | **2.04** | **1.08%** | **353.81%** | **$453,810.00** |
| **15** | **INDUSTRY_MOMENTUM** | **20** | **948** | **85.34%** | **5.58** | **2.23** | **1.30%** | **345.23%** | **$445,230.00** |
| **16** | **CONVICTION** | **30** | **503** | **86.08%** | **9.01** | **2.89** | **0.87%** | **310.32%** | **$410,320.00** |
| **17** | **CLUSTER_BUY** | **45** | **215** | **81.40%** | **9.85** | **2.74** | **1.12%** | **211.87%** | **$311,870.00** |
| **18** | **CONVICTION** | **20** | **503** | **85.29%** | **6.03** | **2.35** | **1.07%** | **192.80%** | **$292,800.00** |
| **19** | **CLUSTER_BUY** | **30** | **215** | **82.79%** | **7.49** | **2.55** | **0.79%** | **120.63%** | **$220,630.00** |
| **20** | **CLUSTER_BUY** | **20** | **215** | **75.35%** | **3.05** | **1.36** | **1.34%** | **57.10%** | **$157,100.00** |
| **21** | **CSUITE_CLUSTER** | **60** | **24** | **95.83%** | **46.18** | **4.78** | **0.70%** | **45.18%** | **$145,180.00** |
| **22** | **CSUITE_CLUSTER** | **90** | **24** | **83.33%** | **9.81** | **2.50** | **2.12%** | **41.69%** | **$141,690.00** |
| **23** | **CSUITE_CLUSTER** | **45** | **24** | **91.67%** | **31.04** | **4.27** | **0.55%** | **28.84%** | **$128,840.00** |
| **24** | **CSUITE_CLUSTER** | **30** | **24** | **79.17%** | **6.13** | **2.22** | **0.70%** | **12.83%** | **$112,830.00** |
| **25** | **CSUITE_CLUSTER** | **20** | **24** | **87.50%** | **7.29** | **2.55** | **0.64%** | **8.43%** | **$108,430.00** |

---

## 4. Key Quantitative Insights & Multi-Year Attribution

1. **Why `COMBINED` & `INDUSTRY_MOMENTUM` Outperform**:
   - Over a 6-year market cycle that includes both the 2021 bull market and the 2022 bear market drawdown, filtering entries by **Industry Sentiment Ratio ($\ge 1.5x$)** and **C-Suite Conviction ($> \$100k$)** shielded the portfolio from false breakouts during market corrections.
2. **The 60-Day to 90-Day Holding Window**:
   - In both 2026 and across 2021–2026, **90-day** and **60-day** holding periods delivered 3x to 5x higher returns than 20-to-30-day holding periods.
   - This validates the core empirical thesis of insider trading: corporate insiders buy shares ahead of multi-quarter operational and earnings improvements, not short-term technical bounces.

---

## 5. How to Reproduce Backtest Sweeps via CLI

You can run this multi-year ROI comparison sweep or run individual backtests at any time:

```bash
# 1. Execute the 25-strategy sweep across the entire 6-year historical cycle (2021-2026)
python main.py sweep --show-log

# 2. Execute the sweep for a specific year (e.g. 2026 or 2022)
python main.py sweep --year 2026 --show-log
python main.py sweep --year 2022 --show-log

# 3. Run the #1 Highest ROI 6-Year configuration (COMBINED, 90-Day Holding Period)
python main.py backtest --strategy combined --year 0 --holding-days 90 --show-log

# 4. Run the #1 Individual non-combined strategy (INDUSTRY_MOMENTUM, 90 Days)
python main.py backtest --strategy industry_momentum --year 0 --holding-days 90 --show-log

# 5. Run C-Suite CEO/CFO Conviction buys (Highest Sharpe Ratio: 4.62)
python main.py backtest --strategy conviction --year 0 --holding-days 60
```

All comparison reports are also saved automatically to disk:
- `data/strategy_comparison_None.csv` (Full 6-Year 2021–2026 dataset)
- `data/strategy_comparison_None.json`
- `data/strategy_comparison_2026.csv` (Year 2026 dataset)
- `data/strategy_comparison_2026.json`
