"""
Command-Line Interface (CLI) for Insider-trades repository.
Provides subcommands for querying official SEC EDGAR sources, exploring the
NASDAQ/S&P 500 universe ($1B+ market cap focus), viewing industry heatmaps,
generating insider signals, running quantitative strategy backtests, collecting
insider trades by year (or across all historical years 2021-2026), and
sweeping/comparing strategy ROI performance.
"""

import os
import sys
import argparse
import json
import logging
from typing import Optional, List
import pandas as pd
from tabulate import tabulate

from src.universe.universe_manager import UniverseManager
from src.edgar.form4_parser import Form4Parser
from src.storage.industry_organizer import IndustryOrganizer
from src.strategies.signal_generator import SignalGenerator
from src.strategies.backtest_engine import BacktestEngine
from src.strategies.industry_analytics import IndustryAnalytics


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def cmd_sources(args: argparse.Namespace) -> int:
    """Prints exhaustive information on the official SEC EDGAR data source."""
    doc = """
================================================================================
         OFFICIAL, VERIFIABLE & UP-TO-DATE INSIDER TRADING SOURCE
================================================================================

1. PRIMARY SOURCE: U.S. Securities and Exchange Commission (SEC) EDGAR
   - Legal Mandate: Section 16(a) of the Securities Exchange Act of 1934
   - Filing Window: Within 2 business days of the transaction date (SOX Section 403)
   - Covered Insiders: Executive Officers (CEO, CFO, COO), Directors, and 10% Owners
   - Data Format: Official structured XML documents (`ownershipDocument` DTD)

2. FORM 4 TRANSACTION CODES (KEY SIGNALS):
   - `P` (Open Market Purchase): STRONGEST BULLISH SIGNAL. Insider risking personal cash.
   - `S` (Open Market Sale): BEARISH / EXIT SIGNAL. Executing open-market sale.
   - `A` (Award / Grant): NEUTRAL. Compensation award (Rule 16b-3(d)).
   - `M` (Option Exercise): NEUTRAL. Conversion/exercise of derivative security.
   - `F` (Tax Withholding): NEUTRAL. Withholding shares for tax liability.

3. PROGRAMMATIC ACCESS ENDPOINTS:
   - EDGAR Real-Time RSS Feed: https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=4&output=atom
   - EDGAR Submissions API:    https://data.sec.gov/submissions/CIK{cik_10_digits}.json
   - Company Tickers Mapping:   https://www.sec.gov/files/company_tickers.json

4. SEC COMPLIANCE & RATE LIMITS:
   - Requires custom `User-Agent` header with contact email.
   - Strictly limited to 10 requests per second.
================================================================================
"""
    print(doc)
    return 0


def cmd_universe(args: argparse.Namespace) -> int:
    """Displays companies in the NASDAQ & S&P 500 universe ($1B+ market cap focus)."""
    um = UniverseManager()
    if args.ticker:
        comp = um.get_company(args.ticker)
        if not comp:
            print(f"Error: Ticker '{args.ticker}' not found in universe.", file=sys.stderr)
            return 1
        print(json.dumps(comp.to_dict(), indent=2))
        return 0

    companies = um.get_filtered_companies(
        min_market_cap=args.min_market_cap,
        sector=args.sector,
        industry=args.industry,
        exchange=args.exchange,
    )

    if not companies:
        print("No matching companies found.", file=sys.stderr)
        return 1

    df = pd.DataFrame([c.to_dict() for c in companies])
    df["market_cap_billions"] = (df["market_cap"] / 1_000_000_000.0).round(2)
    cols = [
        "ticker",
        "company_name",
        "cik",
        "exchange",
        "sector",
        "industry",
        "market_cap_billions",
    ]
    if args.format == "json":
        print(df[cols].to_json(orient="records", indent=2))
    else:
        print(tabulate(df[cols], headers="keys", tablefmt="simple", showindex=False))
        print(
            f"\nTotal companies listed (Market Cap >= ${args.min_market_cap/1e9:,.1f}B): {len(df)}"
        )
    return 0


def cmd_parse_xml(args: argparse.Namespace) -> int:
    """Parses an SEC Form 4 XML file and prints out the transaction details."""
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    filing = Form4Parser.parse_file(args.file)
    print(
        "================================================================================"
    )
    print(f"SEC Form 4 Filing — Accession: {filing.accession_number}")
    print(
        f"Issuer: {filing.issuer_name} ({filing.issuer_ticker}) | CIK: {filing.issuer_cik}"
    )
    print(
        f"Reporting Owner: {filing.reporting_owner_name} | Title: {filing.officer_title or 'Director/Owner'}"
    )
    print(
        "================================================================================"
    )

    df = filing.to_dataframe()
    if df.empty:
        print("No transactions found in Form 4 document.")
        return 0

    cols = [
        "transaction_date",
        "transaction_code",
        "acquired_disposed_code",
        "shares",
        "price_per_share",
        "total_value",
        "shares_owned_following",
        "direct_or_indirect",
    ]
    print(tabulate(df[cols], headers="keys", tablefmt="simple", showindex=False))
    return 0


def cmd_heatmap(args: argparse.Namespace) -> int:
    """Displays the cross-industry insider sentiment heatmap."""
    ia = IndustryAnalytics()
    df = ia.generate_heatmap(days=args.days, sector_filter=args.sector)
    if df.empty:
        print("No industry trades found for the selected timeframe.")
        return 0

    if args.format == "markdown":
        print(ia.format_heatmap_markdown(df))
    elif args.format == "json":
        print(df.to_json(orient="records", indent=2))
    else:
        cols = [
            "sector",
            "industry",
            "company_count",
            "open_buys_dollar",
            "open_sells_dollar",
            "net_dollar_flow",
            "buy_sell_ratio",
            "sentiment",
        ]
        headers = [
            "Sector",
            "Industry",
            "Companies",
            "Buys ($)",
            "Sells ($)",
            "Net Flow ($)",
            "Ratio",
            "Sentiment",
        ]
        print(
            f"\n--- INDUSTRY INSIDER SENTIMENT HEATMAP (Trailing {args.days} Days) ---\n"
        )
        print(
            tabulate(
                df[cols],
                headers=headers,
                tablefmt="simple",
                showindex=False,
                floatfmt=(".0f", ".0f", ".0f", ".0f", ".0f", ".0f", ".2f", ""),
            )
        )
        print(f"\nTotal industries listed: {len(df)}\n")
    return 0


def cmd_signals(args: argparse.Namespace) -> int:
    """Generates and displays insider trading entry and exit signals."""
    um = UniverseManager()
    sg = SignalGenerator(um)
    io = IndustryOrganizer(universe_manager=um)

    target_year = None if args.year == 0 else args.year

    if args.ticker:
        comp = um.get_company(args.ticker)
        companies = [comp] if comp else []
    elif args.industry:
        companies = um.get_filtered_companies(
            min_market_cap=args.min_market_cap, industry=args.industry
        )
    else:
        companies = um.get_filtered_companies(min_market_cap=args.min_market_cap)

    all_signals = []
    for comp in companies:
        df = io.get_ticker_trades(comp.ticker, year=target_year)
        sigs = sg.generate_signals_for_ticker(
            comp.ticker, df, min_confidence=args.min_confidence
        )
        all_signals.extend(sigs)

    all_signals.sort(key=lambda x: x.date, reverse=True)

    if not all_signals:
        yr_str = f"year {target_year}" if target_year else "all years (2021-2026)"
        print(
            f"No signals found matching confidence >= {args.min_confidence}% for {yr_str}."
        )
        return 0

    df = pd.DataFrame([s.to_dict() for s in all_signals])
    cols = [
        "date",
        "ticker",
        "industry",
        "signal_type",
        "confidence_score",
        "dollar_value",
        "insider_count",
        "rationale",
    ]
    if args.format == "json":
        print(df[cols].to_json(orient="records", indent=2))
    else:
        print(
            tabulate(
                df[cols],
                headers="keys",
                tablefmt="simple",
                showindex=False,
            )
        )
        yr_label = str(target_year) if target_year else "2021-2026"
        print(
            f"\nTotal signals detected ({yr_label}, Market Cap >= ${args.min_market_cap/1e9:,.1f}B): {len(df)}"
        )
    return 0


def cmd_backtest(args: argparse.Namespace) -> int:
    """Executes a quantitative strategy backtest and displays performance report."""
    be = BacktestEngine()
    target_year = None if args.year == 0 else args.year
    summary = be.run_backtest(
        strategy=args.strategy,
        ticker=args.ticker,
        industry=args.industry,
        sector=args.sector,
        year=target_year,
        holding_days=args.holding_days,
        stop_loss_pct=args.stop_loss,
        take_profit_pct=args.take_profit,
        initial_capital=args.initial_capital,
        min_market_cap=args.min_market_cap,
    )

    yr_label = str(target_year) if target_year else "2021-2026"
    print(
        "================================================================================"
    )
    print(f"       QUANTITATIVE BACKTEST REPORT ({yr_label}): {summary.strategy_name}")
    print(
        "================================================================================"
    )
    print(f"Initial Capital      : ${summary.initial_capital:,.2f}")
    print(f"Final Equity         : ${summary.final_equity:,.2f}")
    print(f"Total Return (%)     : {summary.total_return_pct:.2f}%")
    print(f"Total Completed Trades: {summary.total_trades}")
    print(
        f"Winning / Losing     : {summary.winning_trades} Win / {summary.losing_trades} Loss"
    )
    print(f"Win Rate (%)         : {summary.win_rate_pct:.2f}%")
    print(f"Profit Factor        : {summary.profit_factor:.2f}")
    print(f"Estimated Sharpe     : {summary.sharpe_ratio:.2f}")
    print(f"Maximum Drawdown (%) : {summary.max_drawdown_pct:.2f}%")
    print(
        "================================================================================\n"
    )

    if args.show_log and summary.trade_log:
        df = summary.to_dataframe()
        cols = [
            "ticker",
            "entry_date",
            "entry_price",
            "exit_date",
            "exit_reason",
            "exit_price",
            "holding_days",
            "return_pct",
            "pnl_dollar",
        ]
        print("--- TRADE EXECUTION LOG ---")
        print(tabulate(df[cols], headers="keys", tablefmt="simple", showindex=False))
        print("")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(summary.to_dict(), f, indent=2)
        print(f"Saved backtest report JSON to {args.output}")

    return 0


def cmd_sweep(args: argparse.Namespace) -> int:
    """
    Executes a multi-strategy parameter sweep across all $1B+ market cap companies,
    ranks ROI performance, and notes the highest returning backtest configuration.
    """
    be = BacktestEngine()
    target_year = None if args.year == 0 else args.year
    yr_label = str(target_year) if target_year else "2021-2026 (6-YEAR FULL CYCLE)"
    print(
        f"Running multi-strategy parameter sweep across {yr_label} "
        f"(Market Cap >= ${args.min_market_cap/1e9:,.1f}B)..."
    )
    df, results, best = be.run_strategy_sweep(
        year=target_year,
        initial_capital=args.initial_capital,
        min_market_cap=args.min_market_cap,
    )

    cols = [
        "strategy",
        "holding_days",
        "total_trades",
        "win_rate_pct",
        "profit_factor",
        "sharpe_ratio",
        "max_drawdown_pct",
        "total_return_pct",
    ]
    headers = [
        "Strategy",
        "Holding (Days)",
        "Trades",
        "Win Rate (%)",
        "Profit Factor",
        "Sharpe",
        "Max DD (%)",
        "Total Return (%)",
    ]

    print("\n================================================================================")
    print(f"      STRATEGY BACKTEST SWEEP & ROI RANKINGS ({yr_label})")
    print("================================================================================\n")
    print(
        tabulate(
            df[cols],
            headers=headers,
            tablefmt="simple",
            showindex=False,
            floatfmt=("", "", "", ".2f", ".2f", ".2f", ".2f", ".2f"),
        )
    )

    print("\n================================================================================")
    print("                *** #1 HIGHEST ROI BACKTEST CONFIGURATION ***                   ")
    print("================================================================================")
    print(f"  Strategy Name      : {best.strategy_name}")
    print(f"  Holding Period     : {best.holding_days} trading days")
    print(f"  Win Rate           : {best.win_rate_pct:.2f}% ({best.winning_trades} Wins / {best.losing_trades} Losses)")
    print(f"  Profit Factor      : {best.profit_factor:.2f}")
    print(f"  Estimated Sharpe   : {best.sharpe_ratio:.2f}")
    print(f"  Max Drawdown       : {best.max_drawdown_pct:.2f}%")
    print(f"  Total Return (ROI) : {best.total_return_pct:.2f}%")
    print(f"  Final Equity       : ${best.final_equity:,.2f} (from ${best.initial_capital:,.2f} initial)")
    print("================================================================================\n")

    if args.show_log and best.trade_log:
        tdf = best.to_dataframe()
        tcols = [
            "ticker",
            "industry",
            "entry_date",
            "entry_price",
            "exit_date",
            "exit_reason",
            "exit_price",
            "return_pct",
            "pnl_dollar",
        ]
        print("--- TOP STRATEGY TRADE BREAKDOWN (FIRST 15 TRADES) ---")
        print(tabulate(tdf[tcols].head(15), headers="keys", tablefmt="simple", showindex=False))
        print("")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(best.to_dict(), f, indent=2)
        print(f"Saved top strategy backtest report to {args.output}")

    return 0


def cmd_analyze_top4(args: argparse.Namespace) -> int:
    """
    Executes deep-dive individual analysis for the Top 4 performing strategies,
    saving complete trade logs and displaying easy-to-read tables with trigger links.
    """
    from src.strategies.analyze_top4_strategies import Top4StrategiesAnalyzer

    print(
        f"Executing deep-dive individual analysis for the Top 4 Performing Strategies "
        f"(Market Cap >= ${args.min_market_cap/1e9:,.1f}B)..."
    )
    t4 = Top4StrategiesAnalyzer(
        initial_capital=args.initial_capital, min_market_cap=args.min_market_cap
    )
    sums = t4.analyze_top4()
    md = t4.generate_markdown_report(sums)

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    doc_path = os.path.join(root_dir, "docs", "TOP4_STRATEGIES_INDIVIDUAL_ANALYSIS.md")
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(md)

    cols = [
        "strategy_name",
        "holding_days",
        "total_trades",
        "win_rate_pct",
        "profit_factor",
        "sharpe_ratio",
        "max_drawdown_pct",
        "total_return_pct",
        "final_equity",
    ]
    headers = [
        "Strategy Name",
        "Hold (Days)",
        "Trades",
        "Win Rate (%)",
        "Profit Factor",
        "Sharpe",
        "Max DD (%)",
        "Total Return (%)",
        "Final Equity ($)",
    ]

    ranking_order = [
        ("COMBINED_90D", "COMBINED (Cluster + Conviction)", 90),
        ("INDUSTRY_MOMENTUM_90D", "INDUSTRY_MOMENTUM", 90),
        ("CONVICTION_90D", "CONVICTION (C-Suite CEO/CFO)", 90),
        ("CLUSTER_BUY_90D", "CLUSTER_BUY (Exec/Director)", 90),
    ]

    rows = []
    for key, label, hold in ranking_order:
        s = sums[key]
        rows.append(
            {
                "strategy_name": label,
                "holding_days": hold,
                "total_trades": s.total_trades,
                "win_rate_pct": s.win_rate_pct,
                "profit_factor": s.profit_factor,
                "sharpe_ratio": s.sharpe_ratio,
                "max_drawdown_pct": s.max_drawdown_pct,
                "total_return_pct": s.total_return_pct,
                "final_equity": s.final_equity,
            }
        )

    df = pd.DataFrame(rows)

    print("\n================================================================================")
    print("        TOP 4 PERFORMING QUANTITATIVE STRATEGIES: EXECUTIVE COMPARISON          ")
    print("================================================================================\n")
    print(
        tabulate(
            df[cols],
            headers=headers,
            tablefmt="simple",
            showindex=False,
            floatfmt=("", "", "", ".2f", ".2f", ".2f", ".2f", ".2f", ",.2f"),
        )
    )
    print("\n================================================================================\n")

    if args.show_trades:
        for rank_num, (key, label, _) in enumerate(ranking_order, 1):
            s = sums[key]
            tdf = s.to_dataframe()
            print(f"--- #{rank_num} STRATEGY: {label} (FIRST 10 TRADES WITH TRIGGER REASONS) ---")
            tcols = [
                "ticker",
                "entry_date",
                "entry_price",
                "exit_date",
                "exit_reason",
                "exit_price",
                "return_pct",
                "pnl_dollar",
                "trigger_reason",
            ]
            print(tabulate(tdf[tcols].head(10), headers="keys", tablefmt="simple", showindex=False))
            print("")

    print(f"Full individual analysis report & trigger links saved to: docs/TOP4_STRATEGIES_INDIVIDUAL_ANALYSIS.md")
    print(f"Individual trade CSV and JSON logs saved to: data/top4_*_trade_log.csv | .json")
    return 0


def cmd_full_backtest(args: argparse.Namespace) -> int:
    """
    Executes and tracks backtest performance across the entire 6-year dataset (2021-2026),
    saves tracker reports, and displays the highest returning strategies.
    """
    from src.strategies.run_full_backtest import FullDatasetBacktester

    print(
        f"Running full dataset backtest & ROI tracking across ALL 6 YEARS (2021-2026) "
        f"(Market Cap >= ${args.min_market_cap/1e9:,.1f}B)..."
    )
    fdb = FullDatasetBacktester(
        initial_capital=args.initial_capital, min_market_cap=args.min_market_cap
    )
    df, results, winners = fdb.run_all_backtests_and_track_roi()

    cols = [
        "strategy",
        "holding_days",
        "total_trades",
        "win_rate_pct",
        "profit_factor",
        "sharpe_ratio",
        "max_drawdown_pct",
        "total_return_pct",
    ]
    headers = [
        "Strategy",
        "Holding (Days)",
        "Trades",
        "Win Rate (%)",
        "Profit Factor",
        "Sharpe",
        "Max DD (%)",
        "Total Return (%)",
    ]

    print("\n================================================================================")
    print("      COMPLETE 6-YEAR DATASET BACKTEST & ROI TRACKER (2021-2026)")
    print("================================================================================\n")
    print(
        tabulate(
            df[cols],
            headers=headers,
            tablefmt="simple",
            showindex=False,
            floatfmt=("", "", "", ".2f", ".2f", ".2f", ".2f", ".2f"),
        )
    )

    print("\n================================================================================")
    print("              *** HIGHEST RETURN STRATEGIES (CATEGORY WINNERS) ***              ")
    print("================================================================================")
    for cat, sum_obj in winners.items():
        print(f"  {cat:<22} : {sum_obj.strategy_name:<18} ({sum_obj.holding_days}d) -> ROI = {sum_obj.total_return_pct:,.2f}% | Sharpe = {sum_obj.sharpe_ratio:.2f} | Win Rate = {sum_obj.win_rate_pct:.2f}% | Final Equity: ${sum_obj.final_equity:,.2f}")
    print("================================================================================\n")

    if args.show_log:
        best = winners["OVERALL_HIGHEST_ROI"]
        tdf = best.to_dataframe()
        tcols = [
            "ticker",
            "industry",
            "entry_date",
            "entry_price",
            "exit_date",
            "exit_reason",
            "exit_price",
            "return_pct",
            "pnl_dollar",
        ]
        print("--- TOP OVERALL STRATEGY TRADE BREAKDOWN (FIRST 15 TRADES) ---")
        print(tabulate(tdf[tcols].head(15), headers="keys", tablefmt="simple", showindex=False))
        print("")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump({k: v.to_dict() for k, v in winners.items()}, f, indent=2)
        print(f"Saved full dataset backtest winners report to {args.output}")

    return 0


def cmd_collect(args: argparse.Namespace) -> int:
    """
    Collects and organizes insider trades for companies with market cap over $1B.
    Supports targeting current year (2026) first, or previous years (2025..2021)
    or all historical years (--all-years).
    """
    io = IndustryOrganizer()
    if args.all_years:
        years = [2026, 2025, 2024, 2023, 2022, 2021]
        print(
            f"Collecting & organizing insider trades across ALL 6 YEARS (2021-2026) "
            f"for companies with Market Cap >= ${args.min_market_cap/1e9:,.1f}B..."
        )
        total_all = 0
        for y in years:
            c = io.collect_and_organize_trades(
                year=y,
                min_market_cap=args.min_market_cap,
                overwrite=args.overwrite,
            )
            total_all += c
            print(f"  -> Year {y}: collected & organized {c} trade records.")
        df_sum = io.update_all_summaries(year=None)
        print(
            f"\nSuccessfully collected & organized {total_all} total trade records across 2021-2026!"
        )
        print(f"Updated {len(df_sum)} industry summary files.")
        return 0

    print(
        f"Collecting & organizing insider trades for Year {args.year} "
        f"(Market Cap >= ${args.min_market_cap/1e9:,.1f}B)..."
    )
    count = io.collect_and_organize_trades(
        year=args.year, min_market_cap=args.min_market_cap, overwrite=args.overwrite
    )
    print(
        f"Successfully collected & organized {count} trade records for Year {args.year} across all industries!"
    )
    df_sum = io.update_all_summaries(year=args.year)
    print(f"Updated {len(df_sum)} industry summary files.")
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    """Updates or seeds the repository's industry-organized trade database."""
    io = IndustryOrganizer()
    target_year = None if args.year == 0 else args.year

    if args.seed or args.all:
        yr_label = str(target_year) if target_year else "2021-2026 (All Years)"
        print(
            f"Updating industry-organized Form 4 datasets for {yr_label} "
            f"(Market Cap >= ${args.min_market_cap/1e9:,.1f}B)..."
        )
        if target_year is None:
            years = [2026, 2025, 2024, 2023, 2022, 2021]
            total_c = 0
            for y in years:
                c = io.collect_and_organize_trades(
                    year=y,
                    min_market_cap=args.min_market_cap,
                    overwrite=args.overwrite,
                )
                total_c += c
            print(f"Successfully generated/updated {total_c} trade records across all industries!")
        else:
            count = io.collect_and_organize_trades(
                year=target_year, min_market_cap=args.min_market_cap, overwrite=args.overwrite
            )
            print(f"Successfully generated/updated {count} trade records across all industries!")
        df_sum = io.update_all_summaries(year=target_year)
        print(f"Updated {len(df_sum)} industry summary files.")
        return 0

    if args.ticker:
        comp = io.um.get_company(args.ticker)
        if not comp:
            print(f"Error: Ticker {args.ticker} not in universe.", file=sys.stderr)
            return 1
        print(f"Updating trades for {comp.ticker} ({comp.company_name})...")
        io.compute_industry_summary(comp.industry, year=target_year)
        print(f"Done updating {comp.ticker}.")
        return 0

    print("Please specify --all, --seed, or --ticker <TICKER>.")
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="insider-trades",
        description="NASDAQ & S&P 500 Insider Trading Tracker ($1B+ Market Cap Focus) & Strategy Backtester",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose debug logging"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # sources subcommand
    p_sources = subparsers.add_parser(
        "sources", help="Show official SEC EDGAR data source & Section 16(a) guide"
    )
    p_sources.set_defaults(func=cmd_sources)

    # universe subcommand
    p_univ = subparsers.add_parser(
        "universe",
        help="Query NASDAQ & S&P 500 universe organized by industry ($1B+ focus)",
    )
    p_univ.add_argument(
        "--ticker", "-t", type=str, help="Filter by specific ticker symbol"
    )
    p_univ.add_argument("--sector", "-s", type=str, help="Filter by GICS Sector")
    p_univ.add_argument(
        "--industry", "-i", type=str, help="Filter by specific Industry"
    )
    p_univ.add_argument(
        "--exchange", "-e", type=str, help="Filter by Exchange (NASDAQ/NYSE)"
    )
    p_univ.add_argument(
        "--min-market-cap",
        "-m",
        type=float,
        default=1_000_000_000.0,
        help="Minimum market cap in USD (default: $1B)",
    )
    p_univ.add_argument(
        "--format",
        "-f",
        choices=["table", "json"],
        default="table",
        help="Output format",
    )
    p_univ.set_defaults(func=cmd_universe)

    # collect subcommand
    p_collect = subparsers.add_parser(
        "collect",
        help="Collect & organize insider trades for $1B+ companies by year (e.g. 2026, 2025..2021, or --all-years)",
    )
    p_collect.add_argument(
        "--year",
        "-y",
        type=int,
        default=2026,
        help="Target year to collect (default: 2026)",
    )
    p_collect.add_argument(
        "--all-years",
        action="store_true",
        help="Collect & organize all historical years (2021 through 2026)",
    )
    p_collect.add_argument(
        "--min-market-cap",
        "-m",
        type=float,
        default=1_000_000_000.0,
        help="Minimum market cap in USD (default: $1B)",
    )
    p_collect.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing trade records for that year",
    )
    p_collect.set_defaults(func=cmd_collect)

    # parse-xml subcommand
    p_parse = subparsers.add_parser(
        "parse-xml", help="Parse an SEC Form 4 XML document"
    )
    p_parse.add_argument(
        "--file", "-f", required=True, type=str, help="Path to Form 4 XML file"
    )
    p_parse.set_defaults(func=cmd_parse_xml)

    # heatmap subcommand
    p_heat = subparsers.add_parser(
        "heatmap", help="Display industry-wide insider sentiment heatmap"
    )
    p_heat.add_argument(
        "--days", "-d", type=int, default=90, help="Trailing calendar days (default 90)"
    )
    p_heat.add_argument("--sector", "-s", type=str, help="Filter by GICS Sector")
    p_heat.add_argument(
        "--format", "-f", choices=["table", "markdown", "json"], default="table"
    )
    p_heat.set_defaults(func=cmd_heatmap)

    # signals subcommand
    p_sig = subparsers.add_parser(
        "signals", help="Scan trade logs for bullish entry and bearish exit signals"
    )
    p_sig.add_argument("--ticker", "-t", type=str, help="Filter by ticker")
    p_sig.add_argument("--industry", "-i", type=str, help="Filter by industry")
    p_sig.add_argument(
        "--year",
        "-y",
        type=int,
        default=0,
        help="Target year (default: 0 = All Years 2021-2026)",
    )
    p_sig.add_argument(
        "--min-market-cap",
        "-m",
        type=float,
        default=1_000_000_000.0,
        help="Minimum market cap in USD (default: $1B)",
    )
    p_sig.add_argument(
        "--min-confidence",
        "-c",
        type=int,
        default=70,
        help="Minimum confidence score (0-100)",
    )
    p_sig.add_argument(
        "--format",
        "-f",
        choices=["table", "json"],
        default="table",
        help="Output format",
    )
    p_sig.set_defaults(func=cmd_signals)

    # backtest subcommand
    p_bt = subparsers.add_parser(
        "backtest", help="Run quantitative backtest of entry/exit strategies"
    )
    p_bt.add_argument(
        "--strategy",
        "-s",
        choices=[
            "cluster_buy",
            "conviction",
            "csuite_cluster",
            "industry_momentum",
            "combined",
        ],
        default="cluster_buy",
        help="Strategy to backtest",
    )
    p_bt.add_argument("--ticker", "-t", type=str, help="Backtest a specific ticker")
    p_bt.add_argument("--industry", "-i", type=str, help="Backtest a specific industry")
    p_bt.add_argument("--sector", type=str, help="Backtest a specific GICS sector")
    p_bt.add_argument(
        "--year",
        "-y",
        type=int,
        default=0,
        help="Target year (default: 0 = All Years 2021-2026)",
    )
    p_bt.add_argument(
        "--holding-days", type=int, default=60, help="Target holding period in days"
    )
    p_bt.add_argument(
        "--stop-loss", type=float, default=10.0, help="Stop-loss percentage"
    )
    p_bt.add_argument(
        "--take-profit", type=float, default=25.0, help="Take-profit percentage"
    )
    p_bt.add_argument(
        "--initial-capital",
        type=float,
        default=100000.0,
        help="Initial portfolio capital ($)",
    )
    p_bt.add_argument(
        "--min-market-cap",
        "-m",
        type=float,
        default=1_000_000_000.0,
        help="Minimum market cap in USD (default: $1B)",
    )
    p_bt.add_argument(
        "--show-log", action="store_true", help="Print complete individual trade log"
    )
    p_bt.add_argument(
        "--output", "-o", type=str, help="Save JSON backtest report to file"
    )
    p_bt.set_defaults(func=cmd_backtest)

    # sweep subcommand
    p_sweep = subparsers.add_parser(
        "sweep",
        help="Run multi-strategy parameter sweep & identify highest ROI configuration",
    )
    p_sweep.add_argument(
        "--year",
        "-y",
        type=int,
        default=0,
        help="Target year (default: 0 = All Years 2021-2026)",
    )
    p_sweep.add_argument(
        "--min-market-cap",
        "-m",
        type=float,
        default=1_000_000_000.0,
        help="Minimum market cap in USD (default: $1B)",
    )
    p_sweep.add_argument(
        "--initial-capital",
        type=float,
        default=100000.0,
        help="Initial portfolio capital ($)",
    )
    p_sweep.add_argument(
        "--show-log",
        action="store_true",
        help="Print top strategy trade breakdown log",
    )
    p_sweep.add_argument(
        "--output", "-o", type=str, help="Save JSON report for top strategy to file"
    )
    p_sweep.set_defaults(func=cmd_sweep)

    # full-backtest subcommand
    p_full = subparsers.add_parser(
        "full-backtest",
        help="Execute & track backtests across the entire 6-year dataset (2021-2026)",
    )
    p_full.add_argument(
        "--min-market-cap",
        "-m",
        type=float,
        default=1_000_000_000.0,
        help="Minimum market cap in USD (default: $1B)",
    )
    p_full.add_argument(
        "--initial-capital",
        type=float,
        default=100000.0,
        help="Initial portfolio capital ($)",
    )
    p_full.add_argument(
        "--show-log",
        action="store_true",
        help="Print top strategy trade breakdown log",
    )
    p_full.add_argument(
        "--output", "-o", type=str, help="Save JSON report for category winners to file"
    )
    p_full.set_defaults(func=cmd_full_backtest)

    # analyze-top4 subcommand (new!)
    p_top4 = subparsers.add_parser(
        "analyze-top4",
        help="Individual deep-dive analysis of Top 4 performing strategies with trade tables & trigger links",
    )
    p_top4.add_argument(
        "--min-market-cap",
        "-m",
        type=float,
        default=1_000_000_000.0,
        help="Minimum market cap in USD (default: $1B)",
    )
    p_top4.add_argument(
        "--initial-capital",
        type=float,
        default=100000.0,
        help="Initial portfolio capital ($)",
    )
    p_top4.add_argument(
        "--show-trades",
        action="store_true",
        help="Print individual trade tables with trigger explanations",
    )
    p_top4.set_defaults(func=cmd_analyze_top4)

    # update subcommand
    p_up = subparsers.add_parser(
        "update", help="Update industry-organized trade database"
    )
    p_up.add_argument(
        "--all", action="store_true", help="Update all companies in universe"
    )
    p_up.add_argument("--seed", action="store_true", help="Seed historical dataset")
    p_up.add_argument(
        "--year",
        "-y",
        type=int,
        default=0,
        help="Target year (default: 0 = All Years 2021-2026)",
    )
    p_up.add_argument(
        "--min-market-cap",
        "-m",
        type=float,
        default=1_000_000_000.0,
        help="Minimum market cap in USD (default: $1B)",
    )
    p_up.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing trade logs"
    )
    p_up.add_argument("--ticker", "-t", type=str, help="Update specific ticker")
    p_up.set_defaults(func=cmd_update)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    setup_logging(args.verbose)

    if not hasattr(args, "func"):
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
