"""
Unit tests for Industry Organizer storage engine.
"""

import os
import pytest
import pandas as pd
from src.storage.industry_organizer import IndustryOrganizer
from src.universe.universe_manager import UniverseManager


def test_get_ticker_dir():
    io = IndustryOrganizer()
    path = io.get_ticker_dir("NVDA")
    assert "information_technology" in path.lower()
    assert "semiconductors" in path.lower()
    assert os.path.exists(path)


def test_add_and_get_trades(tmp_path):
    um = UniverseManager()
    io = IndustryOrganizer(base_dir=str(tmp_path), universe_manager=um)

    sample_trade = [
        {
            "ticker": "AAPL",
            "filing_date": "2026-07-28",
            "transaction_date": "2026-07-28",
            "reporting_owner_cik": "0001193125",
            "reporting_owner_name": "Cook Timothy D.",
            "officer_title": "Chief Executive Officer",
            "is_director": True,
            "is_officer": True,
            "is_ten_percent_owner": False,
            "transaction_code": "P",
            "acquired_disposed_code": "A",
            "shares": 1000.0,
            "price_per_share": 220.0,
            "total_value": 220000.0,
            "shares_owned_following": 3000000.0,
            "direct_or_indirect": "D",
            "is_open_market_buy": True,
            "is_open_market_sell": False,
            "accession_number": "0000320193-26-000001",
        }
    ]

    filepath = io.add_trades("AAPL", sample_trade, append=False)
    assert os.path.exists(filepath)

    df = io.get_ticker_trades("AAPL", year=2026)
    assert len(df) == 1
    assert df.iloc[0]["ticker"] == "AAPL"
    assert df.iloc[0]["transaction_code"] == "P"

    # Test year filter with non-matching year
    df_empty = io.get_ticker_trades("AAPL", year=2025)
    assert len(df_empty) == 0

    # Test industry summary generation
    summary = io.compute_industry_summary("Consumer Electronics", year=2026)
    assert summary["open_market_buys_count"] == 1
    assert summary["open_market_buys_dollar_value"] == 220000.0
