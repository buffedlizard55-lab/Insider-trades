# Verifiable, Trustworthy, Official & Up-to-Date Insider Trading Data Sources

The **first and most important foundation** of quantitative insider trade analysis is establishing an **official, verifiable, trustworthy, and real-time source of truth**. Secondary aggregators often introduce scraping lag, data omissions, or parsing errors. 

This document details the authoritative source of publicly available insider transactions in the United States, regulatory requirements, schema definitions, and programmatic access protocols implemented in this repository.

---

## 1. The Official Primary Source: SEC EDGAR Form 4 Filings

In the United States, the single verifiable, legally mandated source for insider transactions at publicly traded companies (NASDAQ and S&P 500) is the **U.S. Securities and Exchange Commission (SEC) Electronic Data Gathering, Analysis, and Retrieval (EDGAR) system**.

### 1.1 Regulatory Mandate: Section 16(a) of the Exchange Act
Under Section 16(a) of the **Securities Exchange Act of 1934**, corporate insiders are legally required to report transactions in their company's equity securities to the SEC.

- **Who is defined as an Insider?**
  1. **Officers**: Executive officers including Chief Executive Officer (CEO), Chief Financial Officer (CFO), Chief Operating Officer (COO), General Counsel, and Vice Presidents in charge of principal business units.
  2. **Directors**: Members of the company's Board of Directors.
  3. **10% Beneficial Owners**: Individuals or entities holding more than 10% of any class of the company's registered equity securities.
  4. **Other Section 16 Insiders**: Affiliates or beneficial owners subject to Section 16 reporting.

- **Strict Two-Business-Day Deadline**:
  Since the enactment of the Sarbanes-Oxley Act of 2002 (SOX Section 403), insiders must file a **Form 4** with the SEC **within two business days** of the transaction date. This rapid reporting window ensures that Form 4 filings are an **up-to-date, actionable signal** for market participants.

---

## 2. SEC EDGAR Technical Architecture & API Endpoints

The SEC provides free public programmatic access to EDGAR filings via structured XML and JSON APIs. Our pipeline connects directly to these official endpoints.

### 2.1 Official SEC Endpoints Used by Our Collector
1. **EDGAR RSS & Electronic Filing Transfer System (EFTS) Real-Time Feed**:
   - URL: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=4&output=atom`
   - Provides real-time Atom/RSS feeds of new Form 4 filings as soon as they are submitted to EDGAR.
2. **SEC EDGAR Submissions API**:
   - URL: `https://data.sec.gov/submissions/CIK{cik_10_digits}.json`
   - Returns complete filing history and metadata for any company identified by its 10-digit Central Index Key (CIK).
3. **SEC EDGAR Daily Archive Index**:
   - URL: `https://www.sec.gov/Archives/edgar/daily-index/`
   - Provides official daily master indexes of all filings submitted on any given business day.
4. **SEC Official Company Ticker-to-CIK Mapping**:
   - URL: `https://www.sec.gov/files/company_tickers.json` and `company_tickers_exchange.json`
   - Authoritative mapping between stock ticker symbols (e.g., `AAPL`, `NVDA`), CIK numbers, and stock exchanges (`NASDAQ`, `NYSE`).

### 2.2 SEC Rate Limiting & User-Agent Compliance
The SEC enforces strict programmatic access guidelines:
- **Custom User-Agent Header**: Every HTTP request must include a clearly identifiable `User-Agent` string declaring the application name and administrative contact email:
  ```http
  User-Agent: ArenaInsiderTracker/1.0 (contact@arena.ai)
  ```
- **Rate Limit**: Automated clients must not exceed **10 requests per second** across `www.sec.gov` and `data.sec.gov`. Our client (`EdgarClient`) implements a token-bucket rate limiter and automatic exponential backoff on `429 Too Many Requests` responses.

---

## 3. SEC Form 4 XML Schema (`ownershipDocument`)

Unlike unstructured text or PDF reports, SEC Form 4 filings are submitted as **structured XML documents** adhering to the official SEC EDGAR XML DTD (`https://www.sec.gov/info/edgar/forms/edgform.pdf`).

### 3.1 Key XML Schema Elements Extracted by Our Parser
An SEC Form 4 XML document (`<ownershipDocument>`) contains three critical sections:

1. **Issuer Identification (`<issuer>`)**:
   - `<issuerCik>`: SEC Central Index Key of the company.
   - `<issuerName>`: Registered corporate name.
   - `<issuerTradingSymbol>`: Ticker symbol on NASDAQ/NYSE.
2. **Reporting Owner (`<reportingOwner>`)**:
   - `<reportingOwnerId>`: Contains `<rptOwnerCik>` and `<rptOwnerName>`.
   - `<reportingOwnerRelationship>`: Flags indicating insider status (`<isDirector>`, `<isOfficer>`, `<isTenPercentOwner>`, `<isOther>`) and specific title (`<officerTitle>`, e.g., "Chief Executive Officer").
3. **Transactions Table (`<nonDerivativeTable>` & `<derivativeTable>`)**:
   - `<nonDerivativeTransaction>` / `<derivativeTransaction>`:
     - `<securityTitle>`: e.g., "Common Stock".
     - `<transactionDate>`: Official date the trade occurred.
     - `<transactionCoding>`:
       - `<transactionFormType>`: Form 4.
       - `<transactionCode>`: One-character transaction code (**critical for strategy signal filtering**).
     - `<transactionAmounts>`:
       - `<transactionShares>`: Number of shares transacted.
       - `<transactionPricePerShare>`: Executed dollar price per share.
       - `<transactionAcquiredDisposedCode>`: `A` (Acquired/Buy) or `D` (Disposed/Sell).
     - `<postTransactionAmounts>`:
       - `<sharesOwnedFollowingTransaction>`: Insider's remaining equity balance after the trade.
     - `<ownershipNature>`:
       - `<directOrIndirectOwnership>`: `D` (Direct) or `I` (Indirect, e.g., family trust or LLC).

---

## 4. Understanding SEC Form 4 Transaction Codes

A common pitfall in quantitative insider analysis is treating all Form 4 transactions equally. **Not all insider transactions represent discretionary market conviction.** Our parser classifies trades using the official SEC transaction codes:

| Code | Type | Description | Quantitative Interpretation |
| :--- | :--- | :--- | :--- |
| **`P`** | **Open Market Buy** | Open-market or private purchase of non-derivative or derivative security | **Strongest Bullish Signal**: Insiders putting their own capital at risk. |
| **`S`** | **Open Market Sell** | Open-market or private sale of non-derivative or derivative security | **Bearish/Exit Signal**: Selling shares for cash on the open market. Note: Must be evaluated for cluster/volume severity. |
| **`A`** | Grant / Award | Award or grant of stock or options from the issuer (Rule 16b-3(d)) | **Neutral**: Executive compensation; does not indicate discretionary market timing. |
| **`M`** | Option Exercise | Exercise or conversion of derivative security exempted pursuant to Rule 16b-3 | **Neutral**: Often paired with a same-day sale (`S`) or tax withholding (`F`). |
| **`F`** | Tax Withholding | Payment of exercise price or tax liability by delivering or withholding shares | **Neutral**: Non-discretionary tax withholding upon option vesting. |
| **`G`** | Gift | Bona fide gift of securities | **Neutral**: Estate planning or charitable donation. |
| **`D`** | Issuer Return | Disposition to the issuer of issuer equity securities pursuant to Rule 16b-3(e) | **Neutral**: Corporate redemption or buyback mechanics. |

### 4.1 Focusing on Conviction: Why `P` and `S` Matter
For strategy entry and exit modeling, our pipeline isolates discretionary open-market transactions (**Code `P`** for open-market purchases and **Code `S`** for open-market sales), filtering out routine stock awards (`A`), automatic option exercises (`M`), and tax withholdings (`F`).

---

## 5. Complementary & Secondary Market Data Sources

To classify companies into GICS sectors and industries and to benchmark trading signals, our system integrates the following official universes:

1. **NASDAQ & S&P 500 Constituent Mapping**:
   - Combines official NASDAQ-100 and S&P 500 membership lists.
   - Every ticker is mapped to its **10-digit CIK**, **Stock Exchange** (`NASDAQ` or `NYSE`), **GICS Sector** (11 sectors), and **GICS Industry** (50+ specific industries).
2. **Industry-Organized Filesystem Architecture**:
   - Rather than storing insider trades in a monolithic database, all parsed transactions are partitioned by sector and industry inside `data/industries/{sector_slug}/{industry_slug}/{ticker}_insider_trades.csv`.
   - This architecture allows quantitative researchers to run cross-sectional industry sentiment heatmaps, sector rotation backtests, and peer-relative conviction scores effortlessly.
