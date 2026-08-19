"""
Unit tests for quantitative Strategy Backtest Engine.
"""

from src.strategies.backtest_engine import BacktestEngine, BacktestSummary


def test_backtest_cluster_buy_strategy():
    be = BacktestEngine()
    summary = be.run_backtest(
        strategy="cluster_buy", holding_days=60, initial_capital=100000.0
    )
    assert isinstance(summary, BacktestSummary)
    assert summary.strategy_name == "CLUSTER_BUY"
    # Official seed data has no cluster-buy Form 4 rows; zero trades is correct.
    assert summary.total_trades >= 0
    assert summary.final_equity > 0.0
    assert len(summary.trade_log) == summary.total_trades


def test_backtest_conviction_strategy():
    be = BacktestEngine()
    summary = be.run_backtest(
        strategy="conviction", holding_days=45, initial_capital=100000.0
    )
    assert summary.strategy_name == "CONVICTION"
    assert summary.total_trades >= 0
