#!/usr/bin/env python3
"""Remove fabricated insider-trade rows and write official seed records only."""

import csv
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRADE_HEADER = [
    "ticker",
    "company_name",
    "cik",
    "sector",
    "industry",
    "filing_date",
    "transaction_date",
    "reporting_owner_cik",
    "reporting_owner_name",
    "officer_title",
    "is_director",
    "is_officer",
    "is_ten_percent_owner",
    "transaction_code",
    "acquired_disposed_code",
    "shares",
    "price_per_share",
    "total_value",
    "shares_owned_following",
    "direct_or_indirect",
    "is_open_market_buy",
    "is_open_market_sell",
    "accession_number",
    "source_url",
]

# Official SEC Form 4 rows verified 2026-08-18 from EDGAR Archives.
OFFICIAL_SEEDS = {
    "AAPL": [
        {
            "ticker": "AAPL",
            "company_name": "Apple Inc.",
            "cik": "0000320193",
            "sector": "Information Technology",
            "industry": "Consumer Electronics",
            "filing_date": "2026-08-13",
            "transaction_date": "2026-08-11",
            "reporting_owner_cik": "0001780525",
            "reporting_owner_name": "Newstead Jennifer",
            "officer_title": "SVP, GC and Secretary",
            "is_director": False,
            "is_officer": True,
            "is_ten_percent_owner": False,
            "transaction_code": "S",
            "acquired_disposed_code": "D",
            "shares": 1439.0,
            "price_per_share": 307.75,
            "total_value": 442852.25,
            "shares_owned_following": 40107.0,
            "direct_or_indirect": "D",
            "is_open_market_buy": False,
            "is_open_market_sell": True,
            "accession_number": "0001140361-26-032884",
            "source_url": "https://www.sec.gov/Archives/edgar/data/320193/000114036126032884/0001140361-26-032884-index.htm",
        }
    ],
    "MSFT": [
        {
            "ticker": "MSFT",
            "company_name": "Microsoft Corporation",
            "cik": "0000789019",
            "sector": "Information Technology",
            "industry": "Software - Infrastructure",
            "filing_date": "2026-08-17",
            "transaction_date": "2026-08-17",
            "reporting_owner_cik": "0002062356",
            "reporting_owner_name": "Coleman Amy",
            "officer_title": "EVP, Chief Human Resources Off",
            "is_director": False,
            "is_officer": True,
            "is_ten_percent_owner": False,
            "transaction_code": "F",
            "acquired_disposed_code": "D",
            "shares": 89.044,
            "price_per_share": 495.40,
            "total_value": 44112.40,
            "shares_owned_following": 45323.5761,
            "direct_or_indirect": "D",
            "is_open_market_buy": False,
            "is_open_market_sell": False,
            "accession_number": "0000789019-26-000145",
            "source_url": "https://www.sec.gov/Archives/edgar/data/789019/000078901926000145/0000789019-26-000145-index.htm",
        }
    ],
}

GENERATED_PREFIXES = (
    "full_dataset_backtest_tracker",
    "strategy_comparison_",
    "active_entry_exit_predictions",
    "forward_test_results",
    "top2_",
    "top4_",
    "trades_2026_",
    "trades_all_years_",
    "selective_",
    "combined.json",
    "conviction.json",
    "industry_momentum.json",
    "strategies.json",
    "meta.json",
)


def write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=TRADE_HEADER)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def main():
    industries = ROOT / "data" / "industries"
    wiped = 0
    for csv_path in industries.rglob("*_insider_trades.csv"):
        ticker = csv_path.name.split("_")[0]
        write_csv(csv_path, OFFICIAL_SEEDS.get(ticker, []))
        wiped += 1
    print(f"rewrote {wiped} ticker trade files")

    # Industry summaries: recompute from remaining official rows only.
    summaries = []
    for summary_path in industries.rglob("industry_summary.json"):
        ind_dir = summary_path.parent
        frames = []
        for csv_path in ind_dir.glob("*_insider_trades.csv"):
            with csv_path.open(encoding="utf-8") as f:
                frames.extend(list(csv.DictReader(f)))
        buys = [r for r in frames if str(r.get("is_open_market_buy")).lower() == "true"]
        sells = [r for r in frames if str(r.get("is_open_market_sell")).lower() == "true"]
        buy_val = sum(float(r.get("total_value") or 0) for r in buys)
        sell_val = sum(float(r.get("total_value") or 0) for r in sells)
        # Keep existing sector/industry labels from the file if present.
        prev = {}
        try:
            prev = json.loads(summary_path.read_text(encoding="utf-8"))
        except Exception:
            pass
        payload = {
            "sector": prev.get("sector", ""),
            "industry": prev.get("industry", ind_dir.name),
            "industry_slug": prev.get("industry_slug", ind_dir.name),
            "year_filter": "ALL",
            "total_companies": len(list(ind_dir.glob("*_insider_trades.csv"))),
            "total_transactions": len(frames),
            "open_market_buys_count": len(buys),
            "open_market_buys_dollar_value": round(buy_val, 2),
            "open_market_sells_count": len(sells),
            "open_market_sells_dollar_value": round(sell_val, 2),
            "net_dollar_flow": round(buy_val - sell_val, 2),
            "buy_sell_dollar_ratio": (
                round(buy_val / sell_val, 2) if sell_val else (999.0 if buy_val else 0.0)
            ),
            "data_note": "Official SEC Form 4 rows only. Run `python main.py collect` to pull more filings.",
        }
        summary_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        summaries.append(payload)

    (ROOT / "data" / "summary_by_industry.json").write_text(
        json.dumps(summaries, indent=2) + "\n", encoding="utf-8"
    )
    if summaries:
        with (ROOT / "data" / "summary_by_industry.csv").open(
            "w", newline="", encoding="utf-8"
        ) as f:
            w = csv.DictWriter(f, fieldnames=list(summaries[0].keys()))
            w.writeheader()
            w.writerows(summaries)

    # Drop fabricated backtest / prediction artifacts (keep empty headers where useful).
    data_dir = ROOT / "data"
    removed = 0
    for path in list(data_dir.iterdir()):
        if not path.is_file():
            continue
        if any(path.name.startswith(p) or path.name == p for p in GENERATED_PREFIXES):
            path.unlink()
            removed += 1
    print(f"removed {removed} generated backtest/prediction artifacts")

    # Universe JSON mirror of the verified CSV.
    with (ROOT / "data" / "universe" / "nasdaq_sp500_universe.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["cik"] = str(row.get("cik", "")).zfill(10)
        try:
            row["market_cap"] = float(row.get("market_cap") or 0)
        except ValueError:
            row["market_cap"] = 0.0
        row["in_sp500"] = str(row.get("in_sp500", "")).lower() == "true"
        row["in_nasdaq100"] = str(row.get("in_nasdaq100", "")).lower() == "true"
    (ROOT / "data" / "universe" / "nasdaq_sp500_universe.json").write_text(
        json.dumps(rows, indent=2) + "\n", encoding="utf-8"
    )

    prices_readme = ROOT / "data" / "market_prices" / "README.md"
    prices_readme.write_text(
        """# Stored daily prices — not official exchange prints

Files in this folder are a **local cache** used by the backtester.

1. When the network is available, `python main.py prices --seed` tries Yahoo Finance
   chart history (`query1.finance.yahoo.com`).
2. If that fetch fails, the seeder writes a **deterministic interpolated fallback**
   (yearly anchors + hash noise). Those fallback rows are **not** NYSE/Nasdaq official
   last-sale prints and must not be cited as such.

SEC EDGAR does not publish daily equity prices. Official last-sale data comes from
the listing exchange.
""",
        encoding="utf-8",
    )

    print("done")


if __name__ == "__main__":
    main()
