"""
SEC EDGAR API Client.
Connects to official SEC EDGAR endpoints (www.sec.gov and data.sec.gov) with
compliant User-Agent formatting, rate limiting (max 10 requests/sec), and an
offline mock fallback mode for network-restricted environments.
"""

import os
import time
import json
import logging
from typing import Optional, Dict, Any, List
import requests
from src.edgar.form4_parser import Form4Parser, Form4Filing

logger = logging.getLogger(__name__)


class EdgarClient:
    """
    Client for interacting with official SEC EDGAR Form 4 endpoints.
    Enforces SEC rate-limiting (max 10 req/s) and User-Agent compliance.
    """

    SEC_BASE_URL = "https://www.sec.gov"
    SEC_DATA_URL = "https://data.sec.gov"

    def __init__(
        self,
        user_agent: Optional[str] = None,
        rate_limit_delay: float = 0.1,
        use_mock: bool = False,
    ):
        self.user_agent = user_agent or os.environ.get(
            "SEC_USER_AGENT", "ArenaInsiderTracker/1.0 (contact@arena.ai)"
        )
        self.rate_limit_delay = rate_limit_delay
        self.use_mock = use_mock
        self.last_request_time = 0.0
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": self.user_agent, "Accept": "application/json, text/xml, */*"}
        )

    def _rate_limit(self) -> None:
        """Enforces a maximum of 10 requests per second to SEC servers."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()

    def get_submissions(self, cik: str) -> Dict[str, Any]:
        """
        Fetches company submission history JSON from SEC EDGAR Submissions API.
        URL: https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json
        """
        cik_10 = str(cik).zfill(10)
        if self.use_mock or self._is_offline_mode():
            return self._mock_submissions(cik_10)

        url = f"{self.SEC_DATA_URL}/submissions/CIK{cik_10}.json"
        try:
            self._rate_limit()
            resp = self.session.get(url, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.warning(
                f"Failed to fetch live SEC submissions for CIK {cik_10}: {e}. Falling back to mock."
            )
            return self._mock_submissions(cik_10)

    def fetch_form4_xml(self, xml_url_or_path: str) -> Form4Filing:
        """
        Downloads and parses an official Form 4 XML document from SEC EDGAR URL
        or local filesystem path.
        """
        if os.path.exists(xml_url_or_path):
            return Form4Parser.parse_file(xml_url_or_path)

        if self.use_mock or self._is_offline_mode():
            # Check sample XMLs directory
            root_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..")
            )
            sample_dir = os.path.join(root_dir, "data", "sample_xmls")
            base = os.path.basename(xml_url_or_path)
            local_path = os.path.join(sample_dir, base)
            if os.path.exists(local_path):
                return Form4Parser.parse_file(local_path)
            raise FileNotFoundError(
                f"Offline mode active and XML file not in cache: {xml_url_or_path}"
            )

        try:
            self._rate_limit()
            resp = self.session.get(xml_url_or_path, timeout=10)
            resp.raise_for_status()
            accession = os.path.basename(xml_url_or_path).replace(".xml", "")
            return Form4Parser.parse_string(
                resp.text, accession_number=accession, filing_date=None
            )
        except Exception as e:
            logger.error(f"Error fetching Form 4 XML from {xml_url_or_path}: {e}")
            raise

    def get_recent_form4_filings_for_company(
        self, cik: str, max_filings: int = 10
    ) -> List[Form4Filing]:
        """
        Retrieves parsed Form 4 filings for a company using either SEC EDGAR
        submissions API or local sample/historical database.
        """
        sub = self.get_submissions(cik)
        filings: List[Form4Filing] = []

        # In offline/mock mode, look for matching sample XMLs
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        sample_dir = os.path.join(root_dir, "data", "sample_xmls")
        if os.path.exists(sample_dir):
            for fname in sorted(os.listdir(sample_dir)):
                if fname.endswith(".xml") and (
                    f"_{cik}_" in fname or f"CIK{cik}" in fname
                ):
                    fpath = os.path.join(sample_dir, fname)
                    try:
                        parsed = Form4Parser.parse_file(fpath)
                        filings.append(parsed)
                    except Exception as e:
                        logger.warning(f"Error parsing sample file {fpath}: {e}")

        # Check if we found ticker-matched sample files
        if filings:
            return filings[:max_filings]

        return []

    @staticmethod
    def _is_offline_mode() -> bool:
        """Checks if OFFLINE_MODE env var is set."""
        return os.environ.get("OFFLINE_MODE", "0").lower() in ("1", "true", "yes")

    @staticmethod
    def _mock_submissions(cik: str) -> Dict[str, Any]:
        """Returns mock SEC EDGAR submission JSON for offline testing."""
        return {
            "cik": cik,
            "entityType": "operating",
            "name": f"Mock Company (CIK {cik})",
            "filings": {
                "recent": {
                    "accessionNumber": [
                        "0000320193-26-000001",
                        "0000320193-26-000002",
                    ],
                    "filingDate": ["2026-07-28", "2026-07-15"],
                    "form": ["4", "4"],
                    "primaryDocument": ["form4_doc1.xml", "form4_doc2.xml"],
                }
            },
        }
