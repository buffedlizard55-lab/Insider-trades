"""
Universe Manager for NASDAQ and S&P 500 companies.
Manages ticker-to-CIK mapping, GICS sectors, industries, and market cap filtering ($1B+ focus).
"""

import os
import json
import csv
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
import pandas as pd


@dataclass
class CompanyInfo:
    ticker: str
    company_name: str
    cik: str
    exchange: str
    sector: str
    industry: str
    industry_slug: str
    market_cap: float = 0.0
    in_sp500: bool = True
    in_nasdaq100: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class UniverseManager:
    """
    Manages the universe of publicly traded NASDAQ and S&P 500 companies,
    providing structured access to sectors, industries, CIKs, market cap ($1B+),
    and metadata.
    """

    def __init__(self, data_path: Optional[str] = None):
        if data_path is None:
            root_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..")
            )
            data_path = os.path.join(
                root_dir, "data", "universe", "nasdaq_sp500_universe.csv"
            )
        self.data_path = data_path
        self._companies: Dict[str, CompanyInfo] = {}
        self._cik_map: Dict[str, CompanyInfo] = {}
        self.load_universe()

    def load_universe(self) -> None:
        """Loads the company universe from CSV or JSON file."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Universe file not found: {self.data_path}")

        self._companies.clear()
        self._cik_map.clear()

        if self.data_path.endswith(".json"):
            with open(self.data_path, "r", encoding="utf-8") as f:
                records = json.load(f)
        else:
            df = pd.read_csv(self.data_path, dtype={"cik": str})
            records = df.to_dict(orient="records")

        for r in records:
            cik_str = str(r.get("cik", "")).zfill(10)
            try:
                mc = float(r.get("market_cap", 0.0))
            except (ValueError, TypeError):
                mc = 0.0

            comp = CompanyInfo(
                ticker=str(r["ticker"]).upper().strip(),
                company_name=str(r["company_name"]).strip(),
                cik=cik_str,
                exchange=str(r["exchange"]).upper().strip(),
                sector=str(r["sector"]).strip(),
                industry=str(r["industry"]).strip(),
                industry_slug=str(r.get("industry_slug", self.slugify(r["industry"]))),
                market_cap=mc,
                in_sp500=bool(r.get("in_sp500", True)),
                in_nasdaq100=bool(r.get("in_nasdaq100", False)),
            )
            self._companies[comp.ticker] = comp
            self._cik_map[comp.cik] = comp

    @staticmethod
    def slugify(text: str) -> str:
        """Converts industry name into clean filesystem-friendly slug."""
        return (
            text.lower()
            .replace(" - ", "_")
            .replace(" & ", "_")
            .replace(" ", "_")
            .replace("/", "_")
            .replace("-", "_")
        )

    def get_company(self, ticker: str) -> Optional[CompanyInfo]:
        """Returns CompanyInfo for a given ticker symbol (case-insensitive)."""
        return self._companies.get(ticker.upper().strip())

    def get_by_cik(self, cik: str) -> Optional[CompanyInfo]:
        """Returns CompanyInfo for a 10-digit CIK."""
        return self._cik_map.get(str(cik).zfill(10))

    def get_all_companies(self) -> List[CompanyInfo]:
        """Returns all companies in the universe."""
        return list(self._companies.values())

    def get_by_market_cap(
        self, min_market_cap: float = 1_000_000_000.0
    ) -> List[CompanyInfo]:
        """Returns companies with a market cap greater than or equal to min_market_cap ($1B default)."""
        return [
            c for c in self._companies.values() if c.market_cap >= min_market_cap
        ]

    def get_filtered_companies(
        self,
        min_market_cap: float = 1_000_000_000.0,
        sector: Optional[str] = None,
        industry: Optional[str] = None,
        exchange: Optional[str] = None,
    ) -> List[CompanyInfo]:
        """Filters companies by market cap ($1B+), sector, industry, or exchange."""
        companies = self.get_by_market_cap(min_market_cap)
        if sector:
            sec_lower = sector.lower().strip()
            companies = [
                c
                for c in companies
                if c.sector.lower() == sec_lower
                or self.slugify(c.sector) == self.slugify(sector)
            ]
        if industry:
            ind_lower = industry.lower().strip()
            companies = [
                c
                for c in companies
                if c.industry.lower() == ind_lower
                or c.industry_slug == self.slugify(industry)
            ]
        if exchange:
            ex_lower = exchange.upper().strip()
            companies = [c for c in companies if c.exchange == ex_lower]
        return companies

    def get_by_sector(self, sector: str) -> List[CompanyInfo]:
        """Returns companies in a specific GICS sector."""
        sector_lower = sector.lower().strip()
        return [
            c
            for c in self._companies.values()
            if c.sector.lower() == sector_lower
            or self.slugify(c.sector) == self.slugify(sector)
        ]

    def get_by_industry(self, industry: str) -> List[CompanyInfo]:
        """Returns companies in a specific industry or industry_slug."""
        ind_lower = industry.lower().strip()
        return [
            c
            for c in self._companies.values()
            if c.industry.lower() == ind_lower
            or c.industry_slug == self.slugify(industry)
        ]

    def get_by_exchange(self, exchange: str) -> List[CompanyInfo]:
        """Returns companies traded on a specific exchange (NASDAQ or NYSE)."""
        ex_lower = exchange.upper().strip()
        return [c for c in self._companies.values() if c.exchange == ex_lower]

    def list_sectors(self) -> List[str]:
        """Returns sorted list of all unique GICS sectors."""
        return sorted(list({c.sector for c in self._companies.values()}))

    def list_industries(self, sector: Optional[str] = None) -> List[str]:
        """Returns sorted list of industries, optionally filtered by sector."""
        if sector:
            sector_lower = sector.lower().strip()
            return sorted(
                list(
                    {
                        c.industry
                        for c in self._companies.values()
                        if c.sector.lower() == sector_lower
                    }
                )
            )
        return sorted(list({c.industry for c in self._companies.values()}))

    def get_sector_slug(self, sector: str) -> str:
        """Returns filesystem slug for a sector."""
        return self.slugify(sector)

    def to_dataframe(self) -> pd.DataFrame:
        """Returns entire universe as a pandas DataFrame."""
        return pd.DataFrame([c.to_dict() for c in self._companies.values()])

    def get_sector_industry_stats(self) -> pd.DataFrame:
        """Returns a summary table with company counts per sector and industry."""
        df = self.to_dataframe()
        stats = (
            df.groupby(["sector", "industry"])
            .size()
            .reset_index(name="company_count")
            .sort_values(["sector", "company_count"], ascending=[True, False])
        )
        return stats
