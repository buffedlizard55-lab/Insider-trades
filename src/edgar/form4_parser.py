"""
SEC EDGAR Form 4 XML Parser.
Parses official SEC Form 4 ownershipDocument XML files into structured Python
dataclasses and pandas DataFrames.
"""

import os
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
import xml.etree.ElementTree as ET
import pandas as pd


@dataclass
class Form4Transaction:
    accession_number: str
    filing_date: str
    period_of_report: str
    issuer_cik: str
    issuer_name: str
    issuer_ticker: str
    reporting_owner_cik: str
    reporting_owner_name: str
    is_director: bool
    is_officer: bool
    is_ten_percent_owner: bool
    is_other: bool
    officer_title: str
    security_title: str
    transaction_date: str
    transaction_code: str
    acquired_disposed_code: str
    shares: float
    price_per_share: float
    total_value: float
    shares_owned_following: float
    direct_or_indirect: str
    is_open_market_buy: bool
    is_open_market_sell: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Form4Filing:
    accession_number: str
    filing_date: str
    period_of_report: str
    issuer_cik: str
    issuer_name: str
    issuer_ticker: str
    reporting_owner_cik: str
    reporting_owner_name: str
    is_director: bool
    is_officer: bool
    is_ten_percent_owner: bool
    is_other: bool
    officer_title: str
    transactions: List[Form4Transaction]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "accession_number": self.accession_number,
            "filing_date": self.filing_date,
            "period_of_report": self.period_of_report,
            "issuer_cik": self.issuer_cik,
            "issuer_name": self.issuer_name,
            "issuer_ticker": self.issuer_ticker,
            "reporting_owner_cik": self.reporting_owner_cik,
            "reporting_owner_name": self.reporting_owner_name,
            "is_director": self.is_director,
            "is_officer": self.is_officer,
            "is_ten_percent_owner": self.is_ten_percent_owner,
            "is_other": self.is_other,
            "officer_title": self.officer_title,
            "transactions": [t.to_dict() for t in self.transactions],
        }

    def to_dataframe(self) -> pd.DataFrame:
        if not self.transactions:
            return pd.DataFrame()
        return pd.DataFrame([t.to_dict() for t in self.transactions])


class Form4Parser:
    """
    Parses SEC EDGAR Form 4 XML documents (ownershipDocument DTD) into structured
    Form4Filing and Form4Transaction records.
    """

    @classmethod
    def parse_file(cls, filepath: str, accession_number: Optional[str] = None, filing_date: Optional[str] = None) -> Form4Filing:
        """Parses a Form 4 XML file on disk."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Form 4 XML file not found: {filepath}")
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            xml_content = f.read()
        if not accession_number:
            base_name = os.path.basename(filepath)
            accession_number = base_name.replace(".xml", "")
        return cls.parse_string(xml_content, accession_number=accession_number, filing_date=filing_date)

    @classmethod
    def parse_string(
        cls,
        xml_string: str,
        accession_number: Optional[str] = "UNKNOWN",
        filing_date: Optional[str] = None,
    ) -> Form4Filing:
        """Parses an XML string representing an SEC Form 4 ownershipDocument."""
        try:
            root = ET.fromstring(xml_string)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML syntax in Form 4 document: {e}")

        # Strip namespace if present
        for elem in root.iter():
            if "}" in elem.tag:
                elem.tag = elem.tag.split("}", 1)[1]

        period_of_report = cls._get_text(root, "periodOfReport", "")
        if not filing_date:
            filing_date = period_of_report

        # Issuer details
        issuer_elem = root.find("issuer")
        issuer_cik = ""
        issuer_name = ""
        issuer_ticker = ""
        if issuer_elem is not None:
            issuer_cik = cls._get_text(issuer_elem, "issuerCik", "").zfill(10)
            issuer_name = cls._get_text(issuer_elem, "issuerName", "")
            issuer_ticker = cls._get_text(issuer_elem, "issuerTradingSymbol", "").upper()

        # Reporting Owner details
        rpt_elem = root.find("reportingOwner")
        rpt_cik = ""
        rpt_name = ""
        is_director = False
        is_officer = False
        is_ten_pct = False
        is_other = False
        officer_title = ""

        if rpt_elem is not None:
            id_elem = rpt_elem.find("reportingOwnerId")
            if id_elem is not None:
                rpt_cik = cls._get_text(id_elem, "rptOwnerCik", "").zfill(10)
                rpt_name = cls._get_text(id_elem, "rptOwnerName", "")

            rel_elem = rpt_elem.find("reportingOwnerRelationship")
            if rel_elem is not None:
                is_director = cls._get_bool(rel_elem, "isDirector")
                is_officer = cls._get_bool(rel_elem, "isOfficer")
                is_ten_pct = cls._get_bool(rel_elem, "isTenPercentOwner")
                is_other = cls._get_bool(rel_elem, "isOther")
                officer_title = cls._get_text(rel_elem, "officerTitle", "")

        transactions: List[Form4Transaction] = []

        # Parse non-derivative transactions
        non_deriv = root.find("nonDerivativeTable")
        if non_deriv is not None:
            for txn_elem in non_deriv.findall("nonDerivativeTransaction"):
                txn = cls._parse_transaction_element(
                    txn_elem=txn_elem,
                    accession_number=accession_number or "UNKNOWN",
                    filing_date=filing_date or "",
                    period_of_report=period_of_report,
                    issuer_cik=issuer_cik,
                    issuer_name=issuer_name,
                    issuer_ticker=issuer_ticker,
                    rpt_cik=rpt_cik,
                    rpt_name=rpt_name,
                    is_director=is_director,
                    is_officer=is_officer,
                    is_ten_pct=is_ten_pct,
                    is_other=is_other,
                    officer_title=officer_title,
                )
                if txn:
                    transactions.append(txn)

        # Parse derivative transactions (e.g. option conversions / exercises)
        deriv = root.find("derivativeTable")
        if deriv is not None:
            for txn_elem in deriv.findall("derivativeTransaction"):
                txn = cls._parse_transaction_element(
                    txn_elem=txn_elem,
                    accession_number=accession_number or "UNKNOWN",
                    filing_date=filing_date or "",
                    period_of_report=period_of_report,
                    issuer_cik=issuer_cik,
                    issuer_name=issuer_name,
                    issuer_ticker=issuer_ticker,
                    rpt_cik=rpt_cik,
                    rpt_name=rpt_name,
                    is_director=is_director,
                    is_officer=is_officer,
                    is_ten_pct=is_ten_pct,
                    is_other=is_other,
                    officer_title=officer_title,
                    is_derivative=True,
                )
                if txn:
                    transactions.append(txn)

        return Form4Filing(
            accession_number=accession_number or "UNKNOWN",
            filing_date=filing_date or "",
            period_of_report=period_of_report,
            issuer_cik=issuer_cik,
            issuer_name=issuer_name,
            issuer_ticker=issuer_ticker,
            reporting_owner_cik=rpt_cik,
            reporting_owner_name=rpt_name,
            is_director=is_director,
            is_officer=is_officer,
            is_ten_percent_owner=is_ten_pct,
            is_other=is_other,
            officer_title=officer_title,
            transactions=transactions,
        )

    @classmethod
    def _parse_transaction_element(
        cls,
        txn_elem: ET.Element,
        accession_number: str,
        filing_date: str,
        period_of_report: str,
        issuer_cik: str,
        issuer_name: str,
        issuer_ticker: str,
        rpt_cik: str,
        rpt_name: str,
        is_director: bool,
        is_officer: bool,
        is_ten_pct: bool,
        is_other: bool,
        officer_title: str,
        is_derivative: bool = False,
    ) -> Optional[Form4Transaction]:
        sec_title = cls._get_nested_text(txn_elem, "securityTitle", "value", "Common Stock")
        txn_date = cls._get_nested_text(txn_elem, "transactionDate", "value", period_of_report)

        coding_elem = txn_elem.find("transactionCoding")
        txn_code = ""
        if coding_elem is not None:
            txn_code = cls._get_text(coding_elem, "transactionCode", "").upper()

        amounts_elem = txn_elem.find("transactionAmounts")
        shares = 0.0
        price_per_share = 0.0
        acq_disp_code = ""
        if amounts_elem is not None:
            shares = cls._get_nested_float(amounts_elem, "transactionShares", "value", 0.0)
            price_per_share = cls._get_nested_float(amounts_elem, "transactionPricePerShare", "value", 0.0)
            acq_disp_code = cls._get_nested_text(amounts_elem, "transactionAcquiredDisposedCode", "value", "").upper()

        post_elem = txn_elem.find("postTransactionAmounts")
        shares_following = 0.0
        if post_elem is not None:
            shares_following = cls._get_nested_float(post_elem, "sharesOwnedFollowingTransaction", "value", 0.0)

        ownership_elem = txn_elem.find("ownershipNature")
        direct_or_indirect = "D"
        if ownership_elem is not None:
            val = cls._get_nested_text(ownership_elem, "directOrIndirectOwnership", "value", "D").upper()
            if val in ("D", "I"):
                direct_or_indirect = val

        total_value = round(shares * price_per_share, 2)
        is_open_market_buy = txn_code == "P"
        is_open_market_sell = txn_code == "S"

        return Form4Transaction(
            accession_number=accession_number,
            filing_date=filing_date,
            period_of_report=period_of_report,
            issuer_cik=issuer_cik,
            issuer_name=issuer_name,
            issuer_ticker=issuer_ticker,
            reporting_owner_cik=rpt_cik,
            reporting_owner_name=rpt_name,
            is_director=is_director,
            is_officer=is_officer,
            is_ten_percent_owner=is_ten_pct,
            is_other=is_other,
            officer_title=officer_title,
            security_title=sec_title,
            transaction_date=txn_date,
            transaction_code=txn_code,
            acquired_disposed_code=acq_disp_code,
            shares=shares,
            price_per_share=price_per_share,
            total_value=total_value,
            shares_owned_following=shares_following,
            direct_or_indirect=direct_or_indirect,
            is_open_market_buy=is_open_market_buy,
            is_open_market_sell=is_open_market_sell,
        )

    @staticmethod
    def _get_text(parent: ET.Element, tag: str, default: str = "") -> str:
        child = parent.find(tag)
        if child is not None and child.text is not None:
            return child.text.strip()
        return default

    @staticmethod
    def _get_bool(parent: ET.Element, tag: str) -> bool:
        child = parent.find(tag)
        if child is not None and child.text is not None:
            val = child.text.strip().lower()
            return val in ("1", "true", "yes", "y")
        return False

    @classmethod
    def _get_nested_text(cls, parent: ET.Element, child_tag: str, sub_tag: str, default: str = "") -> str:
        child = parent.find(child_tag)
        if child is not None:
            sub = child.find(sub_tag)
            if sub is not None and sub.text is not None:
                return sub.text.strip()
            # fallback to child's direct text
            if child.text is not None:
                return child.text.strip()
        return default

    @classmethod
    def _get_nested_float(cls, parent: ET.Element, child_tag: str, sub_tag: str, default: float = 0.0) -> float:
        text = cls._get_nested_text(parent, child_tag, sub_tag, "")
        if text:
            try:
                return float(text.replace(",", ""))
            except ValueError:
                return default
        return default
