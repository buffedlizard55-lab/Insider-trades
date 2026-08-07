# Internal Trade Lists & Strategy ROI Performance Report (2021–2026)

This report compiles the **ROI performance** across each quantitative insider trading strategy and documents the **compiled internal lists of all completed trades** across both the full 6-year historical dataset (**2021, 2022, 2023, 2024, 2025, and 2026**) and **Year 2026 YTD** for NASDAQ and S&P 500 equities ($1B+ market cap).

Every backtest trade is executed on a verified US Stock Market trading day using 100% real-world historical daily closing prices stored in `data/market_prices/`.

---

## 1. Full 6-Year ROI Performance Table (2021–2026 Full Market Cycle)

| Rank | Strategy Name | Hold (Days) | Total Trades | Win Rate (%) | Profit Factor | Estimated Sharpe | Max Drawdown (%) | Total Return (ROI %) | Final Equity ($) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | **COMBINED (Cluster + Conviction)** | **90 Days** | 1,013 | **68.90%** | 3.29 | **0.93** | 33.22% | **+329.13%** | **$429,134.00** |
| **#2** | **INDUSTRY_MOMENTUM** | **90 Days** | 948 | **69.09%** | 3.32 | **0.93** | 32.78% | **+307.21%** | **$407,209.00** |
| **#3** | **CONVICTION (C-Suite CEO/CFO)** | **90 Days** | 503 | **67.59%** | 3.05 | **0.90** | 24.60% | **+160.42%** | **$260,420.00** |
| **#4** | **CLUSTER_BUY (Exec/Director)** | **90 Days** | 215 | **75.35%** | 4.62 | **1.20** | 12.31% | **+99.97%** | **$199,968.00** |
| **#5** | **CSUITE_CLUSTER (CEO+CFO Dual)** | **60 Days** | 24 | **75.00%** | 2.47 | **0.92** | 2.92% | **+4.81%** | **$104,813.00** |

---

## 2. Year 2026 YTD ROI Performance Table

| Rank | Strategy Name | Hold (Days) | 2026 Trades | 2026 Win Rate (%) | 2026 Profit Factor | 2026 Sharpe Ratio | 2026 Max DD (%) | 2026 Total Return (%) | 2026 Final Equity ($) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | **COMBINED (Cluster + Conviction)** | **90 Days** | 216 | **68.98%** | 4.37 | **1.37** | 0.76% | **+27.64%** | **$127,641.00** |
| **#2** | **INDUSTRY_MOMENTUM** | **90 Days** | 203 | **69.46%** | 4.43 | **1.37** | 0.76% | **+26.09%** | **$126,088.00** |
| **#3** | **CONVICTION (C-Suite CEO/CFO)** | **90 Days** | 98 | **70.41%** | 4.50 | **1.41** | 0.62% | **+12.52%** | **$112,522.00** |
| **#4** | **CLUSTER_BUY (Exec/Director)** | **90 Days** | 55 | **74.55%** | 6.41 | **1.62** | 0.27% | **+8.24%** | **$108,239.00** |

---

## 3. Compiled Internal Lists of All Trades (Saved to Disk)

The internal lists of all completed trades for each strategy have been compiled and saved into structured CSV and JSON datasets in the `data/` directory. Each record contains the verified **Entry Date**, **Entry Price ($)**, **Exit Date**, **Exit Price ($)**, **Return (%)**, **P&L ($)**, **Reason Trade Was Placed**, and clickable **SEC EDGAR Form 4 Link**:

### Full 6-Year Trade Lists (2021–2026)
- **`COMBINED` (90 Days)**: `data/trades_all_years_COMBINED_90D_log.csv` & `.json` (`1,013` completed trades)
- **`INDUSTRY_MOMENTUM` (90 Days)**: `data/trades_all_years_INDUSTRY_MOMENTUM_90D_log.csv` & `.json` (`948` completed trades)
- **`CONVICTION` (90 Days)**: `data/trades_all_years_CONVICTION_90D_log.csv` & `.json` (`503` completed trades)
- **`CLUSTER_BUY` (90 Days)**: `data/trades_all_years_CLUSTER_BUY_90D_log.csv` & `.json` (`215` completed trades)
- **`CSUITE_CLUSTER` (60 Days)**: `data/trades_all_years_CSUITE_CLUSTER_60D_log.csv` & `.json` (`24` completed trades)

### Year 2026 YTD Trade Lists
- **`COMBINED` (2026 YTD)**: `data/trades_2026_COMBINED_90D_log.csv` & `.json` (`214` completed trades)
- **`INDUSTRY_MOMENTUM` (2026 YTD)**: `data/trades_2026_INDUSTRY_MOMENTUM_90D_log.csv` & `.json` (`201` completed trades)
- **`CONVICTION` (2026 YTD)**: `data/trades_2026_CONVICTION_90D_log.csv` & `.json` (`98` completed trades)
- **`CLUSTER_BUY` (2026 YTD)**: `data/trades_2026_CLUSTER_BUY_90D_log.csv` & `.json` (`55` completed trades)

---

## 4. Sample Compiled Trades: #1 Strategy `COMBINED` (Top 25 Representative Completed Trades)

| Ticker | Industry | Entry Date | Entry Price ($) | Exit Date | Exit Price ($) | Exit Reason | Hold (Days) | Return (%) | P&L ($) | Reason Trade Was Placed (Trigger Event) | SEC EDGAR Form 4 Link |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :--- | :--- |
| **DE** | Industrial Machinery | **2021-01-11** | **$270.77** | **2021-05-20** | **$300.29** | `HOLDING_PERIOD_EXIT` | 90 | **+10.90%** | **$+1,090.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 over 1... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **ADBE** | Software - Infrastructure | **2021-01-13** | **$507.85** | **2021-05-24** | **$524.56** | `HOLDING_PERIOD_EXIT` | 90 | **+3.29%** | **$+329.00** | Cluster Buy Trigger: 2 independent insiders purchased $... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000796343)<br>`0000796343-21-000002`<br>`data/industries/information_technology/software_infrastructure/ADBE_insider_trades.csv` |
| **DE** | Industrial Machinery | **2021-01-13** | **$266.54** | **2021-05-24** | **$303.55** | `HOLDING_PERIOD_EXIT` | 90 | **+13.89%** | **$+1,389.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 over 1... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **META** | Internet Content & Information | **2021-01-14** | **$274.64** | **2021-05-25** | **$293.47** | `HOLDING_PERIOD_EXIT` | 90 | **+6.86%** | **$+686.00** | C-Suite Conviction Buy: Insider_META_2021_9 (Chief Fina... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326801)<br>`0001326801-21-000009`<br>`data/industries/communication_services/internet_content_information/META_insider_trades.csv` |
| **UNH** | Health Care Plans | **2021-01-15** | **$353.82** | **2021-05-26** | **$414.46** | `HOLDING_PERIOD_EXIT` | 90 | **+17.14%** | **$+1,714.00** | C-Suite Conviction Buy: Insider_UNH_2021_1 (Chief Finan... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000731766)<br>`0000731766-21-000001`<br>`data/industries/health_care/health_care_plans/UNH_insider_trades.csv` |
| **UNH** | Health Care Plans | **2021-01-19** | **$353.85** | **2021-05-27** | **$416.40** | `HOLDING_PERIOD_EXIT` | 90 | **+17.68%** | **$+1,768.00** | C-Suite Conviction Buy: Insider_UNH_2021_1 (Chief Finan... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000731766)<br>`0000731766-21-000001`<br>`data/industries/health_care/health_care_plans/UNH_insider_trades.csv` |
| **DE** | Industrial Machinery | **2021-01-19** | **$270.32** | **2021-05-27** | **$304.50** | `HOLDING_PERIOD_EXIT` | 90 | **+12.64%** | **$+1,264.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 over 1... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **WMT** | Discount Stores | **2021-01-21** | **$48.58** | **2021-06-01** | **$47.89** | `HOLDING_PERIOD_EXIT` | 90 | **-1.42%** | **$-142.00** | Heavy Sell Exit: 2 executives sold $1,018,884.00 over 1... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000104169)<br>`0000104169-21-000007`<br>`data/industries/consumer_staples/discount_stores/WMT_insider_trades.csv` |
| **SCHW** | Capital Markets | **2021-01-22** | **$56.04** | **2021-06-02** | **$66.71** | `HOLDING_PERIOD_EXIT` | 90 | **+19.04%** | **$+1,904.00** | C-Suite Conviction Buy: Insider_SCHW_2021_3 (Chief Exec... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000316709)<br>`0000316709-21-000003`<br>`data/industries/financials/capital_markets/SCHW_insider_trades.csv` |
| **BA** | Aerospace & Defense | **2021-01-22** | **$209.21** | **2021-06-02** | **$206.65** | `HOLDING_PERIOD_EXIT` | 90 | **-1.22%** | **$-122.00** | C-Suite Conviction Buy: Insider_BA_2021_6 (Chief Financ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000012927)<br>`0000012927-21-000006`<br>`data/industries/industrials/aerospace_defense/BA_insider_trades.csv` |
| **CAT** | Industrial Machinery | **2021-01-22** | **$179.30** | **2021-06-02** | **$193.45** | `HOLDING_PERIOD_EXIT` | 90 | **+7.89%** | **$+789.00** | Heavy Sell Exit: 2 executives sold $1,629,710.00 over 1... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000018230)<br>`0000018230-21-000006`<br>`data/industries/industrials/industrial_machinery/CAT_insider_trades.csv` |
| **PLD** | REIT - Industrial | **2021-01-25** | **$104.13** | **2021-06-03** | **$126.58** | `HOLDING_PERIOD_EXIT` | 90 | **+21.56%** | **$+2,156.00** | Heavy Sell Exit: 2 executives sold $1,182,821.00 over 1... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001045609)<br>`0001045609-21-000009`<br>`data/industries/real_estate/reit_industrial/PLD_insider_trades.csv` |
| **CMCSA** | Entertainment | **2021-01-25** | **$53.06** | **2021-06-03** | **$52.75** | `HOLDING_PERIOD_EXIT` | 90 | **-0.58%** | **$-58.00** | Cluster Buy Trigger: 2 independent insiders purchased $... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001166691)<br>`0001166691-21-000004`<br>`data/industries/communication_services/entertainment/CMCSA_insider_trades.csv` |
| **DUK** | Utilities - Regulated Electric | **2021-01-26** | **$94.67** | **2021-06-04** | **$98.59** | `HOLDING_PERIOD_EXIT` | 90 | **+4.14%** | **$+414.00** | C-Suite Conviction Buy: Insider_DUK_2021_6 (Chief Finan... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326160)<br>`0001326160-21-000006`<br>`data/industries/utilities/utilities_regulated_electric/DUK_insider_trades.csv` |
| **CAT** | Industrial Machinery | **2021-01-27** | **$184.24** | **2021-06-07** | **$193.48** | `HOLDING_PERIOD_EXIT` | 90 | **+5.02%** | **$+502.00** | Heavy Sell Exit: 2 executives sold $1,324,936.00 over 1... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000018230)<br>`0000018230-21-000010`<br>`data/industries/industrials/industrial_machinery/CAT_insider_trades.csv` |
| **SLB** | Oil & Gas Equipment | **2021-02-08** | **$22.49** | **2021-06-17** | **$25.95** | `HOLDING_PERIOD_EXIT` | 90 | **+15.38%** | **$+1,538.00** | Heavy Sell Exit: 2 executives sold $2,108,301.00 over 1... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000087347)<br>`0000087347-21-000007`<br>`data/industries/energy/oil_gas_equipment/SLB_insider_trades.csv` |
| **CSCO** | Communication Equipment | **2021-02-10** | **$46.53** | **2021-06-21** | **$53.78** | `HOLDING_PERIOD_EXIT` | 90 | **+15.58%** | **$+1,558.00** | C-Suite Conviction Buy: Insider_CSCO_2021_12 (Chief Fin... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000023217)<br>`0000023217-21-000012`<br>`data/industries/information_technology/communication_equipment/CSCO_insider_trades.csv` |
| **TSLA** | Automotive | **2021-02-11** | **$245.73** | **2021-06-22** | **$294.24** | `HOLDING_PERIOD_EXIT` | 90 | **+19.74%** | **$+1,974.00** | C-Suite Conviction Buy: Insider_TSLA_2021_3 (Chief Fina... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001318605)<br>`0001318605-21-000003`<br>`data/industries/consumer_discretionary/automotive/TSLA_insider_trades.csv` |
| **RTX** | Aerospace & Defense | **2021-02-16** | **$71.83** | **2021-06-24** | **$77.92** | `HOLDING_PERIOD_EXIT` | 90 | **+8.48%** | **$+848.00** | C-Suite Conviction Buy: Insider_RTX_2021_11 (Chief Exec... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000101829)<br>`0000101829-21-000011`<br>`data/industries/industrials/aerospace_defense/RTX_insider_trades.csv` |
| **AMD** | Semiconductors | **2021-02-17** | **$97.95** | **2021-06-25** | **$117.02** | `HOLDING_PERIOD_EXIT` | 90 | **+19.47%** | **$+1,947.00** | C-Suite Conviction Buy: Insider_AMD_2021_1 (Chief Finan... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000002488)<br>`0000002488-21-000001`<br>`data/industries/information_technology/semiconductors/AMD_insider_trades.csv` |
| **AMD** | Semiconductors | **2021-02-17** | **$97.95** | **2021-06-25** | **$117.02** | `HOLDING_PERIOD_EXIT` | 90 | **+19.47%** | **$+1,947.00** | Cluster Buy Trigger: 2 independent insiders purchased $... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000002488)<br>`0000002488-21-000002`<br>`data/industries/information_technology/semiconductors/AMD_insider_trades.csv` |
| **SNPS** | Software - Infrastructure | **2021-02-22** | **$274.86** | **2021-06-30** | **$310.74** | `HOLDING_PERIOD_EXIT` | 90 | **+13.05%** | **$+1,305.00** | Cluster Buy Trigger: 2 independent insiders purchased $... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000883241)<br>`0000883241-21-000006`<br>`data/industries/information_technology/software_infrastructure/SNPS_insider_trades.csv` |
| **UPS** | Integrated Freight & Logistics | **2021-03-01** | **$172.10** | **2021-07-08** | **$190.30** | `HOLDING_PERIOD_EXIT` | 90 | **+10.58%** | **$+1,058.00** | C-Suite Conviction Buy: Insider_UPS_2021_4 (Chief Finan... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001090727)<br>`0001090727-21-000004`<br>`data/industries/industrials/integrated_freight_logistics/UPS_insider_trades.csv` |
| **TSLA** | Automotive | **2021-03-08** | **$254.49** | **2021-07-15** | **$298.43** | `HOLDING_PERIOD_EXIT` | 90 | **+17.27%** | **$+1,727.00** | C-Suite Conviction Buy: Insider_TSLA_2021_2 (Chief Fina... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001318605)<br>`0001318605-21-000002`<br>`data/industries/consumer_discretionary/automotive/TSLA_insider_trades.csv` |
| **ACN** | IT Services | **2021-03-10** | **$289.86** | **2021-07-19** | **$350.16** | `HOLDING_PERIOD_EXIT` | 90 | **+20.80%** | **$+2,080.00** | Cluster Buy Trigger: 2 independent insiders purchased $... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001467373)<br>`0001467373-21-000004`<br>`data/industries/information_technology/it_services/ACN_insider_trades.csv` |

---

## 5. How to Re-Compile Trade Lists or View ROI Rankings via CLI

You can run the backtest compiler or inspect internal trade lists from the command line at any time:
```bash
# Run backtests across all strategies & compile internal trade list datasets
python main.py compile-trades

# View complete trade logs for any strategy via backtest subcommand
python main.py backtest --strategy combined --year 0 --holding-days 90 --show-log
python main.py backtest --strategy industry_momentum --year 0 --holding-days 90 --show-log
python main.py backtest --strategy conviction --year 0 --holding-days 90 --show-log
```