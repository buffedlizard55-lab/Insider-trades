"""
Unit tests for NASDAQ and S&P 500 Universe Manager.
"""

import pytest
from src.universe.universe_manager import UniverseManager, CompanyInfo


def test_universe_loading():
    um = UniverseManager()
    companies = um.get_all_companies()
    assert len(companies) > 50
    assert "AAPL" in [c.ticker for c in companies]
    assert "NVDA" in [c.ticker for c in companies]
    assert "MSFT" in [c.ticker for c in companies]


def test_get_company():
    um = UniverseManager()
    aapl = um.get_company("aapl")
    assert aapl is not None
    assert aapl.ticker == "AAPL"
    assert aapl.sector == "Information Technology"
    assert aapl.industry == "Consumer Electronics"
    assert aapl.cik == "0000320193"
    assert aapl.exchange == "NASDAQ"
    assert aapl.market_cap >= 1_000_000_000.0


def test_get_by_market_cap_filter():
    um = UniverseManager()
    companies_1b = um.get_by_market_cap(min_market_cap=1_000_000_000.0)
    assert len(companies_1b) > 50
    for c in companies_1b:
        assert c.market_cap >= 1_000_000_000.0


def test_get_by_sector_and_industry():
    um = UniverseManager()
    it_companies = um.get_by_sector("Information Technology")
    assert len(it_companies) >= 10

    semis = um.get_by_industry("Semiconductors")
    assert len(semis) >= 5
    tickers = [c.ticker for c in semis]
    assert "NVDA" in tickers
    assert "AVGO" in tickers


def test_list_sectors_and_industries():
    um = UniverseManager()
    sectors = um.list_sectors()
    assert "Information Technology" in sectors
    assert "Health Care" in sectors
    assert "Financials" in sectors
    assert len(sectors) == 11

    industries = um.list_industries(sector="Information Technology")
    assert "Semiconductors" in industries
    assert "Software - Infrastructure" in industries
