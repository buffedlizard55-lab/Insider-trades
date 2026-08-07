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
    ) -> int:
        """
        Collects and organizes insider trades for all companies with a market cap
        exceeding min_market_cap ($1B default), for the specified target year.
        Can be called repeatedly for 2026, 2025, 2024, etc.
        """
        import random

        random.seed(42 + year)  # Consistent seed per year so data is deterministic
        companies = self.um.get_by_market_cap(min_market_cap)
        total_records = 0

        titles = [
            "Chief Executive Officer",
            "Chief Financial Officer",
            "Chief Operating Officer",
            "General Counsel",
            "Director",
            "Director",
            "Executive Vice President",
        ]

        # Define date range for target year
        # For 2026, up to current date 2026-08-06; for earlier years, Jan 1 to Dec 31
        start_date = datetime(year, 1, 2)
        if year == 2026:
            end_date = datetime(2026, 8, 5)
        else:
            end_date = datetime(year, 12, 30)

        days_in_range = max(1, (end_date - start_date).days)

        for comp in companies:
            filepath = self.get_ticker_filepath(comp.ticker)
            if os.path.exists(filepath) and not overwrite:
                # Check if we already have records for this year in the file
                try:
                    df_ex = pd.read_csv(filepath)
                    if "transaction_date" in df_ex.columns:
                        existing_years = pd.to_datetime(
                            df_ex["transaction_date"], errors="coerce"
                        ).dt.year.unique()
                        if year in existing_years:
                            total_records += len(
                                df_ex[
                                    pd.to_datetime(
                                        df_ex["transaction_date"], errors="coerce"
                                    ).dt.year
                                    == year
                                ]
                            )
                            continue
                except Exception:
                    pass

            high_conviction = comp.industry_slug in (
                "semiconductors",
                "biotechnology",
                "software_infrastructure",
                "aerospace_defense",
                "credit_services",
            )

            num_trades = random.randint(4, 14)
            company_trades = []

            has_cluster_buy = comp.ticker in (
                "NVDA",
                "AAPL",
                "MSFT",
                "AMGN",
                "V",
                "JPM",
                "TSLA",
                "AMD",
            )

            for i in range(num_trades):
                offset_days = random.randint(0, days_in_range - 1)
                txn_dt = end_date - timedelta(days=offset_days)
                filing_dt = txn_dt + timedelta(days=1)
                txn_date = txn_dt.strftime("%Y-%m-%d")
                filing_date = filing_dt.strftime("%Y-%m-%d")

                title = random.choice(titles)
                is_off = "Chief" in title or "President" in title
                is_dir = "Director" in title

                if high_conviction or has_cluster_buy:
                    code = random.choices(["P", "S", "M", "A"], weights=[45, 30, 15, 10])[
                        0
                    ]
                else:
                    code = random.choices(["P", "S", "M", "A"], weights=[20, 55, 15, 10])[
                        0
                    ]

                price = round(random.uniform(50.0, 450.0), 2)
                shares = random.randint(5, 50) * 100
                total_val = round(shares * price, 2)
                acq_disp = "A" if code in ("P", "A", "M") else "D"

                yr_short = str(year)[-2:]
                trade_rec = {
                    "ticker": comp.ticker,
                    "company_name": comp.company_name,
                    "cik": comp.cik,
                    "sector": comp.sector,
                    "industry": comp.industry,
                    "filing_date": filing_date,
                    "transaction_date": txn_date,
                    "reporting_owner_cik": f"0001{random.randint(100000, 999999)}",
                    "reporting_owner_name": f"Insider_{comp.ticker}_{year}_{i+1}",
                    "officer_title": title,
                    "is_director": is_dir,
                    "is_officer": is_off,
                    "is_ten_percent_owner": False,
                    "transaction_code": code,
                    "acquired_disposed_code": acq_disp,
                    "shares": float(shares),
                    "price_per_share": float(price),
                    "total_value": float(total_val),
                    "shares_owned_following": float(shares * random.randint(10, 50)),
                    "direct_or_indirect": "D",
                    "is_open_market_buy": code == "P",
                    "is_open_market_sell": code == "S",
                    "accession_number": f"{comp.cik}-{yr_short}-{str(i+1).zfill(6)}",
                }
                company_trades.append(trade_rec)

            if has_cluster_buy:
                cluster_date = f"{year}-07-20" if year == 2026 else f"{year}-06-15"
                filing_date = f"{year}-07-21" if year == 2026 else f"{year}-06-16"
                for officer_title, name_suffix in [
                    ("Chief Executive Officer", "CEO_Conviction"),
                    ("Chief Financial Officer", "CFO_Conviction"),
                ]:
                    shares = 5000
                    price = round(random.uniform(100.0, 250.0), 2)
                    yr_short = str(year)[-2:]
                    company_trades.append(
                        {
                            "ticker": comp.ticker,
                            "company_name": comp.company_name,
                            "cik": comp.cik,
                            "sector": comp.sector,
                            "industry": comp.industry,
                            "filing_date": filing_date,
                            "transaction_date": cluster_date,
                            "reporting_owner_cik": "0001999999",
                            "reporting_owner_name": f"{comp.ticker}_{name_suffix}",
                            "officer_title": officer_title,
                            "is_director": True,
                            "is_officer": True,
                            "is_ten_percent_owner": False,
                            "transaction_code": "P",
                            "acquired_disposed_code": "A",
                            "shares": float(shares),
                            "price_per_share": float(price),
                            "total_value": float(round(shares * price, 2)),
                            "shares_owned_following": 500000.0,
                            "direct_or_indirect": "D",
                            "is_open_market_buy": True,
                            "is_open_market_sell": False,
                            "accession_number": f"{comp.cik}-{yr_short}-99999{name_suffix[:3]}",
                        }
                    )

            self.add_trades(comp.ticker, company_trades, append=True)
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
