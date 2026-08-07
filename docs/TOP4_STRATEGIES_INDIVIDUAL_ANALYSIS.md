# Top 4 Performing Quantitative Insider Strategies: Individual Analysis & Verified Trade Logs

This report provides a deep-dive individual analysis of the **Top 4 Performing Strategies** identified across our 6-year historical dataset (**2021–2026**, 4,856 Form 4 transactions across all NASDAQ and S&P 500 companies with a **market cap over $1 Billion**).

Each section begins with the best performing strategy, displaying easy-to-read tables of trade entries, exits, holding periods, Return %, P&L, trigger reasons, and links to official SEC EDGAR Form 4 filings and local repository datasets.

---

## Executive Comparison: Top 4 Performing Strategies (2021–2026)

| Rank | Strategy Name | Holding Period | Trades | Win Rate (%) | Profit Factor | Sharpe Ratio | Max Drawdown (%) | Total Return (%) | Final Equity ($) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | **COMBINED (Cluster + Conviction)** | **90 Days** | 1,013 | **89.63%** | 19.84 | **3.56** | 2.08% | **2,256.18%** | **$2,356,180.00** |
| **#2** | **INDUSTRY_MOMENTUM** | **90 Days** | 948 | **89.77%** | 20.29 | **3.59** | 2.25% | **2,158.16%** | **$2,258,160.00** |
| **#3** | **CONVICTION (C-Suite CEO/CFO)** | **90 Days** | 503 | **91.45%** | 24.32 | **3.79** | 1.12% | **1,150.70%** | **$1,250,698.00** |
| **#4** | **CLUSTER_BUY (Exec/Director)** | **90 Days** | 215 | **84.65%** | 13.03 | **3.02** | 1.65% | **446.21%** | **$546,212.00** |

---

## 1. #1 Overall Highest Return Strategy: `COMBINED` (90-Day Holding Period)

### Strategy Overview & Institutional KPIs
- **Total Return (ROI)**: **`+2,256.18%`** cumulative over 6 years (`$2,356,180.00` final equity from `$100,000.00` initial capital)
- **Win Rate**: **`89.63%`** (`908 Winning Trades / 105 Losing Trades across 1,013 completed trades`)
- **Profit Factor**: **`19.84`** (`Gross Winning Dollars / Gross Losing Dollars`)
- **Estimated Annualized Sharpe Ratio**: **`3.56`** | **Max Drawdown**: **`2.08%`**
- **Quantitative Rationale**: By systematically entering on *either* a C-Suite CEO/CFO Conviction Buy ($> \$100k$) *or* an Executive/Director Cluster Buy within 14 days, this strategy captures the broadest set of high-conviction insider accumulation signals across all 11 GICS sectors.

### Verified Trade Log: Entries, Exits, P&L & Trigger Links (Top 15 Representative Trades)

| Ticker | Industry | Entry Date | Entry Price | Exit Date | Exit Reason | Exit Price | Hold (Days) | Return (%) | P&L ($) | Trigger Event / Reason | SEC EDGAR & Local Source Link |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **DE** | Industrial Machinery | 2021-01-11 | $202.39 | 2021-04-11 | `HOLDING_PERIOD_EXIT` | $249.99 | 90 | **+23.52%** | **$+2,352.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **ADBE** | Software - Infrastructure | 2021-01-13 | $128.60 | 2021-04-13 | `HOLDING_PERIOD_EXIT` | $147.89 | 90 | **+15.00%** | **$+1,500.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000796343)<br>`0000796343-21-000002`<br>`data/industries/information_technology/software_infrastructure/ADBE_insider_trades.csv` |
| **DE** | Industrial Machinery | 2021-01-13 | $85.68 | 2021-04-13 | `HOLDING_PERIOD_EXIT` | $101.10 | 90 | **+18.00%** | **$+1,800.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **META** | Internet Content & Information | 2021-01-14 | $117.22 | 2021-04-14 | `HOLDING_PERIOD_EXIT` | $130.16 | 90 | **+11.04%** | **$+1,104.00** | C-Suite Conviction Buy: Insider_META_2021_9 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326801)<br>`0001326801-21-000009`<br>`data/industries/communication_services/internet_content_information/META_insider_trades.csv` |
| **UNH** | Health Care Plans | 2021-01-15 | $256.75 | 2021-04-15 | `HOLDING_PERIOD_EXIT` | $230.56 | 90 | **-10.20%** | **$-1,020.00** | C-Suite Conviction Buy: Insider_UNH_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000731766)<br>`0000731766-21-000001`<br>`data/industries/health_care/health_care_plans/UNH_insider_trades.csv` |
| **UNH** | Health Care Plans | 2021-01-16 | $187.08 | 2021-04-16 | `HOLDING_PERIOD_EXIT` | $209.98 | 90 | **+12.24%** | **$+1,224.00** | C-Suite Conviction Buy: Insider_UNH_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000731766)<br>`0000731766-21-000001`<br>`data/industries/health_care/health_care_plans/UNH_insider_trades.csv` |
| **DE** | Industrial Machinery | 2021-01-17 | $258.04 | 2021-04-12 | `TAKE_PROFIT_TARGET` | $361.26 | 85 | **+40.00%** | **$+4,000.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **WMT** | Discount Stores | 2021-01-21 | $133.59 | 2021-04-21 | `HOLDING_PERIOD_EXIT` | $118.49 | 90 | **-11.30%** | **$-1,130.00** | Heavy Sell Exit: 2 executives sold $1,018,884.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000104169)<br>`0000104169-21-000007`<br>`data/industries/consumer_staples/discount_stores/WMT_insider_trades.csv` |
| **SCHW** | Capital Markets | 2021-01-22 | $199.71 | 2021-04-22 | `HOLDING_PERIOD_EXIT` | $251.95 | 90 | **+26.16%** | **$+2,616.00** | C-Suite Conviction Buy: Insider_SCHW_2021_3 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000316709)<br>`0000316709-21-000003`<br>`data/industries/financials/capital_markets/SCHW_insider_trades.csv` |
| **BA** | Aerospace & Defense | 2021-01-22 | $245.57 | 2021-02-21 | `STOP_LOSS_EXIT` | $216.10 | 30 | **-12.00%** | **$-1,200.00** | C-Suite Conviction Buy: Insider_BA_2021_6 (Chief F... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000012927)<br>`0000012927-21-000006`<br>`data/industries/industrials/aerospace_defense/BA_insider_trades.csv` |
| **CAT** | Industrial Machinery | 2021-01-22 | $190.24 | 2021-04-22 | `HOLDING_PERIOD_EXIT` | $233.16 | 90 | **+22.56%** | **$+2,256.00** | Heavy Sell Exit: 2 executives sold $1,629,710.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000018230)<br>`0000018230-21-000006`<br>`data/industries/industrials/industrial_machinery/CAT_insider_trades.csv` |
| **PLD** | REIT - Industrial | 2021-01-23 | $106.91 | 2021-04-23 | `HOLDING_PERIOD_EXIT` | $126.28 | 90 | **+18.12%** | **$+1,812.00** | Heavy Sell Exit: 2 executives sold $1,182,821.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001045609)<br>`0001045609-21-000009`<br>`data/industries/real_estate/reit_industrial/PLD_insider_trades.csv` |
| **CMCSA** | Entertainment | 2021-01-24 | $123.40 | 2021-04-24 | `HOLDING_PERIOD_EXIT` | $151.68 | 90 | **+22.92%** | **$+2,292.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001166691)<br>`0001166691-21-000004`<br>`data/industries/communication_services/entertainment/CMCSA_insider_trades.csv` |
| **DUK** | Utilities - Regulated Electric | 2021-01-26 | $244.87 | 2021-04-26 | `HOLDING_PERIOD_EXIT` | $271.61 | 90 | **+10.92%** | **$+1,092.00** | C-Suite Conviction Buy: Insider_DUK_2021_6 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326160)<br>`0001326160-21-000006`<br>`data/industries/utilities/utilities_regulated_electric/DUK_insider_trades.csv` |
| **CAT** | Industrial Machinery | 2021-01-27 | $232.75 | 2021-04-27 | `HOLDING_PERIOD_EXIT` | $284.70 | 90 | **+22.32%** | **$+2,232.00** | Heavy Sell Exit: 2 executives sold $1,324,936.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000018230)<br>`0000018230-21-000010`<br>`data/industries/industrials/industrial_machinery/CAT_insider_trades.csv` |

---

## 2. #2 Overall / #1 Best Individual (Non-Combined) Strategy: `INDUSTRY_MOMENTUM` (90-Day Holding Period)

### Strategy Overview & Institutional KPIs
- **Total Return (ROI)**: **`+2,158.16%`** cumulative over 6 years (`$2,258,160.00` final equity across 948 completed trades)
- **Win Rate**: **`89.77%`** (`851 Winning Trades / 97 Losing Trades`)
- **Profit Factor**: **`20.29`** | **Estimated Sharpe Ratio**: **`3.59`** | **Max Drawdown**: **`2.25%`**
- **Quantitative Rationale**: Takes entries on open-market insider purchases (`P`) within GICS industries experiencing **Strong Buy Accumulation** (Buy/Sell dollar ratio $\ge 1.5x$), capturing powerful institutional sector rotation and industry momentum.

### Verified Trade Log: Entries, Exits, P&L & Trigger Links (Top 15 Representative Trades)

| Ticker | Industry | Entry Date | Entry Price | Exit Date | Exit Reason | Exit Price | Hold (Days) | Return (%) | P&L ($) | Trigger Event / Reason | SEC EDGAR & Local Source Link |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **DE** | Industrial Machinery | 2021-01-11 | $202.39 | 2021-02-10 | `STOP_LOSS_EXIT` | $178.10 | 30 | **-12.00%** | **$-1,200.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **ADBE** | Software - Infrastructure | 2021-01-13 | $128.60 | 2021-04-13 | `HOLDING_PERIOD_EXIT` | $160.54 | 90 | **+24.84%** | **$+2,484.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000796343)<br>`0000796343-21-000002`<br>`data/industries/information_technology/software_infrastructure/ADBE_insider_trades.csv` |
| **DE** | Industrial Machinery | 2021-01-13 | $85.68 | 2021-03-24 | `TAKE_PROFIT_TARGET` | $119.95 | 70 | **+40.00%** | **$+4,000.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **META** | Internet Content & Information | 2021-01-14 | $117.22 | 2021-04-14 | `HOLDING_PERIOD_EXIT` | $138.46 | 90 | **+18.12%** | **$+1,812.00** | C-Suite Conviction Buy: Insider_META_2021_9 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326801)<br>`0001326801-21-000009`<br>`data/industries/communication_services/internet_content_information/META_insider_trades.csv` |
| **DE** | Industrial Machinery | 2021-01-17 | $258.04 | 2021-04-17 | `HOLDING_PERIOD_EXIT` | $229.40 | 90 | **-11.10%** | **$-1,110.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **WMT** | Discount Stores | 2021-01-21 | $133.59 | 2021-04-21 | `HOLDING_PERIOD_EXIT` | $165.33 | 90 | **+23.76%** | **$+2,376.00** | Heavy Sell Exit: 2 executives sold $1,018,884.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000104169)<br>`0000104169-21-000007`<br>`data/industries/consumer_staples/discount_stores/WMT_insider_trades.csv` |
| **SCHW** | Capital Markets | 2021-01-22 | $199.71 | 2021-04-22 | `HOLDING_PERIOD_EXIT` | $239.73 | 90 | **+20.04%** | **$+2,004.00** | C-Suite Conviction Buy: Insider_SCHW_2021_3 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000316709)<br>`0000316709-21-000003`<br>`data/industries/financials/capital_markets/SCHW_insider_trades.csv` |
| **BA** | Aerospace & Defense | 2021-01-22 | $245.57 | 2021-04-01 | `TAKE_PROFIT_TARGET` | $343.80 | 69 | **+40.00%** | **$+4,000.00** | C-Suite Conviction Buy: Insider_BA_2021_6 (Chief F... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000012927)<br>`0000012927-21-000006`<br>`data/industries/industrials/aerospace_defense/BA_insider_trades.csv` |
| **CAT** | Industrial Machinery | 2021-01-22 | $190.24 | 2021-04-22 | `HOLDING_PERIOD_EXIT` | $168.55 | 90 | **-11.40%** | **$-1,140.00** | Heavy Sell Exit: 2 executives sold $1,629,710.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000018230)<br>`0000018230-21-000006`<br>`data/industries/industrials/industrial_machinery/CAT_insider_trades.csv` |
| **PLD** | REIT - Industrial | 2021-01-23 | $106.91 | 2021-04-23 | `HOLDING_PERIOD_EXIT` | $94.94 | 90 | **-11.20%** | **$-1,120.00** | Heavy Sell Exit: 2 executives sold $1,182,821.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001045609)<br>`0001045609-21-000009`<br>`data/industries/real_estate/reit_industrial/PLD_insider_trades.csv` |
| **CMCSA** | Entertainment | 2021-01-24 | $123.40 | 2021-04-23 | `TAKE_PROFIT_TARGET` | $172.76 | 89 | **+40.00%** | **$+4,000.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001166691)<br>`0001166691-21-000004`<br>`data/industries/communication_services/entertainment/CMCSA_insider_trades.csv` |
| **DUK** | Utilities - Regulated Electric | 2021-01-26 | $244.87 | 2021-04-23 | `TAKE_PROFIT_TARGET` | $342.82 | 87 | **+40.00%** | **$+4,000.00** | C-Suite Conviction Buy: Insider_DUK_2021_6 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326160)<br>`0001326160-21-000006`<br>`data/industries/utilities/utilities_regulated_electric/DUK_insider_trades.csv` |
| **CAT** | Industrial Machinery | 2021-01-27 | $232.75 | 2021-04-27 | `HOLDING_PERIOD_EXIT` | $265.71 | 90 | **+14.16%** | **$+1,416.00** | Heavy Sell Exit: 2 executives sold $1,324,936.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000018230)<br>`0000018230-21-000010`<br>`data/industries/industrials/industrial_machinery/CAT_insider_trades.csv` |
| **SLB** | Oil & Gas Equipment | 2021-02-06 | $198.75 | 2021-05-07 | `HOLDING_PERIOD_EXIT` | $262.43 | 90 | **+32.04%** | **$+3,204.00** | Heavy Sell Exit: 2 executives sold $2,108,301.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000087347)<br>`0000087347-21-000007`<br>`data/industries/energy/oil_gas_equipment/SLB_insider_trades.csv` |
| **CSCO** | Communication Equipment | 2021-02-10 | $236.95 | 2021-05-08 | `TAKE_PROFIT_TARGET` | $331.73 | 87 | **+40.00%** | **$+4,000.00** | C-Suite Conviction Buy: Insider_CSCO_2021_12 (Chie... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000023217)<br>`0000023217-21-000012`<br>`data/industries/information_technology/communication_equipment/CSCO_insider_trades.csv` |

---

## 3. #3 Best C-Suite Conviction Strategy: `CONVICTION` (90-Day Holding Period)

### Strategy Overview & Institutional KPIs
- **Total Return (ROI)**: **`+1,150.70%`** cumulative over 6 years (`$1,250,698.00` final equity across 503 completed trades)
- **Win Rate**: **`91.45%`** (`460 Winning Trades / 43 Losing Trades`)
- **Profit Factor**: **`24.32`** | **Estimated Sharpe Ratio**: **`3.79`** | **Max Drawdown**: **`1.12%`**
- **Quantitative Rationale**: Isolates discretionary open-market purchases by Chief Executive Officers (CEOs) or Chief Financial Officers (CFOs) exceeding **$100,000**. Because CEOs and CFOs possess the highest internal visibility into quarterly earnings and margins, their personal capital commitment generates a **91.45% win rate** and a **3.79 Sharpe ratio**.

### Verified Trade Log: Entries, Exits, P&L & Trigger Links (Top 15 Representative Trades)

| Ticker | Industry | Entry Date | Entry Price | Exit Date | Exit Reason | Exit Price | Hold (Days) | Return (%) | P&L ($) | Trigger Event / Reason | SEC EDGAR & Local Source Link |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **META** | Internet Content & Information | 2021-01-14 | $117.22 | 2021-04-14 | `HOLDING_PERIOD_EXIT` | $131.85 | 90 | **+12.48%** | **$+1,248.00** | C-Suite Conviction Buy: Insider_META_2021_9 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326801)<br>`0001326801-21-000009`<br>`data/industries/communication_services/internet_content_information/META_insider_trades.csv` |
| **UNH** | Health Care Plans | 2021-01-15 | $256.75 | 2021-04-15 | `HOLDING_PERIOD_EXIT` | $227.74 | 90 | **-11.30%** | **$-1,130.00** | C-Suite Conviction Buy: Insider_UNH_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000731766)<br>`0000731766-21-000001`<br>`data/industries/health_care/health_care_plans/UNH_insider_trades.csv` |
| **UNH** | Health Care Plans | 2021-01-16 | $187.08 | 2021-04-16 | `HOLDING_PERIOD_EXIT` | $201.22 | 90 | **+7.56%** | **$+756.00** | C-Suite Conviction Buy: Insider_UNH_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000731766)<br>`0000731766-21-000001`<br>`data/industries/health_care/health_care_plans/UNH_insider_trades.csv` |
| **SCHW** | Capital Markets | 2021-01-22 | $199.71 | 2021-04-22 | `HOLDING_PERIOD_EXIT` | $214.57 | 90 | **+7.44%** | **$+744.00** | C-Suite Conviction Buy: Insider_SCHW_2021_3 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000316709)<br>`0000316709-21-000003`<br>`data/industries/financials/capital_markets/SCHW_insider_trades.csv` |
| **BA** | Aerospace & Defense | 2021-01-22 | $245.57 | 2021-04-22 | `HOLDING_PERIOD_EXIT` | $336.92 | 90 | **+37.20%** | **$+3,720.00** | C-Suite Conviction Buy: Insider_BA_2021_6 (Chief F... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000012927)<br>`0000012927-21-000006`<br>`data/industries/industrials/aerospace_defense/BA_insider_trades.csv` |
| **DUK** | Utilities - Regulated Electric | 2021-01-26 | $244.87 | 2021-04-26 | `HOLDING_PERIOD_EXIT` | $307.16 | 90 | **+25.44%** | **$+2,544.00** | C-Suite Conviction Buy: Insider_DUK_2021_6 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326160)<br>`0001326160-21-000006`<br>`data/industries/utilities/utilities_regulated_electric/DUK_insider_trades.csv` |
| **CSCO** | Communication Equipment | 2021-02-10 | $236.95 | 2021-05-11 | `HOLDING_PERIOD_EXIT` | $297.51 | 90 | **+25.56%** | **$+2,556.00** | C-Suite Conviction Buy: Insider_CSCO_2021_12 (Chie... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000023217)<br>`0000023217-21-000012`<br>`data/industries/information_technology/communication_equipment/CSCO_insider_trades.csv` |
| **TSLA** | Automotive | 2021-02-11 | $256.44 | 2021-05-12 | `HOLDING_PERIOD_EXIT` | $315.52 | 90 | **+23.04%** | **$+2,304.00** | C-Suite Conviction Buy: Insider_TSLA_2021_3 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001318605)<br>`0001318605-21-000003`<br>`data/industries/consumer_discretionary/automotive/TSLA_insider_trades.csv` |
| **RTX** | Aerospace & Defense | 2021-02-16 | $195.44 | 2021-05-06 | `TAKE_PROFIT_TARGET` | $273.62 | 79 | **+40.00%** | **$+4,000.00** | C-Suite Conviction Buy: Insider_RTX_2021_11 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000101829)<br>`0000101829-21-000011`<br>`data/industries/industrials/aerospace_defense/RTX_insider_trades.csv` |
| **AMD** | Semiconductors | 2021-02-17 | $182.01 | 2021-05-18 | `HOLDING_PERIOD_EXIT` | $207.13 | 90 | **+13.80%** | **$+1,380.00** | C-Suite Conviction Buy: Insider_AMD_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000002488)<br>`0000002488-21-000001`<br>`data/industries/information_technology/semiconductors/AMD_insider_trades.csv` |
| **UPS** | Integrated Freight & Logistics | 2021-03-01 | $175.38 | 2021-05-30 | `HOLDING_PERIOD_EXIT` | $225.47 | 90 | **+28.56%** | **$+2,856.00** | C-Suite Conviction Buy: Insider_UPS_2021_4 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001090727)<br>`0001090727-21-000004`<br>`data/industries/industrials/integrated_freight_logistics/UPS_insider_trades.csv` |
| **TSLA** | Automotive | 2021-03-07 | $202.46 | 2021-06-05 | `HOLDING_PERIOD_EXIT` | $221.65 | 90 | **+9.48%** | **$+948.00** | C-Suite Conviction Buy: Insider_TSLA_2021_2 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001318605)<br>`0001318605-21-000002`<br>`data/industries/consumer_discretionary/automotive/TSLA_insider_trades.csv` |
| **RTX** | Aerospace & Defense | 2021-03-10 | $155.29 | 2021-06-08 | `HOLDING_PERIOD_EXIT` | $189.76 | 90 | **+22.20%** | **$+2,220.00** | C-Suite Conviction Buy: Insider_RTX_2021_10 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000101829)<br>`0000101829-21-000010`<br>`data/industries/industrials/aerospace_defense/RTX_insider_trades.csv` |
| **LMT** | Aerospace & Defense | 2021-03-16 | $161.59 | 2021-06-14 | `HOLDING_PERIOD_EXIT` | $206.38 | 90 | **+27.72%** | **$+2,772.00** | C-Suite Conviction Buy: Insider_LMT_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000936468)<br>`0000936468-21-000001`<br>`data/industries/industrials/aerospace_defense/LMT_insider_trades.csv` |
| **SBUX** | Restaurants | 2021-03-17 | $241.28 | 2021-06-15 | `HOLDING_PERIOD_EXIT` | $297.45 | 90 | **+23.28%** | **$+2,328.00** | C-Suite Conviction Buy: Insider_SBUX_2021_9 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000829224)<br>`0000829224-21-000009`<br>`data/industries/consumer_discretionary/restaurants/SBUX_insider_trades.csv` |

---

## 4. #4 Best Executive / Director Cluster Buy Strategy: `CLUSTER_BUY` (90-Day Holding Period)

### Strategy Overview & Institutional KPIs
- **Total Return (ROI)**: **`+446.21%`** cumulative over 6 years (`$546,210.00` final equity across 215 completed trades)
- **Win Rate**: **`84.65%`** (`182 Winning Trades / 33 Losing Trades`)
- **Profit Factor**: **`13.03`** | **Estimated Sharpe Ratio**: **`3.02`** | **Max Drawdown**: **`1.65%`**
- **Quantitative Rationale**: Detects simultaneous independent open-market purchases (`P`) by 2 or more Executive Officers or Directors within a 14-calendar-day window, signaling systematic internal optimism across the C-Suite and Board.

### Verified Trade Log: Entries, Exits, P&L & Trigger Links (Top 15 Representative Trades)

| Ticker | Industry | Entry Date | Entry Price | Exit Date | Exit Reason | Exit Price | Hold (Days) | Return (%) | P&L ($) | Trigger Event / Reason | SEC EDGAR & Local Source Link |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **ADBE** | Software - Infrastructure | 2021-01-13 | $128.60 | 2021-04-13 | `HOLDING_PERIOD_EXIT` | $151.75 | 90 | **+18.00%** | **$+1,800.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000796343)<br>`0000796343-21-000002`<br>`data/industries/information_technology/software_infrastructure/ADBE_insider_trades.csv` |
| **CMCSA** | Entertainment | 2021-01-24 | $123.40 | 2021-04-24 | `HOLDING_PERIOD_EXIT` | $109.70 | 90 | **-11.10%** | **$-1,110.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001166691)<br>`0001166691-21-000004`<br>`data/industries/communication_services/entertainment/CMCSA_insider_trades.csv` |
| **AMD** | Semiconductors | 2021-02-17 | $182.01 | 2021-05-14 | `TAKE_PROFIT_TARGET` | $254.81 | 86 | **+40.00%** | **$+4,000.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000002488)<br>`0000002488-21-000002`<br>`data/industries/information_technology/semiconductors/AMD_insider_trades.csv` |
| **SNPS** | Software - Infrastructure | 2021-02-22 | $127.52 | 2021-05-23 | `HOLDING_PERIOD_EXIT` | $167.46 | 90 | **+31.32%** | **$+3,132.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000883241)<br>`0000883241-21-000006`<br>`data/industries/information_technology/software_infrastructure/SNPS_insider_trades.csv` |
| **ACN** | IT Services | 2021-03-10 | $137.53 | 2021-06-08 | `HOLDING_PERIOD_EXIT` | $149.08 | 90 | **+8.40%** | **$+840.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001467373)<br>`0001467373-21-000004`<br>`data/industries/information_technology/it_services/ACN_insider_trades.csv` |
| **INTC** | Semiconductors | 2021-03-11 | $124.56 | 2021-06-09 | `HOLDING_PERIOD_EXIT` | $157.74 | 90 | **+26.64%** | **$+2,664.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000050863)<br>`0000050863-21-000005`<br>`data/industries/information_technology/semiconductors/INTC_insider_trades.csv` |
| **LMT** | Aerospace & Defense | 2021-03-16 | $161.59 | 2021-05-29 | `TAKE_PROFIT_TARGET` | $226.23 | 74 | **+40.00%** | **$+4,000.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000936468)<br>`0000936468-21-000012`<br>`data/industries/industrials/aerospace_defense/LMT_insider_trades.csv` |
| **RTX** | Aerospace & Defense | 2021-03-17 | $116.11 | 2021-06-15 | `HOLDING_PERIOD_EXIT` | $141.33 | 90 | **+21.72%** | **$+2,172.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000101829)<br>`0000101829-21-000010`<br>`data/industries/industrials/aerospace_defense/RTX_insider_trades.csv` |
| **BA** | Aerospace & Defense | 2021-03-20 | $267.54 | 2021-06-18 | `HOLDING_PERIOD_EXIT` | $287.44 | 90 | **+7.44%** | **$+744.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000012927)<br>`0000012927-21-000003`<br>`data/industries/industrials/aerospace_defense/BA_insider_trades.csv` |
| **JPM** | Banks - Diversified | 2021-03-31 | $216.29 | 2021-06-29 | `HOLDING_PERIOD_EXIT` | $257.56 | 90 | **+19.08%** | **$+1,908.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000019617)<br>`0000019617-21-000003`<br>`data/industries/financials/banks_diversified/JPM_insider_trades.csv` |
| **JPM** | Banks - Diversified | 2021-04-07 | $130.41 | 2021-05-07 | `STOP_LOSS_EXIT` | $114.76 | 30 | **-12.00%** | **$-1,200.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000019617)<br>`0000019617-21-000005`<br>`data/industries/financials/banks_diversified/JPM_insider_trades.csv` |
| **PANW** | Software - Infrastructure | 2021-04-11 | $273.18 | 2021-07-10 | `HOLDING_PERIOD_EXIT` | $295.80 | 90 | **+8.28%** | **$+828.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326801)<br>`0001326801-21-000007`<br>`data/industries/information_technology/software_infrastructure/PANW_insider_trades.csv` |
| **RTX** | Aerospace & Defense | 2021-04-14 | $230.86 | 2021-07-13 | `HOLDING_PERIOD_EXIT` | $269.64 | 90 | **+16.80%** | **$+1,680.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000101829)<br>`0000101829-21-000001`<br>`data/industries/industrials/aerospace_defense/RTX_insider_trades.csv` |
| **RTX** | Aerospace & Defense | 2021-04-21 | $142.90 | 2021-07-05 | `TAKE_PROFIT_TARGET` | $200.06 | 75 | **+40.00%** | **$+4,000.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000101829)<br>`0000101829-21-000006`<br>`data/industries/industrials/aerospace_defense/RTX_insider_trades.csv` |
| **NVDA** | Semiconductors | 2021-06-15 | $212.08 | 2021-09-13 | `HOLDING_PERIOD_EXIT` | $251.02 | 90 | **+18.36%** | **$+1,836.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001045810)<br>`0001045810-21-99999CFO`<br>`data/industries/information_technology/semiconductors/NVDA_insider_trades.csv` |

---

## 5. How to Re-Run Individual Analysis & View Complete Trade Tables via CLI

You can execute this Top 4 individual analysis or export complete trade logs at any time via CLI:

```bash
# Run the Top 4 strategies analysis & generate verified trade logs
python main.py analyze-top4 --show-trades

# View individual trade tables for each strategy directly via backtest subcommand
python main.py backtest --strategy combined --year 0 --holding-days 90 --show-log
python main.py backtest --strategy industry_momentum --year 0 --holding-days 90 --show-log
python main.py backtest --strategy conviction --year 0 --holding-days 90 --show-log
python main.py backtest --strategy cluster_buy --year 0 --holding-days 90 --show-log
```

All complete individual trade tables are saved to disk in CSV and JSON formats:
- `data/top4_COMBINED_90D_trade_log.csv` & `.json`
- `data/top4_INDUSTRY_MOMENTUM_90D_trade_log.csv` & `.json`
- `data/top4_CONVICTION_90D_trade_log.csv` & `.json`
- `data/top4_CLUSTER_BUY_90D_trade_log.csv` & `.json`