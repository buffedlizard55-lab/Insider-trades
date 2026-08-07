"""
Integration tests for CLI subcommands.
"""

import os
import pytest
from src.cli import main


def test_cli_sources(capsys):
    ret = main(["sources"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "SECTION 16(A)" in captured.out.upper()
    assert "TRANSACTION CODES" in captured.out.upper()


def test_cli_universe(capsys):
    ret = main(["universe", "--sector", "Information Technology", "--min-market-cap", "1000000000"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "AAPL" in captured.out
    assert "NVDA" in captured.out


def test_cli_parse_xml(capsys):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sample_path = os.path.join(root_dir, "data", "sample_xmls", "AAPL_0000320193_form4_sample1.xml")
    ret = main(["parse-xml", "--file", sample_path])
    assert ret == 0
    captured = capsys.readouterr()
    assert "Cook Timothy D." in captured.out


def test_cli_heatmap(capsys):
    ret = main(["heatmap", "--days", "365"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "Sector" in captured.out
    assert "Industry" in captured.out


def test_cli_signals(capsys):
    ret = main(["signals", "--ticker", "NVDA", "--year", "2026"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "NVDA" in captured.out


def test_cli_backtest(capsys):
    ret = main(["backtest", "--strategy", "cluster_buy"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "QUANTITATIVE BACKTEST REPORT" in captured.out


def test_cli_sweep(capsys):
    ret = main(["sweep", "--year", "2026"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "HIGHEST ROI BACKTEST CONFIGURATION" in captured.out


def test_cli_full_backtest(capsys):
    ret = main(["full-backtest"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "CATEGORY WINNERS" in captured.out
