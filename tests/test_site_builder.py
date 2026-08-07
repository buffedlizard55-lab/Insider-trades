"""
Unit tests for the GitHub Pages dashboard site builder
(src/strategies/site_builder.py).
"""

import json
import os

import pandas as pd
import pytest

from src.strategies.site_builder import (
    STRATEGIES,
    build_site_data,
)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(REPO_ROOT, "data")


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    """Builds the dashboard payloads once into a temp directory."""
    out = tmp_path_factory.mktemp("site_data")
    summary = build_site_data(data_dir=DATA_DIR, out_dir=str(out))
    return summary, str(out)


@pytest.fixture(scope="module")
def payloads(built):
    _, out = built
    return {cfg["key"]: json.load(open(os.path.join(out, f"{cfg['key']}.json"))) for cfg in STRATEGIES}


def test_build_writes_all_expected_files(built):
    _, out = built
    expected = ["meta.json", "strategies.json"] + [f"{s['key']}.json" for s in STRATEGIES]
    for fname in expected:
        assert os.path.exists(os.path.join(out, fname)), f"missing {fname}"


def test_meta_has_generated_at_and_sources(built):
    _, out = built
    meta = json.load(open(os.path.join(out, "meta.json")))
    assert meta["generated_at"].startswith("20")
    assert meta["strategy_count"] == 3
    assert any(f.endswith("COMBINED_90D_trade_log.csv") for f in meta["source_files"])


def test_overview_ranks_top3_in_order(built):
    _, out = built
    overview = json.load(open(os.path.join(out, "strategies.json")))
    assert len(overview) == 3
    assert [s["rank"] for s in overview] == [1, 2, 3]
    assert [s["key"] for s in overview] == ["combined", "industry_momentum", "conviction"]
    # KPI sanity: ROI descends across ranks
    rois = [s["kpis"]["total_return_pct"] for s in overview]
    assert rois == sorted(rois, reverse=True)


def test_trade_logs_match_source_csvs(payloads):
    for cfg in STRATEGIES:
        src = pd.read_csv(os.path.join(DATA_DIR, f"{cfg['csv_name']}.csv"))
        assert len(payloads[cfg["key"]]["trades"]) == len(src)


def test_trade_rows_contain_display_fields(payloads):
    for cfg in STRATEGIES:
        first = payloads[cfg["key"]]["trades"][0]
        for field in [
            "ticker", "company", "industry", "entry_date", "entry_signal",
            "entry_price", "exit_date", "exit_reason", "exit_price",
            "holding_days", "return_pct", "pnl_dollar", "confidence", "url",
        ]:
            assert field in first, f"{cfg['key']} trade missing {field}"


def test_trades_sorted_newest_first(payloads):
    for cfg in STRATEGIES:
        dates = [t["entry_date"] for t in payloads[cfg["key"]]["trades"]]
        assert dates == sorted(dates, reverse=True)


def test_active_mapping_combined(payloads):
    preds = pd.read_csv(os.path.join(DATA_DIR, "active_entry_exit_predictions.csv"))
    expected = preds[
        (preds["action"] == "BUY_ENTRY_TARGET")
        & (preds["strategy_source"].isin(["CONVICTION_BUY", "CLUSTER_BUY"]))
    ]
    active = payloads["combined"]["active"]
    assert len(active) == len(expected)
    assert all(a["confidence"] >= 70 for a in active)


def test_active_mapping_conviction(payloads):
    preds = pd.read_csv(os.path.join(DATA_DIR, "active_entry_exit_predictions.csv"))
    expected = preds[
        (preds["action"] == "BUY_ENTRY_TARGET")
        & (preds["strategy_source"] == "CONVICTION_BUY")
    ]
    assert len(payloads["conviction"]["active"]) == len(expected)


def test_active_mapping_industry_momentum_confidence_floor(payloads):
    preds = pd.read_csv(os.path.join(DATA_DIR, "active_entry_exit_predictions.csv"))
    expected = preds[
        (preds["action"] == "BUY_ENTRY_TARGET") & (preds["confidence_score"] >= 75)
    ]
    active = payloads["industry_momentum"]["active"]
    assert len(active) == len(expected)
    assert all(a["confidence"] >= 75 for a in active)


def test_active_sorted_newest_first(payloads):
    for cfg in STRATEGIES:
        dates = [a["trigger_date"] for a in payloads[cfg["key"]]["active"]]
        assert dates == sorted(dates, reverse=True)


def test_kpis_match_full_dataset_tracker(payloads):
    tracker = pd.read_csv(os.path.join(DATA_DIR, "full_dataset_backtest_tracker.csv"))
    for cfg in STRATEGIES:
        row = tracker[
            (tracker["strategy"] == cfg["name"]) & (tracker["holding_days"] == 90)
        ].iloc[0]
        k = payloads[cfg["key"]]["kpis"]
        assert k["total_trades"] == int(row["total_trades"])
        assert abs(k["total_return_pct"] - row["total_return_pct"]) < 0.01
        assert abs(k["win_rate_pct"] - row["win_rate_pct"]) < 0.01
