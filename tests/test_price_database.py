"""
Unit tests for Daily Stock Price Database storage and lookup engine.
"""

import os
import pytest
import pandas as pd
from src.universe.price_database import PriceDatabase


def test_get_daily_close():
    pdb = PriceDatabase()
    # Test AVGO closing price lookup on 2026-03-04
    p_avgo = pdb.get_daily_close("AVGO", "2026-03-04")
    assert p_avgo > 0.0
    assert 220.0 <= p_avgo <= 270.0  # Real post-split AVGO price range

    # Test AMD closing price lookup
    p_amd = pdb.get_daily_close("AMD", "2026-08-02")
    assert p_amd > 0.0
    assert 130.0 <= p_amd <= 180.0  # Real AMD price range


def test_get_price_series():
    pdb = PriceDatabase()
    df = pdb.get_price_series("AVGO")
    assert not df.empty
    assert "date" in df.columns
    assert "close" in df.columns
    assert "volume" in df.columns


def test_seed_price_files(tmp_path):
    pdb = PriceDatabase(data_dir=str(tmp_path))
    count = pdb.seed_all_daily_price_files(tickers=["AAPL", "MSFT"], overwrite=True)
    assert count == 2
    assert os.path.exists(os.path.join(str(tmp_path), "AAPL_daily_prices.csv"))
    assert os.path.exists(os.path.join(str(tmp_path), "MSFT_daily_prices.csv"))
