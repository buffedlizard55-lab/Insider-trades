"""
Unit tests for SEC EDGAR Form 4 XML parser using official sample filings.
"""

import os
import pytest
from src.edgar.form4_parser import Form4Parser, Form4Filing


def test_parse_aapl_official_form4():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sample_path = os.path.join(
        root_dir, "data", "sample_xmls", "AAPL_0000320193_form4_sample1.xml"
    )
    assert os.path.exists(sample_path), "AAPL official sample XML missing"

    filing = Form4Parser.parse_file(sample_path)
    assert isinstance(filing, Form4Filing)
    assert filing.issuer_ticker == "AAPL"
    assert filing.issuer_cik == "0000320193"
    assert filing.reporting_owner_name == "Newstead Jennifer"
    assert filing.is_officer is True
    assert filing.officer_title == "SVP, GC and Secretary"
    assert len(filing.transactions) == 1

    txn = filing.transactions[0]
    assert txn.transaction_code == "S"
    assert txn.is_open_market_sell is True
    assert txn.is_open_market_buy is False
    assert txn.shares == 1439.0
    assert txn.price_per_share == 307.75
    assert txn.total_value == pytest.approx(1439.0 * 307.75)
    assert txn.direct_or_indirect == "D"


def test_parse_msft_official_form4():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sample_path = os.path.join(
        root_dir, "data", "sample_xmls", "MSFT_0000789019_form4_sample1.xml"
    )
    filing = Form4Parser.parse_file(sample_path)

    assert filing.issuer_ticker == "MSFT"
    assert filing.issuer_cik == "0000789019"
    assert filing.reporting_owner_name == "Coleman Amy"
    assert len(filing.transactions) >= 1
    t = filing.transactions[0]
    assert t.transaction_code == "F"
    assert t.shares == pytest.approx(89.044)
    assert t.price_per_share == pytest.approx(495.40)


def test_parse_nvda_official_form4():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sample_path = os.path.join(
        root_dir, "data", "sample_xmls", "NVDA_0001045810_form4_sample1.xml"
    )
    filing = Form4Parser.parse_file(sample_path)

    assert filing.issuer_ticker == "NVDA"
    assert filing.issuer_cik == "0001045810"
    assert filing.reporting_owner_name == "NORA JOHNSON SUZANNE M"
    assert len(filing.transactions) >= 1
    assert filing.transactions[0].transaction_code == "A"


def test_parse_string_invalid_xml():
    with pytest.raises(ValueError, match="Invalid XML syntax"):
        Form4Parser.parse_string("<invalid><xml>")
