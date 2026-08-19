# Official insider-trading data sources

This project uses **only** public U.S. government sources for insider
transactions and company identifiers. Secondary scrapers are not the source of
truth.

---

## 1. Primary source: SEC EDGAR Form 4

The legally required public report of a Section 16 insider’s change in
beneficial ownership is **SEC Form 4**, published through EDGAR.

### 1.1 Who must file

Under **Section 16(a) of the Securities Exchange Act of 1934**, reports are
required of:

1. Officers of the issuer
2. Directors
3. Beneficial owners of more than 10% of a class of registered equity securities

Official form and instructions: <https://www.sec.gov/files/form4.pdf>

### 1.2 Filing deadline

**Section 403 of the Sarbanes-Oxley Act of 2002** amended Section 16(a) so that
most Form 4 filings must be submitted **before the end of the second business
day** following the day of the transaction. The SEC implemented that deadline
effective 29 August 2002. See the Form 4 general instructions and
[SEC Release 33-8230](https://www.sec.gov/files/rules/final/33-8230.htm).

### 1.3 Structured XML

Modern Form 4 filings include an `ownershipDocument` XML instance (current
schema family `X0606` / `X0609`). This repo’s parser reads that XML; it does
not invent fields.

---

## 2. Official endpoints used by the collector

Documented on [SEC Developer Resources](https://www.sec.gov/about/developer-resources)
and [Accessing EDGAR Data](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data):

| Resource | Official URL |
| :--- | :--- |
| Latest filings Atom feed (filter `type=4`) | `https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=4&output=atom` |
| Company submissions JSON | `https://data.sec.gov/submissions/CIK##########.json` |
| Daily EDGAR indexes | `https://www.sec.gov/Archives/edgar/daily-index/` |
| Ticker / CIK / title map | `https://www.sec.gov/files/company_tickers.json` |
| Ticker / CIK / exchange map | `https://www.sec.gov/files/company_tickers_exchange.json` |
| Individual filing archive | `https://www.sec.gov/Archives/edgar/data/{cik}/{accession_nodash}/` |

CIKs in `data/universe/nasdaq_sp500_universe.csv` were checked against
`company_tickers.json` and EDGAR company search on **2026-08-18**.

---

## 3. Fair access (User-Agent and rate limit)

From [Developer Resources — Fair Access](https://www.sec.gov/about/developer-resources):

> Current guidelines limit each user to a total of no more than **10 requests
> per second**, regardless of the number of machines used to submit requests.

From the [Webmaster FAQ](https://www.sec.gov/about/webmaster-frequently-asked-questions#user-agent),
automated clients must declare a `User-Agent` that identifies the application
and a contact. Set:

```bash
export SEC_USER_AGENT="YourAppName research@yourdomain.example"
```

This client sleeps ~0.12s between requests (~8/s) and retries once on HTTP
403/429. It **never** writes a fake Form 4 when EDGAR is down.

---

## 4. Form 4 transaction codes (official Item 8)

Copied from [Form 4](https://www.sec.gov/files/form4.pdf), Item 8:

| Code | Official description |
| :--- | :--- |
| **P** | Open market or private purchase of non-derivative or derivative security |
| **S** | Open market or private sale of non-derivative or derivative security |
| **V** | Transaction voluntarily reported earlier than required |
| **A** | Grant, award or other acquisition pursuant to Rule 16b-3(d) |
| **D** | Disposition to the issuer of issuer equity securities pursuant to Rule 16b-3(e) |
| **F** | Payment of exercise price or tax liability by delivering or withholding securities |
| **I** | Discretionary transaction in accordance with Rule 16b-3(f) |
| **M** | Exercise or conversion of derivative security exempted pursuant to Rule 16b-3 |
| **G** | Bona fide gift |
| **L** | Small acquisition under Rule 16a-6 |
| **W** | Acquisition or disposition by will or the laws of descent and distribution |
| **J** | Other acquisition or disposition (described in a footnote) |

Research signals in this repo **optionally interpret** `P` as a discretionary
open-market buy and `S` as an open-market sale. That interpretation is a
research choice, not an SEC designation.

---

## 5. What is *not* an official SEC product

| Item in this repo | What it actually is |
| :--- | :--- |
| 89-name universe | Curated large-cap **sample**, not the complete S&P 500 or Nasdaq |
| `sector` / `industry` columns | Conventional GICS-*aligned* labels, not a licensed MSCI/S&P GICS feed |
| `market_cap` | Unofficial approximate snapshot (AAPL ~$4.525T from Yahoo Finance on 2026-08-18). SEC does not publish market cap in `company_tickers.json` |
| `data/market_prices/*.csv` | Yahoo chart history when reachable; otherwise a deterministic interpolated fallback. **Not** official exchange last-sale prints |
| Backtest ROI tables | Simulations on collected Form 4 rows + fallback prices. **Not** live audited performance |

---

## 6. Shipped official Form 4 fixtures

Verified on 2026-08-18 from EDGAR Archives:

1. Apple Inc. accession [0001140361-26-032884](https://www.sec.gov/Archives/edgar/data/320193/000114036126032884/0001140361-26-032884-index.htm)
   — Newstead Jennifer, Common Stock sale (code `S`) on 2026-08-11 at $307.75, 1,439 shares, 10b5-1 footnote.
2. MICROSOFT CORP accession [0000789019-26-000145](https://www.sec.gov/Archives/edgar/data/789019/000078901926000145/0000789019-26-000145-index.htm)
   — Coleman Amy, tax withholding (code `F`) on 2026-08-17, 89.044 shares at $495.40.
