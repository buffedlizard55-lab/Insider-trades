"""
Industry Insider Trading Analytics & Heatmaps.
Aggregates open-market insider buying and selling across GICS sectors and
industries to reveal macro sentiment, sector rotations, and accumulation zones.
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime, timedelta
from src.universe.universe_manager import UniverseManager


@dataclass
class IndustryHeatmapRow:
    sector: str
    industry: str
    industry_slug: str
    company_count: int
    open_buys_count: int
    open_buys_dollar: float
    open_sells_count: int
    open_sells_dollar: float
    net_dollar_flow: float
    buy_sell_ratio: float
    sentiment: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class IndustryAnalytics:
    """
    Computes cross-sectional industry heatmaps and insider sentiment rankings
    from partitioned Form 4 trade data.
    """

    def __init__(self, universe_manager: Optional[UniverseManager] = None):
        self.um = universe_manager or UniverseManager()

    def generate_heatmap(
        self, days: int = 90, sector_filter: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Generates an industry-level insider sentiment heatmap table over the
        specified trailing number of calendar days.
        """
        from src.storage.industry_organizer import IndustryOrganizer

        io = IndustryOrganizer(universe_manager=self.um)

        all_trades = io.get_all_trades()
        if all_trades.empty or "transaction_date" not in all_trades.columns:
            return pd.DataFrame()

        # Filter by trailing date window if days > 0
        df = all_trades.copy()
        if days > 0:
            df["dt"] = pd.to_datetime(df["transaction_date"], errors="coerce")
            cutoff = datetime.now() - timedelta(days=days)
            df = df[df["dt"] >= cutoff]

        if sector_filter:
            sec_lower = sector_filter.lower().strip()
            df = df[
                df["sector"].str.lower() == sec_lower
                | (df["sector"].apply(self.um.slugify) == self.um.slugify(sector_filter))
            ]

        rows: List[IndustryHeatmapRow] = []

        for industry in self.um.list_industries():
            ind_df = df[df["industry"] == industry]
            companies = self.um.get_by_industry(industry)
            sector_name = companies[0].sector if companies else "Unclassified"
            ind_slug = (
                companies[0].industry_slug
                if companies
                else self.um.slugify(industry)
            )

            open_buys = (
                ind_df[ind_df["transaction_code"] == "P"]
                if not ind_df.empty
                else pd.DataFrame()
            )
            open_sells = (
                ind_df[ind_df["transaction_code"] == "S"]
                if not ind_df.empty
                else pd.DataFrame()
            )

            buys_val = (
                float(open_buys["total_value"].sum()) if not open_buys.empty else 0.0
            )
            sells_val = (
                float(open_sells["total_value"].sum()) if not open_sells.empty else 0.0
            )
            net_flow = buys_val - sells_val
            ratio = (
                buys_val / sells_val
                if sells_val > 0
                else (999.0 if buys_val > 0 else 0.0)
            )

            if ratio >= 2.0:
                sentiment = "Strong Buy Accumulation"
            elif ratio >= 1.2:
                sentiment = "Buy Accumulation"
            elif ratio >= 0.6:
                sentiment = "Neutral / Balanced"
            else:
                sentiment = "Distribution (Selling)"

            rows.append(
                IndustryHeatmapRow(
                    sector=sector_name,
                    industry=industry,
                    industry_slug=ind_slug,
                    company_count=len(companies),
                    open_buys_count=len(open_buys),
                    open_buys_dollar=round(buys_val, 2),
                    open_sells_count=len(open_sells),
                    open_sells_dollar=round(sells_val, 2),
                    net_dollar_flow=round(net_flow, 2),
                    buy_sell_ratio=round(ratio, 2),
                    sentiment=sentiment,
                )
            )

        res_df = pd.DataFrame([r.to_dict() for r in rows])
        if not res_df.empty:
            res_df = res_df.sort_values(
                ["buy_sell_ratio", "net_dollar_flow"], ascending=[False, False]
            ).reset_index(drop=True)
        return res_df

    @staticmethod
    def format_heatmap_markdown(df: pd.DataFrame) -> str:
        """Formats an industry heatmap DataFrame into a clean markdown table."""
        if df.empty:
            return "No industry trades found for the selected timeframe."

        lines = [
            "| Sector | Industry | Companies | Buys ($) | Sells ($) | Net Dollar Flow ($) | Buy/Sell Ratio | Sentiment |",
            "| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |",
        ]
        for _, r in df.iterrows():
            buys_fmt = f"${r['open_buys_dollar']:,.0f}"
            sells_fmt = f"${r['open_sells_dollar']:,.0f}"
            net_fmt = f"${r['net_dollar_flow']:,.0f}"
            ratio_fmt = f"{r['buy_sell_ratio']:.2f}x"
            lines.append(
                f"| {r['sector']} | {r['industry']} | {r['company_count']} | {buys_fmt} | {sells_fmt} | {net_fmt} | {ratio_fmt} | {r['sentiment']} |"
            )
        return "\n".join(lines)
