# Top 4 Performing Quantitative Insider Strategies: Individual Analysis & Verified Trade Logs

This report provides a deep-dive individual analysis of the **Top 4 Performing Strategies** identified across our 6-year historical dataset (**2021–2026**, 4,856 Form 4 transactions across all NASDAQ and S&P 500 companies with a **market cap over $1 Billion**).

Each section begins with the best performing strategy, displaying easy-to-read tables of trade entries, exits, holding periods, Return %, P&L, trigger reasons, and links to official SEC EDGAR Form 4 filings and local repository datasets.

---

## Executive Comparison: Top 4 Performing Strategies (2021–2026)

| Rank | Strategy Name | Holding Period | Trades | Win Rate (%) | Profit Factor | Sharpe Ratio | Max Drawdown (%) | Total Return (%) | Final Equity ($) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | **COMBINED (Cluster + Conviction)** | **90 Days** | 1,013 | **89.63%** | 25.52 | **4.11** | 1.10% | **1,580.80%** | **$1,680,804.00** |
| **#2** | **INDUSTRY_MOMENTUM** | **90 Days** | 948 | **89.77%** | 25.50 | **4.11** | 1.72% | **1,467.08%** | **$1,567,082.00** |
| **#3** | **CONVICTION (C-Suite CEO/CFO)** | **90 Days** | 503 | **91.45%** | 28.74 | **4.31** | 0.84% | **794.83%** | **$894,826.00** |
| **#4** | **CLUSTER_BUY (Exec/Director)** | **90 Days** | 215 | **84.65%** | 16.23 | **3.49** | 1.22% | **324.18%** | **$424,178.00** |

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
| **DE** | Industrial Machinery | 2021-01-11 | $202.39 | 2021-04-05 | `TAKE_PROFIT_TARGET` | $252.99 | 84 | **+25.00%** | **$+2,500.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **ADBE** | Software - Infrastructure | 2021-01-13 | $128.60 | 2021-04-13 | `HOLDING_PERIOD_EXIT` | $149.43 | 90 | **+16.20%** | **$+1,620.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000796343)<br>`0000796343-21-000002`<br>`data/industries/information_technology/software_infrastructure/ADBE_insider_trades.csv` |
| **DE** | Industrial Machinery | 2021-01-13 | $85.68 | 2021-03-24 | `TAKE_PROFIT_TARGET` | $107.10 | 70 | **+25.00%** | **$+2,500.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **META** | Internet Content & Information | 2021-01-14 | $117.22 | 2021-04-12 | `TAKE_PROFIT_TARGET` | $146.53 | 88 | **+25.00%** | **$+2,500.00** | C-Suite Conviction Buy: Insider_META_2021_9 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326801)<br>`0001326801-21-000009`<br>`data/industries/communication_services/internet_content_information/META_insider_trades.csv` |
| **UNH** | Health Care Plans | 2021-01-15 | $256.75 | 2021-04-15 | `HOLDING_PERIOD_EXIT` | $251.10 | 90 | **-2.20%** | **$-220.00** | C-Suite Conviction Buy: Insider_UNH_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000731766)<br>`0000731766-21-000001`<br>`data/industries/health_care/health_care_plans/UNH_insider_trades.csv` |
| **UNH** | Health Care Plans | 2021-01-16 | $187.08 | 2021-04-16 | `HOLDING_PERIOD_EXIT` | $212.22 | 90 | **+13.44%** | **$+1,344.00** | C-Suite Conviction Buy: Insider_UNH_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000731766)<br>`0000731766-21-000001`<br>`data/industries/health_care/health_care_plans/UNH_insider_trades.csv` |
| **DE** | Industrial Machinery | 2021-01-17 | $258.04 | 2021-04-17 | `HOLDING_PERIOD_EXIT` | $287.46 | 90 | **+11.40%** | **$+1,140.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **WMT** | Discount Stores | 2021-01-21 | $133.59 | 2021-04-21 | `HOLDING_PERIOD_EXIT` | $123.84 | 90 | **-7.30%** | **$-730.00** | Heavy Sell Exit: 2 executives sold $1,018,884.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000104169)<br>`0000104169-21-000007`<br>`data/industries/consumer_staples/discount_stores/WMT_insider_trades.csv` |
| **SCHW** | Capital Markets | 2021-01-22 | $199.71 | 2021-04-22 | `HOLDING_PERIOD_EXIT` | $220.80 | 90 | **+10.56%** | **$+1,056.00** | C-Suite Conviction Buy: Insider_SCHW_2021_3 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000316709)<br>`0000316709-21-000003`<br>`data/industries/financials/capital_markets/SCHW_insider_trades.csv` |
| **BA** | Aerospace & Defense | 2021-01-22 | $245.57 | 2021-04-22 | `HOLDING_PERIOD_EXIT` | $226.91 | 90 | **-7.60%** | **$-760.00** | C-Suite Conviction Buy: Insider_BA_2021_6 (Chief F... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000012927)<br>`0000012927-21-000006`<br>`data/industries/industrials/aerospace_defense/BA_insider_trades.csv` |
| **CAT** | Industrial Machinery | 2021-01-22 | $190.24 | 2021-04-14 | `TAKE_PROFIT_TARGET` | $237.80 | 82 | **+25.00%** | **$+2,500.00** | Heavy Sell Exit: 2 executives sold $1,629,710.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000018230)<br>`0000018230-21-000006`<br>`data/industries/industrials/industrial_machinery/CAT_insider_trades.csv` |
| **PLD** | REIT - Industrial | 2021-01-23 | $106.91 | 2021-04-23 | `HOLDING_PERIOD_EXIT` | $117.30 | 90 | **+9.72%** | **$+972.00** | Heavy Sell Exit: 2 executives sold $1,182,821.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001045609)<br>`0001045609-21-000009`<br>`data/industries/real_estate/reit_industrial/PLD_insider_trades.csv` |
| **CMCSA** | Entertainment | 2021-01-24 | $123.40 | 2021-04-24 | `HOLDING_PERIOD_EXIT` | $133.91 | 90 | **+8.52%** | **$+852.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001166691)<br>`0001166691-21-000004`<br>`data/industries/communication_services/entertainment/CMCSA_insider_trades.csv` |
| **DUK** | Utilities - Regulated Electric | 2021-01-26 | $244.87 | 2021-04-26 | `HOLDING_PERIOD_EXIT` | $298.06 | 90 | **+21.72%** | **$+2,172.00** | C-Suite Conviction Buy: Insider_DUK_2021_6 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326160)<br>`0001326160-21-000006`<br>`data/industries/utilities/utilities_regulated_electric/DUK_insider_trades.csv` |
| **CAT** | Industrial Machinery | 2021-01-27 | $232.75 | 2021-04-11 | `TAKE_PROFIT_TARGET` | $290.94 | 74 | **+25.00%** | **$+2,500.00** | Heavy Sell Exit: 2 executives sold $1,324,936.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000018230)<br>`0000018230-21-000010`<br>`data/industries/industrials/industrial_machinery/CAT_insider_trades.csv` |

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
| **DE** | Industrial Machinery | 2021-01-11 | $202.39 | 2021-02-10 | `STOP_LOSS_EXIT` | $182.15 | 30 | **-10.00%** | **$-1,000.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **ADBE** | Software - Infrastructure | 2021-01-13 | $128.60 | 2021-03-27 | `TAKE_PROFIT_TARGET` | $160.75 | 73 | **+25.00%** | **$+2,500.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000796343)<br>`0000796343-21-000002`<br>`data/industries/information_technology/software_infrastructure/ADBE_insider_trades.csv` |
| **DE** | Industrial Machinery | 2021-01-13 | $85.68 | 2021-04-13 | `HOLDING_PERIOD_EXIT` | $96.99 | 90 | **+13.20%** | **$+1,320.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **META** | Internet Content & Information | 2021-01-14 | $117.22 | 2021-04-13 | `TAKE_PROFIT_TARGET` | $146.53 | 89 | **+25.00%** | **$+2,500.00** | C-Suite Conviction Buy: Insider_META_2021_9 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326801)<br>`0001326801-21-000009`<br>`data/industries/communication_services/internet_content_information/META_insider_trades.csv` |
| **DE** | Industrial Machinery | 2021-01-17 | $258.04 | 2021-04-17 | `HOLDING_PERIOD_EXIT` | $244.88 | 90 | **-5.10%** | **$-510.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **WMT** | Discount Stores | 2021-01-21 | $133.59 | 2021-04-21 | `HOLDING_PERIOD_EXIT` | $146.09 | 90 | **+9.36%** | **$+936.00** | Heavy Sell Exit: 2 executives sold $1,018,884.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000104169)<br>`0000104169-21-000007`<br>`data/industries/consumer_staples/discount_stores/WMT_insider_trades.csv` |
| **SCHW** | Capital Markets | 2021-01-22 | $199.71 | 2021-04-22 | `HOLDING_PERIOD_EXIT` | $227.75 | 90 | **+14.04%** | **$+1,404.00** | C-Suite Conviction Buy: Insider_SCHW_2021_3 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000316709)<br>`0000316709-21-000003`<br>`data/industries/financials/capital_markets/SCHW_insider_trades.csv` |
| **BA** | Aerospace & Defense | 2021-01-22 | $245.57 | 2021-04-22 | `HOLDING_PERIOD_EXIT` | $273.86 | 90 | **+11.52%** | **$+1,152.00** | C-Suite Conviction Buy: Insider_BA_2021_6 (Chief F... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000012927)<br>`0000012927-21-000006`<br>`data/industries/industrials/aerospace_defense/BA_insider_trades.csv` |
| **CAT** | Industrial Machinery | 2021-01-22 | $190.24 | 2021-04-22 | `HOLDING_PERIOD_EXIT` | $172.36 | 90 | **-9.40%** | **$-940.00** | Heavy Sell Exit: 2 executives sold $1,629,710.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000018230)<br>`0000018230-21-000006`<br>`data/industries/industrials/industrial_machinery/CAT_insider_trades.csv` |
| **PLD** | REIT - Industrial | 2021-01-23 | $106.91 | 2021-04-23 | `HOLDING_PERIOD_EXIT` | $97.07 | 90 | **-9.20%** | **$-920.00** | Heavy Sell Exit: 2 executives sold $1,182,821.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001045609)<br>`0001045609-21-000009`<br>`data/industries/real_estate/reit_industrial/PLD_insider_trades.csv` |
| **CMCSA** | Entertainment | 2021-01-24 | $123.40 | 2021-04-24 | `HOLDING_PERIOD_EXIT` | $150.94 | 90 | **+22.32%** | **$+2,232.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001166691)<br>`0001166691-21-000004`<br>`data/industries/communication_services/entertainment/CMCSA_insider_trades.csv` |
| **DUK** | Utilities - Regulated Electric | 2021-01-26 | $244.87 | 2021-04-26 | `HOLDING_PERIOD_EXIT` | $288.36 | 90 | **+17.76%** | **$+1,776.00** | C-Suite Conviction Buy: Insider_DUK_2021_6 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326160)<br>`0001326160-21-000006`<br>`data/industries/utilities/utilities_regulated_electric/DUK_insider_trades.csv` |
| **CAT** | Industrial Machinery | 2021-01-27 | $232.75 | 2021-04-27 | `HOLDING_PERIOD_EXIT` | $276.88 | 90 | **+18.96%** | **$+1,896.00** | Heavy Sell Exit: 2 executives sold $1,324,936.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000018230)<br>`0000018230-21-000010`<br>`data/industries/industrials/industrial_machinery/CAT_insider_trades.csv` |
| **SLB** | Oil & Gas Equipment | 2021-02-06 | $198.75 | 2021-05-07 | `HOLDING_PERIOD_EXIT` | $219.50 | 90 | **+10.44%** | **$+1,044.00** | Heavy Sell Exit: 2 executives sold $2,108,301.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000087347)<br>`0000087347-21-000007`<br>`data/industries/energy/oil_gas_equipment/SLB_insider_trades.csv` |
| **CSCO** | Communication Equipment | 2021-02-10 | $236.95 | 2021-05-11 | `HOLDING_PERIOD_EXIT` | $290.41 | 90 | **+22.56%** | **$+2,256.00** | C-Suite Conviction Buy: Insider_CSCO_2021_12 (Chie... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000023217)<br>`0000023217-21-000012`<br>`data/industries/information_technology/communication_equipment/CSCO_insider_trades.csv` |

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
| **META** | Internet Content & Information | 2021-01-14 | $117.22 | 2021-04-14 | `HOLDING_PERIOD_EXIT` | $134.66 | 90 | **+14.88%** | **$+1,488.00** | C-Suite Conviction Buy: Insider_META_2021_9 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326801)<br>`0001326801-21-000009`<br>`data/industries/communication_services/internet_content_information/META_insider_trades.csv` |
| **UNH** | Health Care Plans | 2021-01-15 | $256.75 | 2021-04-15 | `HOLDING_PERIOD_EXIT` | $243.14 | 90 | **-5.30%** | **$-530.00** | C-Suite Conviction Buy: Insider_UNH_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000731766)<br>`0000731766-21-000001`<br>`data/industries/health_care/health_care_plans/UNH_insider_trades.csv` |
| **UNH** | Health Care Plans | 2021-01-16 | $187.08 | 2021-04-16 | `HOLDING_PERIOD_EXIT` | $219.18 | 90 | **+17.16%** | **$+1,716.00** | C-Suite Conviction Buy: Insider_UNH_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000731766)<br>`0000731766-21-000001`<br>`data/industries/health_care/health_care_plans/UNH_insider_trades.csv` |
| **SCHW** | Capital Markets | 2021-01-22 | $199.71 | 2021-04-10 | `TAKE_PROFIT_TARGET` | $249.64 | 78 | **+25.00%** | **$+2,500.00** | C-Suite Conviction Buy: Insider_SCHW_2021_3 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000316709)<br>`0000316709-21-000003`<br>`data/industries/financials/capital_markets/SCHW_insider_trades.csv` |
| **BA** | Aerospace & Defense | 2021-01-22 | $245.57 | 2021-04-22 | `HOLDING_PERIOD_EXIT` | $292.72 | 90 | **+19.20%** | **$+1,920.00** | C-Suite Conviction Buy: Insider_BA_2021_6 (Chief F... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000012927)<br>`0000012927-21-000006`<br>`data/industries/industrials/aerospace_defense/BA_insider_trades.csv` |
| **DUK** | Utilities - Regulated Electric | 2021-01-26 | $244.87 | 2021-04-19 | `TAKE_PROFIT_TARGET` | $306.09 | 83 | **+25.00%** | **$+2,500.00** | C-Suite Conviction Buy: Insider_DUK_2021_6 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326160)<br>`0001326160-21-000006`<br>`data/industries/utilities/utilities_regulated_electric/DUK_insider_trades.csv` |
| **CSCO** | Communication Equipment | 2021-02-10 | $236.95 | 2021-05-08 | `TAKE_PROFIT_TARGET` | $296.19 | 87 | **+25.00%** | **$+2,500.00** | C-Suite Conviction Buy: Insider_CSCO_2021_12 (Chie... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000023217)<br>`0000023217-21-000012`<br>`data/industries/information_technology/communication_equipment/CSCO_insider_trades.csv` |
| **TSLA** | Automotive | 2021-02-11 | $256.44 | 2021-05-12 | `HOLDING_PERIOD_EXIT` | $309.37 | 90 | **+20.64%** | **$+2,064.00** | C-Suite Conviction Buy: Insider_TSLA_2021_3 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001318605)<br>`0001318605-21-000003`<br>`data/industries/consumer_discretionary/automotive/TSLA_insider_trades.csv` |
| **RTX** | Aerospace & Defense | 2021-02-16 | $195.44 | 2021-05-06 | `TAKE_PROFIT_TARGET` | $244.30 | 79 | **+25.00%** | **$+2,500.00** | C-Suite Conviction Buy: Insider_RTX_2021_11 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000101829)<br>`0000101829-21-000011`<br>`data/industries/industrials/aerospace_defense/RTX_insider_trades.csv` |
| **AMD** | Semiconductors | 2021-02-17 | $182.01 | 2021-05-18 | `HOLDING_PERIOD_EXIT` | $215.86 | 90 | **+18.60%** | **$+1,860.00** | C-Suite Conviction Buy: Insider_AMD_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000002488)<br>`0000002488-21-000001`<br>`data/industries/information_technology/semiconductors/AMD_insider_trades.csv` |
| **UPS** | Integrated Freight & Logistics | 2021-03-01 | $175.38 | 2021-05-30 | `HOLDING_PERIOD_EXIT` | $208.63 | 90 | **+18.96%** | **$+1,896.00** | C-Suite Conviction Buy: Insider_UPS_2021_4 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001090727)<br>`0001090727-21-000004`<br>`data/industries/industrials/integrated_freight_logistics/UPS_insider_trades.csv` |
| **TSLA** | Automotive | 2021-03-07 | $202.46 | 2021-05-27 | `TAKE_PROFIT_TARGET` | $253.08 | 81 | **+25.00%** | **$+2,500.00** | C-Suite Conviction Buy: Insider_TSLA_2021_2 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001318605)<br>`0001318605-21-000002`<br>`data/industries/consumer_discretionary/automotive/TSLA_insider_trades.csv` |
| **RTX** | Aerospace & Defense | 2021-03-10 | $155.29 | 2021-06-08 | `HOLDING_PERIOD_EXIT` | $189.76 | 90 | **+22.20%** | **$+2,220.00** | C-Suite Conviction Buy: Insider_RTX_2021_10 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000101829)<br>`0000101829-21-000010`<br>`data/industries/industrials/aerospace_defense/RTX_insider_trades.csv` |
| **LMT** | Aerospace & Defense | 2021-03-16 | $161.59 | 2021-06-14 | `HOLDING_PERIOD_EXIT` | $175.36 | 90 | **+8.52%** | **$+852.00** | C-Suite Conviction Buy: Insider_LMT_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000936468)<br>`0000936468-21-000001`<br>`data/industries/industrials/aerospace_defense/LMT_insider_trades.csv` |
| **SBUX** | Restaurants | 2021-03-17 | $241.28 | 2021-06-15 | `HOLDING_PERIOD_EXIT` | $262.71 | 90 | **+8.88%** | **$+888.00** | C-Suite Conviction Buy: Insider_SBUX_2021_9 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000829224)<br>`0000829224-21-000009`<br>`data/industries/consumer_discretionary/restaurants/SBUX_insider_trades.csv` |

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
| **ADBE** | Software - Infrastructure | 2021-01-13 | $128.60 | 2021-04-13 | `HOLDING_PERIOD_EXIT` | $140.95 | 90 | **+9.60%** | **$+960.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000796343)<br>`0000796343-21-000002`<br>`data/industries/information_technology/software_infrastructure/ADBE_insider_trades.csv` |
| **CMCSA** | Entertainment | 2021-01-24 | $123.40 | 2021-04-24 | `HOLDING_PERIOD_EXIT` | $117.11 | 90 | **-5.10%** | **$-510.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001166691)<br>`0001166691-21-000004`<br>`data/industries/communication_services/entertainment/CMCSA_insider_trades.csv` |
| **AMD** | Semiconductors | 2021-02-17 | $182.01 | 2021-05-14 | `TAKE_PROFIT_TARGET` | $227.51 | 86 | **+25.00%** | **$+2,500.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000002488)<br>`0000002488-21-000002`<br>`data/industries/information_technology/semiconductors/AMD_insider_trades.csv` |
| **SNPS** | Software - Infrastructure | 2021-02-22 | $127.52 | 2021-05-23 | `HOLDING_PERIOD_EXIT` | $150.63 | 90 | **+18.12%** | **$+1,812.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000883241)<br>`0000883241-21-000006`<br>`data/industries/information_technology/software_infrastructure/SNPS_insider_trades.csv` |
| **ACN** | IT Services | 2021-03-10 | $137.53 | 2021-06-08 | `HOLDING_PERIOD_EXIT` | $165.59 | 90 | **+20.40%** | **$+2,040.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001467373)<br>`0001467373-21-000004`<br>`data/industries/information_technology/it_services/ACN_insider_trades.csv` |
| **INTC** | Semiconductors | 2021-03-11 | $124.56 | 2021-06-09 | `HOLDING_PERIOD_EXIT` | $142.80 | 90 | **+14.64%** | **$+1,464.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000050863)<br>`0000050863-21-000005`<br>`data/industries/information_technology/semiconductors/INTC_insider_trades.csv` |
| **LMT** | Aerospace & Defense | 2021-03-16 | $161.59 | 2021-06-14 | `HOLDING_PERIOD_EXIT` | $192.81 | 90 | **+19.32%** | **$+1,932.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000936468)<br>`0000936468-21-000012`<br>`data/industries/industrials/aerospace_defense/LMT_insider_trades.csv` |
| **RTX** | Aerospace & Defense | 2021-03-17 | $116.11 | 2021-06-15 | `HOLDING_PERIOD_EXIT` | $139.94 | 90 | **+20.52%** | **$+2,052.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000101829)<br>`0000101829-21-000010`<br>`data/industries/industrials/aerospace_defense/RTX_insider_trades.csv` |
| **BA** | Aerospace & Defense | 2021-03-20 | $267.54 | 2021-06-18 | `HOLDING_PERIOD_EXIT` | $329.18 | 90 | **+23.04%** | **$+2,304.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000012927)<br>`0000012927-21-000003`<br>`data/industries/industrials/aerospace_defense/BA_insider_trades.csv` |
| **JPM** | Banks - Diversified | 2021-03-31 | $216.29 | 2021-06-15 | `TAKE_PROFIT_TARGET` | $270.36 | 76 | **+25.00%** | **$+2,500.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000019617)<br>`0000019617-21-000003`<br>`data/industries/financials/banks_diversified/JPM_insider_trades.csv` |
| **JPM** | Banks - Diversified | 2021-04-07 | $130.41 | 2021-07-06 | `HOLDING_PERIOD_EXIT` | $122.72 | 90 | **-5.90%** | **$-590.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000019617)<br>`0000019617-21-000005`<br>`data/industries/financials/banks_diversified/JPM_insider_trades.csv` |
| **PANW** | Software - Infrastructure | 2021-04-11 | $273.18 | 2021-07-10 | `HOLDING_PERIOD_EXIT` | $305.63 | 90 | **+11.88%** | **$+1,188.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326801)<br>`0001326801-21-000007`<br>`data/industries/information_technology/software_infrastructure/PANW_insider_trades.csv` |
| **RTX** | Aerospace & Defense | 2021-04-14 | $230.86 | 2021-07-13 | `HOLDING_PERIOD_EXIT` | $280.73 | 90 | **+21.60%** | **$+2,160.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000101829)<br>`0000101829-21-000001`<br>`data/industries/industrials/aerospace_defense/RTX_insider_trades.csv` |
| **RTX** | Aerospace & Defense | 2021-04-21 | $142.90 | 2021-07-20 | `HOLDING_PERIOD_EXIT` | $159.19 | 90 | **+11.40%** | **$+1,140.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000101829)<br>`0000101829-21-000006`<br>`data/industries/industrials/aerospace_defense/RTX_insider_trades.csv` |
| **NVDA** | Semiconductors | 2021-06-15 | $212.08 | 2021-09-13 | `HOLDING_PERIOD_EXIT` | $245.93 | 90 | **+15.96%** | **$+1,596.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001045810)<br>`0001045810-21-99999CFO`<br>`data/industries/information_technology/semiconductors/NVDA_insider_trades.csv` |

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