"""
Unit tests for SEC EDGAR Form 4 XML parser.
"""

import os
import pytest
from src.edgar.form4_parser import Form4Parser, Form4Filing


def test_parse_aapl_sample_xml():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sample_path = os.path.join(root_dir, "data", "sample_xmls", "AAPL_0000320193_form4_sample1.xml")
    assert os.path.exists(sample_path), "AAPL sample XML missing"

    filing = Form4Parser.parse_file(sample_path)
    assert isinstance(filing, Form4Filing)
    assert filing.issuer_ticker == "AAPL"
    assert filing.issuer_cik == "0000320193"
    assert filing.reporting_owner_name == "Cook Timothy D."
    assert filing.is_director is True
    assert filing.is_officer is True
    assert filing.officer_title == "Chief Executive Officer"
    assert len(filing.transactions) == 1

    txn = filing.transactions[0]
    assert txn.transaction_code == "P"
    assert txn.is_open_market_buy is True
    assert txn.shares == 10000.0
    assert txn.price_per_share == 225.50
    assert txn.total_value == 2255000.0
    assert txn.direct_or_indirect == "D"


def test_parse_nvda_sample_xml():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sample_path = os.path.join(root_dir, "data", "sample_xmls", "NVDA_0001045810_form4_sample1.xml")
    filing = Form4Parser.parse_file(sample_path)

    assert filing.issuer_ticker == "NVDA"
    assert filing.issuer_cik == "0001045810"
    assert len(filing.transactions) >= 1
    t = filing.transactions[0]
    assert t.transaction_code == "P"
    assert t.shares == 5000.0


def test_parse_string_invalid_xml():
    with pytest.raises(ValueError, match="Invalid XML syntax"):
        Form4Parser.parse_string("<invalid><xml>")
