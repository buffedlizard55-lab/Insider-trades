"""
Unit tests for quantitative Insider Signal Generator.
"""

import pandas as pd
from src.strategies.signal_generator import SignalGenerator
from src.universe.universe_manager import UniverseManager


def test_detect_conviction_buy_signal():
    sg = SignalGenerator()
    data = [
        {
            "transaction_date": "2026-07-20",
            "reporting_owner_name": "Tim Cook",
            "officer_title": "Chief Executive Officer",
            "transaction_code": "P",
            "total_value": 500000.0,
            "shares": 2500.0,
            "price_per_share": 200.0,
        }
    ]
    df = pd.DataFrame(data)
    signals = sg.generate_signals_for_ticker("AAPL", df, min_confidence=70)
    assert len(signals) == 1
    assert signals[0].signal_type == SignalGenerator.CONVICTION_BUY
    assert signals[0].confidence_score >= 90
    assert "C-Suite Conviction Buy" in signals[0].rationale


def test_detect_cluster_buy_signal():
    sg = SignalGenerator()
    data = [
        {
            "transaction_date": "2026-07-20",
            "reporting_owner_name": "Insider One",
            "officer_title": "Director",
            "transaction_code": "P",
            "total_value": 150000.0,
        },
        {
            "transaction_date": "2026-07-22",
            "reporting_owner_name": "Insider Two",
            "officer_title": "Chief Financial Officer",
            "transaction_code": "P",
            "total_value": 200000.0,
        },
    ]
    df = pd.DataFrame(data)
    signals = sg.generate_signals_for_ticker("NVDA", df, min_confidence=70)
    assert any(s.signal_type == SignalGenerator.CLUSTER_BUY for s in signals)


def test_detect_heavy_sell_exit_signal():
    sg = SignalGenerator()
    data = [
        {
            "transaction_date": "2026-07-15",
            "reporting_owner_name": "Exec A",
            "officer_title": "Director",
            "transaction_code": "S",
            "total_value": 800000.0,
        },
        {
            "transaction_date": "2026-07-17",
            "reporting_owner_name": "Exec B",
            "officer_title": "VP",
            "transaction_code": "S",
            "total_value": 700000.0,
        },
    ]
    df = pd.DataFrame(data)
    signals = sg.generate_signals_for_ticker("MSFT", df, min_confidence=60)
    assert any(s.signal_type == SignalGenerator.HEAVY_SELL_EXIT for s in signals)
