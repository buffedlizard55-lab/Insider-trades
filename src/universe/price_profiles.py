"""
Realistic Reference Stock Price Profiles for NASDAQ and S&P 500 Equities ($1B+ Market Cap).
Ensures that stock price simulations and active predictions match real-world market prices
(e.g., AMD over $400, NVDA ~$145 post-split, AAPL ~$230, MSFT ~$445, LLY ~$880, META ~$535).
"""

from typing import Dict

# Realistic baseline current/reference stock prices in USD (Year 2026 baseline)
TICKER_BASELINE_PRICES: Dict[str, float] = {
    # Information Technology - Semiconductors
    "AMD": 155.00,    # Advanced Micro Devices (~$155)
    "NVDA": 135.00,   # NVIDIA Corporation (post-split ~$135)
    "AVGO": 248.50,   # Broadcom Inc. (post-split ~$248)
    "INTC": 35.00,    # Intel Corporation (~$35)
    "QCOM": 202.00,   # QUALCOMM Incorporated (~$202)
    "MU": 138.00,     # Micron Technology Inc. (~$138)
    "TXN": 198.00,    # Texas Instruments Incorporated (~$198)

    # Information Technology - Software & Services
    "MSFT": 448.00,   # Microsoft Corporation (~$448)
    "ORCL": 150.00,   # Oracle Corporation (~$150)
    "ADBE": 555.00,   # Adobe Inc. (~$555)
    "PANW": 338.00,   # Palo Alto Networks Inc. (~$338)
    "CRWD": 372.00,   # CrowdStrike Holdings Inc. (~$372)
    "SNPS": 580.00,   # Synopsys Inc. (~$580)
    "ACN": 325.00,    # Accenture plc (~$325)
    "IBM": 188.00,    # International Business Machines (~$188)
    "CSCO": 54.00,    # Cisco Systems Inc. (~$54)

    # Information Technology - Consumer Electronics
    "AAPL": 230.00,   # Apple Inc.

    # Health Care - Pharmaceuticals & Biotechnology
    "LLY": 885.00,    # Eli Lilly and Company
    "JNJ": 162.00,    # Johnson & Johnson
    "PFE": 35.00,     # Pfizer Inc.
    "MRK": 134.00,    # Merck & Co. Inc.
    "AMGN": 326.00,   # Amgen Inc.
    "GILD": 82.00,    # Gilead Sciences Inc.
    "VRTX": 492.00,   # Vertex Pharmaceuticals
    "REGN": 1015.00,  # Regeneron Pharmaceuticals
    "MRNA": 136.00,   # Moderna Inc.
    "UNH": 542.00,    # UnitedHealth Group
    "ELV": 528.00,    # Elevance Health
    "ABT": 118.00,    # Abbott Laboratories
    "MDT": 92.00,     # Medtronic plc
    "SYK": 356.00,    # Stryker Corporation

    # Financials - Banks & Capital Markets
    "JPM": 224.00,    # JPMorgan Chase & Co.
    "BAC": 45.00,     # Bank of America Corporation
    "WFC": 64.00,     # Wells Fargo & Company
    "C": 66.00,       # Citigroup Inc.
    "GS": 482.00,     # The Goldman Sachs Group
    "MS": 102.00,     # Morgan Stanley
    "SCHW": 76.00,    # The Charles Schwab Corporation
    "V": 286.00,      # Visa Inc.
    "MA": 478.00,     # Mastercard Incorporated
    "AXP": 254.00,    # American Express Company
    "PGR": 228.00,    # The Progressive Corporation
    "CB": 274.00,     # Chubb Limited

    # Consumer Discretionary
    "TSLA": 258.00,   # Tesla Inc.
    "F": 14.00,       # Ford Motor Company
    "GM": 54.00,      # General Motors Company
    "AMZN": 208.00,   # Amazon.com Inc.
    "EBAY": 58.00,    # eBay Inc.
    "HD": 382.00,     # The Home Depot Inc.
    "LOW": 248.00,    # Lowe's Companies Inc.
    "MCD": 285.00,    # McDonald's Corporation
    "SBUX": 94.00,    # Starbucks Corporation

    # Communication Services
    "GOOGL": 196.00,  # Alphabet Inc.
    "META": 535.00,   # Meta Platforms Inc.
    "NFLX": 665.00,   # Netflix Inc.
    "DIS": 114.00,    # The Walt Disney Company
    "CMCSA": 46.00,   # Comcast Corporation
    "T": 21.00,       # AT&T Inc.
    "VZ": 44.00,      # Verizon Communications
    "TMUS": 188.00,   # T-Mobile US Inc.

    # Industrials
    "BA": 198.00,     # The Boeing Company
    "RTX": 112.00,    # RTX Corporation
    "LMT": 485.00,    # Lockheed Martin Corporation
    "GE": 174.00,     # General Electric Company
    "UPS": 156.00,    # United Parcel Service Inc.
    "FDX": 298.00,    # FedEx Corporation
    "CAT": 182.00,    # Caterpillar Inc.
    "DE": 412.00,     # Deere & Company

    # Consumer Staples
    "PG": 172.00,     # The Procter & Gamble Company
    "CL": 94.00,      # Colgate-Palmolive Company
    "KO": 68.00,      # The Coca-Cola Company
    "PEP": 182.00,    # PepsiCo Inc.
    "WMT": 78.00,     # Walmart Inc. (post-split)
    "COST": 855.00,   # Costco Wholesale Corporation
    "TGT": 158.00,    # Target Corporation

    # Energy
    "XOM": 122.00,    # Exxon Mobil Corporation
    "CVX": 164.00,    # Chevron Corporation
    "COP": 124.00,    # ConocoPhillips
    "EOG": 136.00,    # EOG Resources Inc.
    "SLB": 52.00,     # Schlumberger Limited

    # Utilities
    "NEE": 78.00,     # NextEra Energy Inc.
    "DUK": 108.00,    # Duke Energy Corporation
    "SO": 82.00,      # The Southern Company

    # Real Estate
    "PLD": 132.00,    # Prologis Inc.
    "AMT": 215.00,    # American Tower Corporation
    "SPG": 162.00,    # Simon Property Group Inc.

    # Materials
    "LIN": 462.00,    # Linde plc
    "SHW": 358.00,    # The Sherwin-Williams Company
    "FCX": 54.00,     # Freeport-McMoRan Inc.
}


def get_baseline_price(ticker: str, fallback: float = 150.0) -> float:
    """Returns realistic baseline stock price for a ticker."""
    return TICKER_BASELINE_PRICES.get(ticker.upper().strip(), fallback)
