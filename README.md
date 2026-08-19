# Insider-trades

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

A Python toolkit that **downloads official SEC EDGAR Form 4 filings**, organizes them by sector/industry, and backtests simple insider-signal rules.

This repository is a **research toolkit**, not a complete NASDAQ or S&P 500 database, and it does **not** ship fabricated insider trades or audited strategy returns.

---

## Links

| | URL |
| :--- | :--- |
| **GitHub repository** | https://github.com/buffedlizard55-lab/Insider-trades |
| **GitHub Pages dashboard** | https://buffedlizard55-lab.github.io/Insider-trades/ |

---

## Official source of truth: SEC EDGAR Form 4

Public US insider transactions are reported to the
[U.S. Securities and Exchange Commission](https://www.sec.gov/) on **Form 4**
and published through **EDGAR**.

| Fact | Official source |
| :--- | :--- |
| Officers, directors, and >10% owners must report changes in beneficial ownership | [Section 16(a) of the Securities Exchange Act of 1934](https://www.sec.gov/about/laws/sea34.pdf) |
| Most Form 4 filings are due before the end of the second business day after the trade | Sarbanes-Oxley Act §403, implemented in [SEC Form 4](https://www.sec.gov/files/form4.pdf) |
| Transaction codes (`P`, `S`, `A`, `M`, `F`, `G`, `D`, …) | [Form 4 instructions, Item 8](https://www.sec.gov/files/form4.pdf) |
| Ticker → CIK map | [company_tickers.json](https://www.sec.gov/files/company_tickers.json) |
| Company filing history API | [data.sec.gov/submissions](https://data.sec.gov/submissions/CIK0000320193.json) |
| Latest Form 4 Atom feed | [browse-edgar getcurrent type=4](https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=4&output=atom) |
| Fair access: identify yourself and stay ≤ 10 requests/second | [SEC Developer Resources](https://www.sec.gov/about/developer-resources) and [Webmaster FAQ — User-Agent](https://www.sec.gov/about/webmaster-frequently-asked-questions#user-agent) |

See [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md) for the full citation list.

`python main.py collect` talks to those official endpoints. It **does not invent**
insider names, accession numbers, or trades. If EDGAR is unreachable, collection
fails rather than writing synthetic rows.

---

## What this repo is — and is not

**Is**

- A Form 4 XML parser (`ownershipDocument`)
- A rate-limited SEC EDGAR client
- A curated **89-name large-cap sample** with CIKs verified against
  [company_tickers.json](https://www.sec.gov/files/company_tickers.json) and
  EDGAR company search on **2026-08-18**
- A research backtester that runs **only** on collected official Form 4 rows

**Is not**

- The complete S&P 500 (500 names) or complete Nasdaq listing
- A licensed GICS constituent file (sector labels are GICS-*aligned* names)
- An official price vendor — stored CSVs are Yahoo-when-available or an
  interpolated fallback (see `data/market_prices/README.md`)
- Audited live trading performance. Any ROI number is a simulation on whatever
  official filings you have collected.

CIKs that were previously wrong in this tree (and are now the official SEC
values) include **AVGO 0001730168**, **PANW 0001327567**, **CSCO 0000858877**,
**AMGN 0000318154**, **MU 0000723125**, **T 0000732717**, **MDT 0001613103**,
**CB 0000896159**, **SPG 0001063761**, **FDX 0001048911**, and **XOM 0002115436**
(ExxonMobil Holdings Corporation, successor registrant after the July 2026
redomicile; prior issuer CIK 0000034088).

---

## Shipped official sample filings

Parser fixtures are verbatim extracts of published EDGAR Form 4 XML:

| File | Accession | Official index |
| :--- | :--- | :--- |
| `data/sample_xmls/AAPL_0000320193_form4_sample1.xml` | 0001140361-26-032884 | [Apple Inc. / Newstead Jennifer](https://www.sec.gov/Archives/edgar/data/320193/000114036126032884/0001140361-26-032884-index.htm) |
| `data/sample_xmls/MSFT_0000789019_form4_sample1.xml` | 0000789019-26-000145 | [MICROSOFT CORP / Coleman Amy](https://www.sec.gov/Archives/edgar/data/789019/000078901926000145/0000789019-26-000145-index.htm) |

The industry CSVs start with those same official rows. Pull more with `collect`.

---

## Quick start

```bash
git clone https://github.com/buffedlizard55-lab/Insider-trades.git
cd Insider-trades
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Required by the SEC before any automated EDGAR request
export SEC_USER_AGENT="YourName Research contact@yourdomain.example"

python main.py sources
python main.py universe --sector "Information Technology"
python main.py parse-xml --file data/sample_xmls/AAPL_0000320193_form4_sample1.xml

# Live EDGAR download (needs network + User-Agent)
python main.py collect --year 2026
```

---

## CLI

| Command | What it does |
| :--- | :--- |
| `python main.py sources` | Print official SEC citations |
| `python main.py universe` | List the curated 89-name sample |
| `python main.py collect --year 2026` | Download official Form 4s for that year |
| `python main.py parse-xml --file …` | Parse a local Form 4 XML |
| `python main.py heatmap` | Industry net-buy / net-sell table from **collected** rows |
| `python main.py signals --ticker AAPL` | Research signals on collected rows |
| `python main.py backtest --strategy conviction` | Simulate rules on collected rows |
| `python main.py prices --ticker AAPL --last 10` | Show the local price cache |
| `python main.py build-site --mirror-root` | Rebuild the static dashboard JSON |

---

## GitHub Pages

The live site is served from the `main` branch root:

**https://buffedlizard55-lab.github.io/Insider-trades/**

The dashboard only shows Form 4-derived tables after you collect filings and
rebuild (`python main.py build-site --mirror-root`). Empty tables mean no
official rows have been collected yet — not a hidden dataset.

Example workflow files live in [`examples/github_workflows/`](examples/github_workflows/).
They are **not** installed under `.github/workflows/` unless you copy them there.

---

## License

MIT. See [LICENSE](LICENSE).
