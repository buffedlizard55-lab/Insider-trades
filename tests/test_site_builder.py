"""
Unit tests for the GitHub Pages dashboard site builder.
"""

import json
import os

from src.strategies.site_builder import STRATEGIES, build_site_data

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(REPO_ROOT, "data")


def test_build_writes_all_expected_files(tmp_path):
    summary = build_site_data(data_dir=DATA_DIR, out_dir=str(tmp_path))
    expected = ["meta.json", "strategies.json"] + [f"{s['key']}.json" for s in STRATEGIES]
    for fname in expected:
        assert os.path.exists(os.path.join(tmp_path, fname)), f"missing {fname}"
    assert summary["generated_at"].startswith("20")


def test_meta_does_not_claim_complete_sp500(tmp_path):
    build_site_data(data_dir=DATA_DIR, out_dir=str(tmp_path))
    meta = json.load(open(os.path.join(tmp_path, "meta.json")))
    assert meta["strategy_count"] == 3
    assert "not the complete S&P 500" in meta["universe_note"]
    assert "SEC EDGAR Form 4" in meta["universe_note"]


def test_overview_ranks_top3_in_order(tmp_path):
    build_site_data(data_dir=DATA_DIR, out_dir=str(tmp_path))
    overview = json.load(open(os.path.join(tmp_path, "strategies.json")))
    assert [s["rank"] for s in overview] == [1, 2, 3]
    assert [s["key"] for s in overview] == ["combined", "industry_momentum", "conviction"]


def test_empty_official_dataset_has_zero_or_more_trades(tmp_path):
    build_site_data(data_dir=DATA_DIR, out_dir=str(tmp_path))
    for cfg in STRATEGIES:
        payload = json.load(open(os.path.join(tmp_path, f"{cfg['key']}.json")))
        assert payload["kpis"]["total_trades"] >= 0
        assert isinstance(payload["trades"], list)
        assert isinstance(payload["active"], list)
