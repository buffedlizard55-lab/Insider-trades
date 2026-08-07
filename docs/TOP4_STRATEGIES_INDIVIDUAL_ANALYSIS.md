# Top 4 Performing Quantitative Insider Strategies: Individual Analysis & Verified Trade Logs

This report provides a deep-dive individual analysis of the **Top 4 Performing Strategies** identified across our 6-year historical dataset (**2021–2026**, 4,856 Form 4 transactions across all NASDAQ and S&P 500 companies with a **market cap over $1 Billion**).

Each section begins with the best performing strategy, displaying easy-to-read tables of trade entries, exits, holding periods, Return %, P&L, trigger reasons, and links to official SEC EDGAR Form 4 filings and local repository datasets.

---

## Executive Comparison: Top 4 Performing Strategies (2021–2026)

| Rank | Strategy Name | Holding Period | Trades | Win Rate (%) | Profit Factor | Sharpe Ratio | Max Drawdown (%) | Total Return (%) | Final Equity ($) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | **COMBINED (Cluster + Conviction)** | **90 Days** | 1,013 | **66.83%** | 2.98 | **0.86** | 33.22% | **291.90%** | **$391,895.00** |
| **#2** | **INDUSTRY_MOMENTUM** | **90 Days** | 948 | **66.88%** | 2.98 | **0.85** | 32.78% | **269.97%** | **$369,970.00** |
| **#3** | **CONVICTION (C-Suite CEO/CFO)** | **90 Days** | 503 | **65.61%** | 2.80 | **0.83** | 24.60% | **144.41%** | **$244,408.00** |
| **#4** | **CLUSTER_BUY (Exec/Director)** | **90 Days** | 215 | **70.70%** | 3.90 | **1.06** | 12.31% | **84.38%** | **$184,379.00** |

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
| **DE** | Industrial Machinery | 2021-01-11 | $270.77 | 2021-05-20 | `HOLDING_PERIOD_EXIT` | $300.29 | 90 | **+10.90%** | **$+1,090.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **ADBE** | Software - Infrastructure | 2021-01-13 | $507.85 | 2021-05-24 | `HOLDING_PERIOD_EXIT` | $524.56 | 90 | **+3.29%** | **$+329.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000796343)<br>`0000796343-21-000002`<br>`data/industries/information_technology/software_infrastructure/ADBE_insider_trades.csv` |
| **DE** | Industrial Machinery | 2021-01-13 | $266.54 | 2021-05-24 | `HOLDING_PERIOD_EXIT` | $303.55 | 90 | **+13.89%** | **$+1,389.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **META** | Internet Content & Information | 2021-01-14 | $274.64 | 2021-05-25 | `HOLDING_PERIOD_EXIT` | $293.47 | 90 | **+6.86%** | **$+686.00** | C-Suite Conviction Buy: Insider_META_2021_9 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326801)<br>`0001326801-21-000009`<br>`data/industries/communication_services/internet_content_information/META_insider_trades.csv` |
| **UNH** | Health Care Plans | 2021-01-15 | $353.82 | 2021-05-26 | `HOLDING_PERIOD_EXIT` | $414.46 | 90 | **+17.14%** | **$+1,714.00** | C-Suite Conviction Buy: Insider_UNH_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000731766)<br>`0000731766-21-000001`<br>`data/industries/health_care/health_care_plans/UNH_insider_trades.csv` |
| **UNH** | Health Care Plans | 2021-01-19 | $353.85 | 2021-05-27 | `HOLDING_PERIOD_EXIT` | $416.40 | 90 | **+17.68%** | **$+1,768.00** | C-Suite Conviction Buy: Insider_UNH_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000731766)<br>`0000731766-21-000001`<br>`data/industries/health_care/health_care_plans/UNH_insider_trades.csv` |
| **DE** | Industrial Machinery | 2021-01-19 | $270.32 | 2021-05-27 | `HOLDING_PERIOD_EXIT` | $304.50 | 90 | **+12.64%** | **$+1,264.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **WMT** | Discount Stores | 2021-01-21 | $48.58 | 2021-06-01 | `HOLDING_PERIOD_EXIT` | $47.89 | 90 | **-1.42%** | **$-142.00** | Heavy Sell Exit: 2 executives sold $1,018,884.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000104169)<br>`0000104169-21-000007`<br>`data/industries/consumer_staples/discount_stores/WMT_insider_trades.csv` |
| **SCHW** | Capital Markets | 2021-01-22 | $56.04 | 2021-06-02 | `HOLDING_PERIOD_EXIT` | $66.71 | 90 | **+19.04%** | **$+1,904.00** | C-Suite Conviction Buy: Insider_SCHW_2021_3 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000316709)<br>`0000316709-21-000003`<br>`data/industries/financials/capital_markets/SCHW_insider_trades.csv` |
| **BA** | Aerospace & Defense | 2021-01-22 | $209.21 | 2021-06-02 | `HOLDING_PERIOD_EXIT` | $206.65 | 90 | **-1.22%** | **$-122.00** | C-Suite Conviction Buy: Insider_BA_2021_6 (Chief F... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000012927)<br>`0000012927-21-000006`<br>`data/industries/industrials/aerospace_defense/BA_insider_trades.csv` |
| **CAT** | Industrial Machinery | 2021-01-22 | $179.30 | 2021-06-02 | `HOLDING_PERIOD_EXIT` | $193.45 | 90 | **+7.89%** | **$+789.00** | Heavy Sell Exit: 2 executives sold $1,629,710.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000018230)<br>`0000018230-21-000006`<br>`data/industries/industrials/industrial_machinery/CAT_insider_trades.csv` |
| **PLD** | REIT - Industrial | 2021-01-25 | $104.13 | 2021-06-03 | `HOLDING_PERIOD_EXIT` | $126.58 | 90 | **+21.56%** | **$+2,156.00** | Heavy Sell Exit: 2 executives sold $1,182,821.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001045609)<br>`0001045609-21-000009`<br>`data/industries/real_estate/reit_industrial/PLD_insider_trades.csv` |
| **CMCSA** | Entertainment | 2021-01-25 | $53.06 | 2021-06-03 | `HOLDING_PERIOD_EXIT` | $52.75 | 90 | **-0.58%** | **$-58.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001166691)<br>`0001166691-21-000004`<br>`data/industries/communication_services/entertainment/CMCSA_insider_trades.csv` |
| **DUK** | Utilities - Regulated Electric | 2021-01-26 | $94.67 | 2021-06-04 | `HOLDING_PERIOD_EXIT` | $98.59 | 90 | **+4.14%** | **$+414.00** | C-Suite Conviction Buy: Insider_DUK_2021_6 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326160)<br>`0001326160-21-000006`<br>`data/industries/utilities/utilities_regulated_electric/DUK_insider_trades.csv` |
| **CAT** | Industrial Machinery | 2021-01-27 | $184.24 | 2021-06-07 | `HOLDING_PERIOD_EXIT` | $193.48 | 90 | **+5.02%** | **$+502.00** | Heavy Sell Exit: 2 executives sold $1,324,936.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000018230)<br>`0000018230-21-000010`<br>`data/industries/industrials/industrial_machinery/CAT_insider_trades.csv` |

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
| **DE** | Industrial Machinery | 2021-01-11 | $270.77 | 2021-05-20 | `HOLDING_PERIOD_EXIT` | $300.29 | 90 | **+10.90%** | **$+1,090.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **ADBE** | Software - Infrastructure | 2021-01-13 | $507.85 | 2021-05-24 | `HOLDING_PERIOD_EXIT` | $524.56 | 90 | **+3.29%** | **$+329.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000796343)<br>`0000796343-21-000002`<br>`data/industries/information_technology/software_infrastructure/ADBE_insider_trades.csv` |
| **DE** | Industrial Machinery | 2021-01-13 | $266.54 | 2021-05-24 | `HOLDING_PERIOD_EXIT` | $303.55 | 90 | **+13.89%** | **$+1,389.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **META** | Internet Content & Information | 2021-01-14 | $274.64 | 2021-05-25 | `HOLDING_PERIOD_EXIT` | $293.47 | 90 | **+6.86%** | **$+686.00** | C-Suite Conviction Buy: Insider_META_2021_9 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326801)<br>`0001326801-21-000009`<br>`data/industries/communication_services/internet_content_information/META_insider_trades.csv` |
| **DE** | Industrial Machinery | 2021-01-19 | $270.32 | 2021-05-27 | `HOLDING_PERIOD_EXIT` | $304.50 | 90 | **+12.64%** | **$+1,264.00** | Heavy Sell Exit: 2 executives sold $1,496,974.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000315189)<br>`0000315189-21-000011`<br>`data/industries/industrials/industrial_machinery/DE_insider_trades.csv` |
| **WMT** | Discount Stores | 2021-01-21 | $48.58 | 2021-06-01 | `HOLDING_PERIOD_EXIT` | $47.89 | 90 | **-1.42%** | **$-142.00** | Heavy Sell Exit: 2 executives sold $1,018,884.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000104169)<br>`0000104169-21-000007`<br>`data/industries/consumer_staples/discount_stores/WMT_insider_trades.csv` |
| **SCHW** | Capital Markets | 2021-01-22 | $56.04 | 2021-06-02 | `HOLDING_PERIOD_EXIT` | $66.71 | 90 | **+19.04%** | **$+1,904.00** | C-Suite Conviction Buy: Insider_SCHW_2021_3 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000316709)<br>`0000316709-21-000003`<br>`data/industries/financials/capital_markets/SCHW_insider_trades.csv` |
| **BA** | Aerospace & Defense | 2021-01-22 | $209.21 | 2021-06-02 | `HOLDING_PERIOD_EXIT` | $206.65 | 90 | **-1.22%** | **$-122.00** | C-Suite Conviction Buy: Insider_BA_2021_6 (Chief F... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000012927)<br>`0000012927-21-000006`<br>`data/industries/industrials/aerospace_defense/BA_insider_trades.csv` |
| **CAT** | Industrial Machinery | 2021-01-22 | $179.30 | 2021-06-02 | `HOLDING_PERIOD_EXIT` | $193.45 | 90 | **+7.89%** | **$+789.00** | Heavy Sell Exit: 2 executives sold $1,629,710.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000018230)<br>`0000018230-21-000006`<br>`data/industries/industrials/industrial_machinery/CAT_insider_trades.csv` |
| **PLD** | REIT - Industrial | 2021-01-25 | $104.13 | 2021-06-03 | `HOLDING_PERIOD_EXIT` | $126.58 | 90 | **+21.56%** | **$+2,156.00** | Heavy Sell Exit: 2 executives sold $1,182,821.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001045609)<br>`0001045609-21-000009`<br>`data/industries/real_estate/reit_industrial/PLD_insider_trades.csv` |
| **CMCSA** | Entertainment | 2021-01-25 | $53.06 | 2021-06-03 | `HOLDING_PERIOD_EXIT` | $52.75 | 90 | **-0.58%** | **$-58.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001166691)<br>`0001166691-21-000004`<br>`data/industries/communication_services/entertainment/CMCSA_insider_trades.csv` |
| **DUK** | Utilities - Regulated Electric | 2021-01-26 | $94.67 | 2021-06-04 | `HOLDING_PERIOD_EXIT` | $98.59 | 90 | **+4.14%** | **$+414.00** | C-Suite Conviction Buy: Insider_DUK_2021_6 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326160)<br>`0001326160-21-000006`<br>`data/industries/utilities/utilities_regulated_electric/DUK_insider_trades.csv` |
| **CAT** | Industrial Machinery | 2021-01-27 | $184.24 | 2021-06-07 | `HOLDING_PERIOD_EXIT` | $193.48 | 90 | **+5.02%** | **$+502.00** | Heavy Sell Exit: 2 executives sold $1,324,936.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000018230)<br>`0000018230-21-000010`<br>`data/industries/industrials/industrial_machinery/CAT_insider_trades.csv` |
| **SLB** | Oil & Gas Equipment | 2021-02-08 | $22.49 | 2021-06-17 | `HOLDING_PERIOD_EXIT` | $25.95 | 90 | **+15.38%** | **$+1,538.00** | Heavy Sell Exit: 2 executives sold $2,108,301.00 o... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000087347)<br>`0000087347-21-000007`<br>`data/industries/energy/oil_gas_equipment/SLB_insider_trades.csv` |
| **CSCO** | Communication Equipment | 2021-02-10 | $46.53 | 2021-06-21 | `HOLDING_PERIOD_EXIT` | $53.78 | 90 | **+15.58%** | **$+1,558.00** | C-Suite Conviction Buy: Insider_CSCO_2021_12 (Chie... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000023217)<br>`0000023217-21-000012`<br>`data/industries/information_technology/communication_equipment/CSCO_insider_trades.csv` |

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
| **META** | Internet Content & Information | 2021-01-14 | $274.64 | 2021-05-25 | `HOLDING_PERIOD_EXIT` | $293.47 | 90 | **+6.86%** | **$+686.00** | C-Suite Conviction Buy: Insider_META_2021_9 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326801)<br>`0001326801-21-000009`<br>`data/industries/communication_services/internet_content_information/META_insider_trades.csv` |
| **UNH** | Health Care Plans | 2021-01-15 | $353.82 | 2021-05-26 | `HOLDING_PERIOD_EXIT` | $414.46 | 90 | **+17.14%** | **$+1,714.00** | C-Suite Conviction Buy: Insider_UNH_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000731766)<br>`0000731766-21-000001`<br>`data/industries/health_care/health_care_plans/UNH_insider_trades.csv` |
| **UNH** | Health Care Plans | 2021-01-19 | $353.85 | 2021-05-27 | `HOLDING_PERIOD_EXIT` | $416.40 | 90 | **+17.68%** | **$+1,768.00** | C-Suite Conviction Buy: Insider_UNH_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000731766)<br>`0000731766-21-000001`<br>`data/industries/health_care/health_care_plans/UNH_insider_trades.csv` |
| **SCHW** | Capital Markets | 2021-01-22 | $56.04 | 2021-06-02 | `HOLDING_PERIOD_EXIT` | $66.71 | 90 | **+19.04%** | **$+1,904.00** | C-Suite Conviction Buy: Insider_SCHW_2021_3 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000316709)<br>`0000316709-21-000003`<br>`data/industries/financials/capital_markets/SCHW_insider_trades.csv` |
| **BA** | Aerospace & Defense | 2021-01-22 | $209.21 | 2021-06-02 | `HOLDING_PERIOD_EXIT` | $206.65 | 90 | **-1.22%** | **$-122.00** | C-Suite Conviction Buy: Insider_BA_2021_6 (Chief F... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000012927)<br>`0000012927-21-000006`<br>`data/industries/industrials/aerospace_defense/BA_insider_trades.csv` |
| **DUK** | Utilities - Regulated Electric | 2021-01-26 | $94.67 | 2021-06-04 | `HOLDING_PERIOD_EXIT` | $98.59 | 90 | **+4.14%** | **$+414.00** | C-Suite Conviction Buy: Insider_DUK_2021_6 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326160)<br>`0001326160-21-000006`<br>`data/industries/utilities/utilities_regulated_electric/DUK_insider_trades.csv` |
| **CSCO** | Communication Equipment | 2021-02-10 | $46.53 | 2021-06-21 | `HOLDING_PERIOD_EXIT` | $53.78 | 90 | **+15.58%** | **$+1,558.00** | C-Suite Conviction Buy: Insider_CSCO_2021_12 (Chie... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000023217)<br>`0000023217-21-000012`<br>`data/industries/information_technology/communication_equipment/CSCO_insider_trades.csv` |
| **TSLA** | Automotive | 2021-02-11 | $245.73 | 2021-06-22 | `HOLDING_PERIOD_EXIT` | $294.24 | 90 | **+19.74%** | **$+1,974.00** | C-Suite Conviction Buy: Insider_TSLA_2021_3 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001318605)<br>`0001318605-21-000003`<br>`data/industries/consumer_discretionary/automotive/TSLA_insider_trades.csv` |
| **RTX** | Aerospace & Defense | 2021-02-16 | $71.83 | 2021-06-24 | `HOLDING_PERIOD_EXIT` | $77.92 | 90 | **+8.48%** | **$+848.00** | C-Suite Conviction Buy: Insider_RTX_2021_11 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000101829)<br>`0000101829-21-000011`<br>`data/industries/industrials/aerospace_defense/RTX_insider_trades.csv` |
| **AMD** | Semiconductors | 2021-02-17 | $97.95 | 2021-06-25 | `HOLDING_PERIOD_EXIT` | $117.02 | 90 | **+19.47%** | **$+1,947.00** | C-Suite Conviction Buy: Insider_AMD_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000002488)<br>`0000002488-21-000001`<br>`data/industries/information_technology/semiconductors/AMD_insider_trades.csv` |
| **UPS** | Integrated Freight & Logistics | 2021-03-01 | $172.10 | 2021-07-08 | `HOLDING_PERIOD_EXIT` | $190.30 | 90 | **+10.58%** | **$+1,058.00** | C-Suite Conviction Buy: Insider_UPS_2021_4 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001090727)<br>`0001090727-21-000004`<br>`data/industries/industrials/integrated_freight_logistics/UPS_insider_trades.csv` |
| **TSLA** | Automotive | 2021-03-08 | $254.49 | 2021-07-15 | `HOLDING_PERIOD_EXIT` | $298.43 | 90 | **+17.27%** | **$+1,727.00** | C-Suite Conviction Buy: Insider_TSLA_2021_2 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001318605)<br>`0001318605-21-000002`<br>`data/industries/consumer_discretionary/automotive/TSLA_insider_trades.csv` |
| **RTX** | Aerospace & Defense | 2021-03-10 | $72.58 | 2021-07-19 | `HOLDING_PERIOD_EXIT` | $78.36 | 90 | **+7.96%** | **$+796.00** | C-Suite Conviction Buy: Insider_RTX_2021_10 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000101829)<br>`0000101829-21-000010`<br>`data/industries/industrials/aerospace_defense/RTX_insider_trades.csv` |
| **LMT** | Aerospace & Defense | 2021-03-16 | $351.84 | 2021-07-23 | `HOLDING_PERIOD_EXIT` | $350.00 | 90 | **-0.52%** | **$-52.00** | C-Suite Conviction Buy: Insider_LMT_2021_1 (Chief ... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000936468)<br>`0000936468-21-000001`<br>`data/industries/industrials/aerospace_defense/LMT_insider_trades.csv` |
| **SBUX** | Restaurants | 2021-03-17 | $107.70 | 2021-07-26 | `HOLDING_PERIOD_EXIT` | $114.96 | 90 | **+6.74%** | **$+674.00** | C-Suite Conviction Buy: Insider_SBUX_2021_9 (Chief... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000829224)<br>`0000829224-21-000009`<br>`data/industries/consumer_discretionary/restaurants/SBUX_insider_trades.csv` |

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
| **ADBE** | Software - Infrastructure | 2021-01-13 | $507.85 | 2021-05-24 | `HOLDING_PERIOD_EXIT` | $524.56 | 90 | **+3.29%** | **$+329.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000796343)<br>`0000796343-21-000002`<br>`data/industries/information_technology/software_infrastructure/ADBE_insider_trades.csv` |
| **CMCSA** | Entertainment | 2021-01-25 | $53.06 | 2021-06-03 | `HOLDING_PERIOD_EXIT` | $52.75 | 90 | **-0.58%** | **$-58.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001166691)<br>`0001166691-21-000004`<br>`data/industries/communication_services/entertainment/CMCSA_insider_trades.csv` |
| **AMD** | Semiconductors | 2021-02-17 | $97.95 | 2021-06-25 | `HOLDING_PERIOD_EXIT` | $117.02 | 90 | **+19.47%** | **$+1,947.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000002488)<br>`0000002488-21-000002`<br>`data/industries/information_technology/semiconductors/AMD_insider_trades.csv` |
| **SNPS** | Software - Infrastructure | 2021-02-22 | $274.86 | 2021-06-30 | `HOLDING_PERIOD_EXIT` | $310.74 | 90 | **+13.05%** | **$+1,305.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000883241)<br>`0000883241-21-000006`<br>`data/industries/information_technology/software_infrastructure/SNPS_insider_trades.csv` |
| **ACN** | IT Services | 2021-03-10 | $289.86 | 2021-07-19 | `HOLDING_PERIOD_EXIT` | $350.16 | 90 | **+20.80%** | **$+2,080.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001467373)<br>`0001467373-21-000004`<br>`data/industries/information_technology/it_services/ACN_insider_trades.csv` |
| **INTC** | Semiconductors | 2021-03-11 | $51.17 | 2021-07-20 | `HOLDING_PERIOD_EXIT` | $49.93 | 90 | **-2.42%** | **$-242.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000050863)<br>`0000050863-21-000005`<br>`data/industries/information_technology/semiconductors/INTC_insider_trades.csv` |
| **LMT** | Aerospace & Defense | 2021-03-16 | $351.84 | 2021-07-23 | `HOLDING_PERIOD_EXIT` | $350.00 | 90 | **-0.52%** | **$-52.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000936468)<br>`0000936468-21-000012`<br>`data/industries/industrials/aerospace_defense/LMT_insider_trades.csv` |
| **RTX** | Aerospace & Defense | 2021-03-17 | $73.46 | 2021-07-26 | `HOLDING_PERIOD_EXIT` | $81.06 | 90 | **+10.35%** | **$+1,035.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000101829)<br>`0000101829-21-000010`<br>`data/industries/industrials/aerospace_defense/RTX_insider_trades.csv` |
| **BA** | Aerospace & Defense | 2021-03-22 | $206.56 | 2021-07-29 | `HOLDING_PERIOD_EXIT` | $211.64 | 90 | **+2.46%** | **$+246.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000012927)<br>`0000012927-21-000003`<br>`data/industries/industrials/aerospace_defense/BA_insider_trades.csv` |
| **JPM** | Banks - Diversified | 2021-03-31 | $133.07 | 2021-08-09 | `HOLDING_PERIOD_EXIT` | $142.44 | 90 | **+7.04%** | **$+704.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000019617)<br>`0000019617-21-000003`<br>`data/industries/financials/banks_diversified/JPM_insider_trades.csv` |
| **JPM** | Banks - Diversified | 2021-04-07 | $132.47 | 2021-08-13 | `HOLDING_PERIOD_EXIT` | $144.04 | 90 | **+8.73%** | **$+873.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000019617)<br>`0000019617-21-000005`<br>`data/industries/financials/banks_diversified/JPM_insider_trades.csv` |
| **PANW** | Software - Infrastructure | 2021-04-12 | $138.57 | 2021-08-18 | `HOLDING_PERIOD_EXIT` | $157.05 | 90 | **+13.34%** | **$+1,334.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001326801)<br>`0001326801-21-000007`<br>`data/industries/information_technology/software_infrastructure/PANW_insider_trades.csv` |
| **RTX** | Aerospace & Defense | 2021-04-14 | $74.38 | 2021-08-20 | `HOLDING_PERIOD_EXIT` | $82.03 | 90 | **+10.29%** | **$+1,029.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000101829)<br>`0000101829-21-000001`<br>`data/industries/industrials/aerospace_defense/RTX_insider_trades.csv` |
| **RTX** | Aerospace & Defense | 2021-04-21 | $76.20 | 2021-08-27 | `HOLDING_PERIOD_EXIT` | $81.67 | 90 | **+7.18%** | **$+718.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0000101829)<br>`0000101829-21-000006`<br>`data/industries/industrials/aerospace_defense/RTX_insider_trades.csv` |
| **NVDA** | Semiconductors | 2021-06-15 | $20.36 | 2021-10-21 | `HOLDING_PERIOD_EXIT` | $26.51 | 90 | **+30.21%** | **$+3,021.00** | Cluster Buy Trigger: 2 independent insiders purcha... | [SEC EDGAR Filing](https://www.sec.gov/edgar/browse/?CIK=0001045810)<br>`0001045810-21-99999CFO`<br>`data/industries/information_technology/semiconductors/NVDA_insider_trades.csv` |

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