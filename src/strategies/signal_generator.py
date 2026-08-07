"""
Signal Generator for Quantitative Insider Trading Strategies.
Analyzes parsed SEC Form 4 transactions and generates structured Bullish Entry
and Bearish Exit signals with confidence scores (0-100%), trigger explanations,
and links to official SEC EDGAR Form 4 filings and local dataset paths.
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime, timedelta
from src.universe.universe_manager import UniverseManager


@dataclass
class InsiderSignal:
    signal_type: str
    ticker: str
    sector: str
    industry: str
    date: str
    confidence_score: int
    dollar_value: float
    insider_count: int
    rationale: str
    trades_count: int
    trigger_accession: str = ""
    trigger_url: str = ""
    local_source_file: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SignalGenerator:
    """
    Generates quantitative insider trading entry and exit signals from
    industry-organized Form 4 transaction records.
    """

    CLUSTER_BUY = "CLUSTER_BUY"
    CONVICTION_BUY = "CONVICTION_BUY"
    INDUSTRY_BULLISH = "INDUSTRY_BULLISH"
    HEAVY_SELL_EXIT = "HEAVY_SELL_EXIT"

    def __init__(self, universe_manager: Optional[UniverseManager] = None):
        self.um = universe_manager or UniverseManager()

    def generate_signals_for_ticker(
        self,
        ticker: str,
        trades_df: pd.DataFrame,
        window_days: int = 14,
        min_confidence: int = 60,
    ) -> List[InsiderSignal]:
        """
        Scans a ticker's trade log and returns all entry and exit signals
        matching or exceeding min_confidence, including trigger links.
        """
        if trades_df.empty or "transaction_date" not in trades_df.columns:
            return []

        comp = self.um.get_company(ticker)
        sector = comp.sector if comp else "Unclassified"
        industry = comp.industry if comp else "Unclassified"
        cik = comp.cik if comp else "0000000000"

        sec_slug = self.um.slugify(sector)
        ind_slug = comp.industry_slug if comp else self.um.slugify(industry)
        local_path = f"data/industries/{sec_slug}/{ind_slug}/{ticker.upper()}_insider_trades.csv"
        sec_url = f"https://www.sec.gov/edgar/browse/?CIK={cik}"

        df = trades_df.copy()
        df["dt"] = pd.to_datetime(df["transaction_date"], errors="coerce")
        df = df.dropna(subset=["dt"]).sort_values("dt").reset_index(drop=True)

        signals: List[InsiderSignal] = []

        unique_dates = sorted(df["dt"].unique())
        for ref_date in unique_dates:
            window_start = ref_date - pd.Timedelta(days=window_days)
            win_df = df[(df["dt"] >= window_start) & (df["dt"] <= ref_date)]

            # 1. Check C-Suite Conviction Buy (CEO or CFO open market purchase P > $100k)
            buys = win_df[win_df["transaction_code"] == "P"]
            for _, row in buys.iterrows():
                title = str(row.get("officer_title", "")).upper()
                total_val = float(row.get("total_value", 0.0))
                if ("CEO" in title or "CHIEF EXECUTIVE" in title or "CFO" in title or "CHIEF FINANCIAL" in title) and total_val >= 100000.0:
                    conf = 70
                    if total_val >= 250000:
                        conf = 80
                    if total_val >= 500000:
                        conf = 90
                    if total_val >= 1000000:
                        conf = 95
                    if conf >= min_confidence:
                        acc = str(row.get("accession_number", "UNKNOWN"))
                        sig = InsiderSignal(
                            signal_type=self.CONVICTION_BUY,
                            ticker=ticker.upper(),
                            sector=sector,
                            industry=industry,
                            date=ref_date.strftime("%Y-%m-%d"),
                            confidence_score=conf,
                            dollar_value=round(total_val, 2),
                            insider_count=1,
                            rationale=f"C-Suite Conviction Buy: {row.get('reporting_owner_name')} ({row.get('officer_title')}) open-market purchase of ${total_val:,.2f}",
                            trades_count=1,
                            trigger_accession=acc,
                            trigger_url=sec_url,
                            local_source_file=local_path,
                        )
                        if not self._is_duplicate(signals, sig):
                            signals.append(sig)

            # 2. Check Cluster Buy (>= 2 distinct insiders buying open market P in window)
            if len(buys) >= 2:
                unique_buyers = set(buys["reporting_owner_name"].unique())
                if len(unique_buyers) >= 2:
                    total_val = float(buys["total_value"].sum())
                    conf = 75 + (len(unique_buyers) - 2) * 10
                    has_csuite = any(
                        "CEO" in str(t).upper() or "CFO" in str(t).upper()
                        for t in buys["officer_title"]
                    )
                    if has_csuite:
                        conf += 5
                    conf = min(conf, 99)
                    if conf >= min_confidence:
                        acc_list = buys["accession_number"].dropna().unique() if "accession_number" in buys.columns else ["UNKNOWN"]
                        primary_acc = str(acc_list[0]) if len(acc_list) > 0 else "UNKNOWN"
                        sig = InsiderSignal(
                            signal_type=self.CLUSTER_BUY,
                            ticker=ticker.upper(),
                            sector=sector,
                            industry=industry,
                            date=ref_date.strftime("%Y-%m-%d"),
                            confidence_score=conf,
                            dollar_value=round(total_val, 2),
                            insider_count=len(unique_buyers),
                            rationale=f"Cluster Buy Trigger: {len(unique_buyers)} independent insiders purchased ${total_val:,.2f} within {window_days} days",
                            trades_count=len(buys),
                            trigger_accession=primary_acc,
                            trigger_url=sec_url,
                            local_source_file=local_path,
                        )
                        if not self._is_duplicate(signals, sig):
                            signals.append(sig)

            # 3. Check Heavy Sell Exit (>= 2 distinct insiders selling open market S in window > $1M)
            sells = win_df[win_df["transaction_code"] == "S"]
            if len(sells) >= 2:
                unique_sellers = set(sells["reporting_owner_name"].unique())
                total_val = float(sells["total_value"].sum())
                if len(unique_sellers) >= 2 and total_val >= 1000000.0:
                    conf = 65 + min(25, int(total_val / 500000) * 5)
                    conf = min(conf, 95)
                    if conf >= min_confidence:
                        acc_list = sells["accession_number"].dropna().unique() if "accession_number" in sells.columns else ["UNKNOWN"]
                        primary_acc = str(acc_list[0]) if len(acc_list) > 0 else "UNKNOWN"
                        sig = InsiderSignal(
                            signal_type=self.HEAVY_SELL_EXIT,
                            ticker=ticker.upper(),
                            sector=sector,
                            industry=industry,
                            date=ref_date.strftime("%Y-%m-%d"),
                            confidence_score=conf,
                            dollar_value=round(total_val, 2),
                            insider_count=len(unique_sellers),
                            rationale=f"Heavy Sell Exit: {len(unique_sellers)} executives sold ${total_val:,.2f} over {window_days} days",
                            trades_count=len(sells),
                            trigger_accession=primary_acc,
                            trigger_url=sec_url,
                            local_source_file=local_path,
                        )
                        if not self._is_duplicate(signals, sig):
                            signals.append(sig)

        signals.sort(key=lambda x: x.date)
        return signals

    def generate_industry_signals(
        self, industry: str, industry_trades_df: pd.DataFrame
    ) -> List[InsiderSignal]:
        """
        Generates industry-wide macro bullish/bearish signals based on
        aggregate net buy/sell ratio.
        """
        if industry_trades_df.empty:
            return []

        companies = self.um.get_by_industry(industry)
        sector = companies[0].sector if companies else "Unclassified"
        cik = companies[0].cik if companies else "0000000000"
        ind_slug = companies[0].industry_slug if companies else self.um.slugify(industry)
        sec_slug = self.um.slugify(sector)
        local_path = f"data/industries/{sec_slug}/{ind_slug}/"
        sec_url = f"https://www.sec.gov/edgar/browse/?CIK={cik}"

        buys = industry_trades_df[industry_trades_df["transaction_code"] == "P"]
        sells = industry_trades_df[industry_trades_df["transaction_code"] == "S"]

        buy_val = float(buys["total_value"].sum()) if not buys.empty else 0.0
        sell_val = float(sells["total_value"].sum()) if not sells.empty else 0.0

        ratio = buy_val / sell_val if sell_val > 0 else (99.0 if buy_val > 0 else 0.0)

        if ratio >= 1.5 and buy_val >= 500000.0:
            conf = min(95, 65 + int(ratio * 10))
            acc_list = buys["accession_number"].dropna().unique() if "accession_number" in buys.columns else ["UNKNOWN"]
            primary_acc = str(acc_list[0]) if len(acc_list) > 0 else "UNKNOWN"
            return [
                InsiderSignal(
                    signal_type=self.INDUSTRY_BULLISH,
                    ticker="INDUSTRY",
                    sector=sector,
                    industry=industry,
                    date=datetime.now().strftime("%Y-%m-%d"),
                    confidence_score=conf,
                    dollar_value=round(buy_val, 2),
                    insider_count=len(set(buys["reporting_owner_name"].unique())),
                    rationale=f"Industry Bullish Accumulation: Net buy/sell dollar ratio of {ratio:.2f}x with ${buy_val:,.2f} total open-market buying",
                    trades_count=len(buys),
                    trigger_accession=primary_acc,
                    trigger_url=sec_url,
                    local_source_file=local_path,
                )
            ]
        return []

    @staticmethod
    def _is_duplicate(existing: List[InsiderSignal], candidate: InsiderSignal) -> bool:
        for s in existing:
            if (
                s.signal_type == candidate.signal_type
                and s.ticker == candidate.ticker
                and s.date == candidate.date
            ):
                return True
        return False
