"""
SEC EDGAR API client.

Talks only to official SEC endpoints (www.sec.gov and data.sec.gov) with a
declared User-Agent and a 10 requests/second ceiling, as required by the
SEC Developer Resources fair-access policy:

  https://www.sec.gov/about/developer-resources
  https://www.sec.gov/about/webmaster-frequently-asked-questions#user-agent

This client never invents filings. If the network is unavailable it raises;
callers must not substitute synthetic Form 4 records.
"""

import os
import time
import logging
from typing import Optional, Dict, Any, List
import requests
from src.edgar.form4_parser import Form4Parser, Form4Filing

logger = logging.getLogger(__name__)

# Official SEC endpoints (documented at the Developer Resources page above).
SEC_WWW = "https://www.sec.gov"
SEC_DATA = "https://data.sec.gov"
COMPANY_TICKERS_URL = f"{SEC_WWW}/files/company_tickers.json"
COMPANY_TICKERS_EXCHANGE_URL = f"{SEC_WWW}/files/company_tickers_exchange.json"
SUBMISSIONS_URL = SEC_DATA + "/submissions/CIK{cik}.json"
CURRENT_FORM4_ATOM = (
    f"{SEC_WWW}/cgi-bin/browse-edgar?action=getcurrent&type=4&owner=only&output=atom"
)
DAILY_INDEX_URL = f"{SEC_WWW}/Archives/edgar/daily-index/"


class EdgarClient:
    """
    Client for official SEC EDGAR Form 4 endpoints.
    Enforces SEC rate-limiting (max 10 req/s) and User-Agent compliance.
    """

    SEC_BASE_URL = SEC_WWW
    SEC_DATA_URL = SEC_DATA

    def __init__(
        self,
        user_agent: Optional[str] = None,
        rate_limit_delay: float = 0.12,
        use_mock: bool = False,
    ):
        env_ua = os.environ.get("SEC_USER_AGENT", "").strip()
        self.user_agent = user_agent or env_ua or (
            "InsiderTradesResearch/1.0 (set SEC_USER_AGENT to 'AppName contact@email')"
        )
        self.rate_limit_delay = rate_limit_delay
        self.use_mock = use_mock
        self.last_request_time = 0.0
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": self.user_agent,
                "Accept-Encoding": "gzip, deflate",
                "Accept": "application/json, text/xml, application/xml, */*",
            }
        )

    def _rate_limit(self) -> None:
        """Stay under the SEC's published 10 requests/second ceiling."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()

    def _get(self, url: str, timeout: int = 20) -> requests.Response:
        self._rate_limit()
        resp = self.session.get(url, timeout=timeout)
        if resp.status_code in (403, 429):
            # Brief backoff then one retry, as recommended when the SEC
            # temporarily limits an IP that exceeded fair-access rules.
            time.sleep(1.0)
            self._rate_limit()
            resp = self.session.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp

    def get_company_tickers(self) -> Dict[str, Any]:
        """
        Official ticker → CIK map.
        https://www.sec.gov/files/company_tickers.json
        """
        return self._get(COMPANY_TICKERS_URL).json()

    def get_submissions(self, cik: str) -> Dict[str, Any]:
        """
        Company submission history from the official Submissions API.
        URL: https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json

        Raises on network/HTTP errors. Does not invent filings.
        """
        cik_10 = str(cik).zfill(10)
        if self.use_mock:
            return self._mock_submissions(cik_10)

        url = SUBMISSIONS_URL.format(cik=cik_10)
        return self._get(url).json()

    def fetch_form4_xml(self, xml_url_or_path: str) -> Form4Filing:
        """
        Parses a Form 4 XML document from a local path or an official
        SEC EDGAR Archives URL.
        """
        if os.path.exists(xml_url_or_path):
            return Form4Parser.parse_file(xml_url_or_path)

        if self.use_mock:
            raise FileNotFoundError(
                f"Mock/offline mode is on and no local XML exists: {xml_url_or_path}"
            )

        resp = self._get(xml_url_or_path)
        accession = os.path.basename(xml_url_or_path).replace(".xml", "")
        return Form4Parser.parse_string(
            resp.text, accession_number=accession, filing_date=None
        )

    @staticmethod
    def archives_xml_url(cik: str, accession: str, primary_document: str) -> str:
        """Build the official EDGAR Archives URL for a filing's primary document."""
        cik_nolead = str(int(str(cik)))
        acc_nodash = accession.replace("-", "")
        doc = (primary_document or "form4.xml").split("/")[-1]
        return (
            f"{SEC_WWW}/Archives/edgar/data/{cik_nolead}/{acc_nodash}/{doc}"
        )

    @staticmethod
    def filing_index_url(cik: str, accession: str) -> str:
        cik_nolead = str(int(str(cik)))
        acc_nodash = accession.replace("-", "")
        return (
            f"{SEC_WWW}/Archives/edgar/data/{cik_nolead}/{acc_nodash}/"
            f"{accession}-index.htm"
        )

    def get_recent_form4_filings_for_company(
        self,
        cik: str,
        max_filings: int = 40,
        year: Optional[int] = None,
    ) -> List[Form4Filing]:
        """
        Downloads and parses official Form 4 XML filings for a company from
        the Submissions API + EDGAR Archives. Returns only successfully
        parsed live filings — never synthetic records.
        """
        if self.use_mock:
            return []

        sub = self.get_submissions(cik)
        recent = (sub.get("filings") or {}).get("recent") or {}
        forms = recent.get("form") or []
        accessions = recent.get("accessionNumber") or []
        dates = recent.get("filingDate") or []
        docs = recent.get("primaryDocument") or []

        filings: List[Form4Filing] = []
        for i, form in enumerate(forms):
            if len(filings) >= max_filings:
                break
            if str(form).strip() not in ("4", "4/A"):
                continue
            filing_date = dates[i] if i < len(dates) else ""
            if year is not None and not str(filing_date).startswith(str(year)):
                continue
            accession = accessions[i] if i < len(accessions) else ""
            primary = docs[i] if i < len(docs) else "form4.xml"
            if not accession:
                continue

            candidates = []
            if primary:
                candidates.append(self.archives_xml_url(cik, accession, primary))
            # Common official primary-document names when the listed file is HTML/XSL.
            for fallback in ("form4.xml", "wk-form4.xml", "doc4.xml"):
                url = self.archives_xml_url(cik, accession, fallback)
                if url not in candidates:
                    candidates.append(url)

            parsed = None
            last_err = None
            for url in candidates:
                try:
                    parsed = self.fetch_form4_xml(url)
                    parsed.accession_number = accession
                    parsed.filing_date = filing_date or parsed.filing_date
                    for txn in parsed.transactions:
                        txn.accession_number = accession
                        txn.filing_date = parsed.filing_date
                    break
                except Exception as exc:
                    last_err = exc
                    continue
            if parsed is None:
                logger.warning(
                    "Could not download Form 4 XML for CIK %s accession %s: %s",
                    cik,
                    accession,
                    last_err,
                )
                continue
            filings.append(parsed)
        return filings

    @staticmethod
    def _is_offline_mode() -> bool:
        return os.environ.get("OFFLINE_MODE", "0").lower() in ("1", "true", "yes")

    @staticmethod
    def _mock_submissions(cik: str) -> Dict[str, Any]:
        """Empty mock used only when use_mock=True (unit tests). Never a live filing."""
        return {
            "cik": cik,
            "entityType": "operating",
            "name": f"Mock Company (CIK {cik})",
            "filings": {
                "recent": {
                    "accessionNumber": [],
                    "filingDate": [],
                    "form": [],
                    "primaryDocument": [],
                }
            },
        }
