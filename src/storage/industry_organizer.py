"""
Industry Organizer and Data Storage Engine.
Organizes all insider trade records cleanly by GICS Sector and Industry:
  data/industries/{sector_slug}/{industry_slug}/{ticker}_insider_trades.csv
  data/industries/{sector_slug}/{industry_slug}/industry_summary.json
  data/summary_by_industry.csv

Supports year-based filtering (e.g. current year 2026 first, previous years later)
and market cap filtering ($1B+ default).
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime, timedelta
from src.universe.universe_manager import UniverseManager, CompanyInfo

logger = logging.getLogger(__name__)


class IndustryOrganizer:
    """
    Manages filesystem-based storage of insider trades organized by
    GICS Sector and Industry.
    """

    def __init__(
        self,
        base_dir: Optional[str] = None,
        universe_manager: Optional[UniverseManager] = None,
    ):
        if base_dir is None:
            root_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..")
            )
            base_dir = os.path.join(root_dir, "data", "industries")
        self.base_dir = base_dir
        self.um = universe_manager or UniverseManager()

    def get_ticker_dir(self, ticker: str) -> str:
        """Returns the directory path for a ticker based on its sector and industry."""
        comp = self.um.get_company(ticker)
        if not comp:
            # Fallback to unclassified
            return os.path.join(self.base_dir, "unclassified", "unclassified")
        sec_slug = self.um.slugify(comp.sector)
        ind_slug = comp.industry_slug
        path = os.path.join(self.base_dir, sec_slug, ind_slug)
        os.makedirs(path, exist_ok=True)
        return path

    def get_ticker_filepath(self, ticker: str) -> str:
        """Returns full filepath for a ticker's trade CSV."""
        t_dir = self.get_ticker_dir(ticker)
        return os.path.join(t_dir, f"{ticker.upper()}_insider_trades.csv")

    def add_trades(
        self,
        ticker: str,
        trades: List[Dict[str, Any]] | pd.DataFrame,
        append: bool = True,
        year: Optional[int] = None,
    ) -> str:
        """
        Saves or appends a list of trade records (or DataFrame) to the ticker's
        industry-organized CSV file. Optionally filters trades by year.
        """
        if isinstance(trades, list):
            df = pd.DataFrame(trades)
        else:
            df = trades.copy()

        if df.empty:
            return self.get_ticker_filepath(ticker)

        # Standardize column order if possible
        std_cols = [
            "ticker",
            "company_name",
            "cik",
            "sector",
            "industry",
            "filing_date",
            "transaction_date",
            "reporting_owner_cik",
            "reporting_owner_name",
            "officer_title",
            "is_director",
            "is_officer",
            "is_ten_percent_owner",
            "transaction_code",
            "acquired_disposed_code",
            "shares",
            "price_per_share",
            "total_value",
            "shares_owned_following",
            "direct_or_indirect",
            "is_open_market_buy",
            "is_open_market_sell",
            "accession_number",
        ]

        comp = self.um.get_company(ticker)
        if "ticker" not in df.columns:
            df["ticker"] = ticker.upper()
        if comp:
            df["company_name"] = comp.company_name
            df["cik"] = comp.cik
            df["sector"] = comp.sector
            df["industry"] = comp.industry

        # If a specific year is provided, filter transaction_date to that year
        if year is not None and "transaction_date" in df.columns:
            df["_dt_year"] = pd.to_datetime(
                df["transaction_date"], errors="coerce"
            ).dt.year
            df = df[df["_dt_year"] == year].drop(columns=["_dt_year"])

        filepath = self.get_ticker_filepath(ticker)
        if append and os.path.exists(filepath):
            existing_df = pd.read_csv(filepath)
            combined = pd.concat([existing_df, df], ignore_index=True)
            subset_cols = [
                c
                for c in [
                    "accession_number",
                    "transaction_date",
                    "shares",
                    "price_per_share",
                ]
                if c in combined.columns
            ]
            if subset_cols:
                combined = combined.drop_duplicates(subset=subset_cols, keep="last")
            else:
                combined = combined.drop_duplicates(keep="last")
            combined = combined.sort_values(
                "transaction_date", ascending=False
            ).reset_index(drop=True)
            combined.to_csv(filepath, index=False)
        else:
            df = df.sort_values("transaction_date", ascending=False).reset_index(
                drop=True
            )
            df.to_csv(filepath, index=False)

        # Update industry summary
        if comp:
            self.compute_industry_summary(comp.industry)

        return filepath

    def get_ticker_trades(
        self, ticker: str, year: Optional[int] = None
    ) -> pd.DataFrame:
        """Loads historical trades for a specific ticker, optionally filtered by year."""
        filepath = self.get_ticker_filepath(ticker)
        if not os.path.exists(filepath):
            return pd.DataFrame()
        df = pd.read_csv(filepath)
        if year is not None and "transaction_date" in df.columns:
            df["_year"] = pd.to_datetime(
                df["transaction_date"], errors="coerce"
            ).dt.year
            df = df[df["_year"] == year].drop(columns=["_year"])
        return df

    def get_industry_trades(
        self,
        industry: str,
        year: Optional[int] = None,
        min_market_cap: float = 1_000_000_000.0,
    ) -> pd.DataFrame:
        """Loads all historical trades for every ticker in a specific industry ($1B+ default)."""
        companies = self.um.get_filtered_companies(
            min_market_cap=min_market_cap, industry=industry
        )
        dfs = []
        for comp in companies:
            df = self.get_ticker_trades(comp.ticker, year=year)
            if not df.empty:
                dfs.append(df)
        if not dfs:
            return pd.DataFrame()
        combined = pd.concat(dfs, ignore_index=True)
        if "transaction_date" in combined.columns:
            combined = combined.sort_values(
                "transaction_date", ascending=False
            ).reset_index(drop=True)
        return combined

    def get_sector_trades(
        self,
        sector: str,
        year: Optional[int] = None,
        min_market_cap: float = 1_000_000_000.0,
    ) -> pd.DataFrame:
        """Loads all historical trades for every ticker in a specific GICS sector ($1B+ default)."""
        companies = self.um.get_filtered_companies(
            min_market_cap=min_market_cap, sector=sector
        )
        dfs = []
        for comp in companies:
            df = self.get_ticker_trades(comp.ticker, year=year)
            if not df.empty:
                dfs.append(df)
        if not dfs:
            return pd.DataFrame()
        combined = pd.concat(dfs, ignore_index=True)
        if "transaction_date" in combined.columns:
            combined = combined.sort_values(
                "transaction_date", ascending=False
            ).reset_index(drop=True)
        return combined

    def get_all_trades(
        self, year: Optional[int] = None, min_market_cap: float = 1_000_000_000.0
    ) -> pd.DataFrame:
        """Loads all insider trades across the entire S&P 500 and NASDAQ universe ($1B+ default)."""
        dfs = []
        for comp in self.um.get_by_market_cap(min_market_cap):
            df = self.get_ticker_trades(comp.ticker, year=year)
            if not df.empty:
                dfs.append(df)
        if not dfs:
            return pd.DataFrame()
        combined = pd.concat(dfs, ignore_index=True)
        if "transaction_date" in combined.columns:
            combined = combined.sort_values(
                "transaction_date", ascending=False
            ).reset_index(drop=True)
        return combined

    def compute_industry_summary(
        self, industry: str, year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Computes aggregate metrics for an industry and saves to
        industry_summary.json inside the industry directory.
        """
        companies = self.um.get_by_industry(industry)
        if not companies:
            return {}

        sec_slug = self.um.slugify(companies[0].sector)
        ind_slug = companies[0].industry_slug
        ind_dir = os.path.join(self.base_dir, sec_slug, ind_slug)
        os.makedirs(ind_dir, exist_ok=True)

        df = self.get_industry_trades(industry, year=year)
        ticker_count = len(companies)
        trades_count = len(df)
        open_buys_val = 0.0
        open_sells_val = 0.0
        open_buys_count = 0
        open_sells_count = 0

        if not df.empty and "is_open_market_buy" in df.columns:
            buys = df[df["is_open_market_buy"] == True]
            sells = df[df["is_open_market_sell"] == True]
            open_buys_val = float(buys["total_value"].sum())
            open_sells_val = float(sells["total_value"].sum())
            open_buys_count = int(len(buys))
            open_sells_count = int(len(sells))

        net_val = open_buys_val - open_sells_val
        buy_sell_ratio = (
            round(open_buys_val / open_sells_val, 2)
            if open_sells_val > 0
            else (999.0 if open_buys_val > 0 else 0.0)
        )

        summary = {
            "sector": companies[0].sector,
            "industry": companies[0].industry,
            "industry_slug": ind_slug,
            "year_filter": year if year else "ALL",
            "total_companies": ticker_count,
            "total_transactions": trades_count,
            "open_market_buys_count": open_buys_count,
            "open_market_buys_dollar_value": round(open_buys_val, 2),
            "open_market_sells_count": open_sells_count,
            "open_market_sells_dollar_value": round(open_sells_val, 2),
            "net_dollar_flow": round(net_val, 2),
            "buy_sell_dollar_ratio": buy_sell_ratio,
        }

        sum_file = os.path.join(ind_dir, "industry_summary.json")
        with open(sum_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        return summary

    def update_all_summaries(self, year: Optional[int] = None) -> pd.DataFrame:
        """
        Computes summaries across all industries and saves a master
        summary_by_industry.csv and .json to the data directory.
        """
        summaries = []
        for industry in self.um.list_industries():
            s = self.compute_industry_summary(industry, year=year)
            if s:
                summaries.append(s)

        df = pd.DataFrame(summaries)
        if not df.empty:
            df = df.sort_values(
                ["buy_sell_dollar_ratio", "net_dollar_flow"], ascending=[False, False]
            ).reset_index(drop=True)

        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        csv_path = os.path.join(root_dir, "data", "summary_by_industry.csv")
        json_path = os.path.join(root_dir, "data", "summary_by_industry.json")
        df.to_csv(csv_path, index=False)
        df.to_json(json_path, orient="records", indent=2)
        return df

    def collect_and_organize_trades(
        self,
        year: int = 2026,
        min_market_cap: float = 1_000_000_000.0,
        overwrite: bool = False,
        max_filings_per_company: int = 40,
    ) -> int:
        """
        Download official SEC EDGAR Form 4 filings for universe companies and
        store the parsed transactions under data/industries/.

        Never invents insider names, accession numbers, prices, or trades.
        Requires network access to data.sec.gov / www.sec.gov and a compliant
        SEC_USER_AGENT environment variable (app name + contact email).
        """
        from src.edgar.client import EdgarClient

        client = EdgarClient()
        companies = self.um.get_by_market_cap(min_market_cap)
        total_records = 0

        for comp in companies:
            try:
                filings = client.get_recent_form4_filings_for_company(
                    comp.cik, max_filings=max_filings_per_company, year=year
                )
            except Exception as exc:
                logger.warning(
                    "SEC Form 4 collect failed for %s (CIK %s): %s",
                    comp.ticker,
                    comp.cik,
                    exc,
                )
                continue

            company_trades: List[Dict[str, Any]] = []
            for filing in filings:
                for txn in filing.transactions:
                    txn_year = None
                    try:
                        txn_year = int(str(txn.transaction_date)[:4])
                    except (TypeError, ValueError):
                        pass
                    if year is not None and txn_year is not None and txn_year != year:
                        continue
                    company_trades.append(
                        {
                            "ticker": comp.ticker,
                            "company_name": comp.company_name,
                            "cik": comp.cik,
                            "sector": comp.sector,
                            "industry": comp.industry,
                            "filing_date": txn.filing_date,
                            "transaction_date": txn.transaction_date,
                            "reporting_owner_cik": txn.reporting_owner_cik,
                            "reporting_owner_name": txn.reporting_owner_name,
                            "officer_title": txn.officer_title,
                            "is_director": txn.is_director,
                            "is_officer": txn.is_officer,
                            "is_ten_percent_owner": txn.is_ten_percent_owner,
                            "transaction_code": txn.transaction_code,
                            "acquired_disposed_code": txn.acquired_disposed_code,
                            "shares": float(txn.shares),
                            "price_per_share": float(txn.price_per_share),
                            "total_value": float(txn.total_value),
                            "shares_owned_following": float(txn.shares_owned_following),
                            "direct_or_indirect": txn.direct_or_indirect,
                            "is_open_market_buy": bool(txn.is_open_market_buy),
                            "is_open_market_sell": bool(txn.is_open_market_sell),
                            "accession_number": txn.accession_number,
                            "source_url": EdgarClient.filing_index_url(
                                comp.cik, txn.accession_number
                            )
                            if txn.accession_number
                            else "",
                        }
                    )

            if company_trades:
                self.add_trades(comp.ticker, company_trades, append=not overwrite)
                total_records += len(company_trades)

        self.update_all_summaries(year=year)
        return total_records

    def seed_historical_dataset(
        self,
        overwrite: bool = False,
        year: int = 2026,
        min_market_cap: float = 1_000_000_000.0,
    ) -> int:
        """
        Alias for collect_and_organize_trades for backward compatibility.
        """
        return self.collect_and_organize_trades(
            year=year, min_market_cap=min_market_cap, overwrite=overwrite
        )
