"""
GitHub Pages Dashboard Builder for the Top 3 Insider-Trading Strategies.

Reads the repository's source-of-truth artifacts (backtest KPI tracker,
per-strategy trade logs, and active entry/exit predictions) and emits a
compact set of JSON files under `site/data/` that the static GitHub Pages
dashboard (`site/index.html`) renders:

  site/data/meta.json          -> build timestamp, data source files, counts
  site/data/strategies.json    -> Top-3 strategy overview + KPIs (no tables)
  site/data/<strategy>.json    -> full trade history + active/upcoming trades

The dashboard itself is pure HTML/CSS/JS with no runtime dependencies, so it
can be served directly from GitHub Pages or any static file server.

Usage:
    python main.py build-site                 # default: writes site/data/
    python main.py build-site --out /tmp/site
"""

import os
import json
from datetime import datetime, timezone
from typing import Dict, List, Any

import pandas as pd

# --------------------------------------------------------------------------
# Strategy configuration: the Top 3 ROI strategies (90-day holding period)
# identified by the full-dataset backtest sweep (2021-2026).
# --------------------------------------------------------------------------
STRATEGIES = [
    {
        "key": "combined",
        "name": "COMBINED",
        "rank": 1,
        "csv_name": "top4_COMBINED_90D_trade_log",
        "tagline": "Every high-conviction insider signal in one strategy",
        "description": (
            "Enters a trade whenever insiders show strong conviction: a C-Suite "
            "(CEO/CFO) open-market buy over $100K, 2+ insiders buying within 14 days, "
            "or heavy open-market selling that historically marks good entry points. "
            "Captures the broadest set of signals, which is why it delivered the "
            "highest ROI of all strategies tested."
        ),
    },
    {
        "key": "industry_momentum",
        "name": "INDUSTRY_MOMENTUM",
        "rank": 2,
        "csv_name": "top4_INDUSTRY_MOMENTUM_90D_trade_log",
        "tagline": "High-confidence signals in accumulation industries",
        "description": (
            "Trades only the highest-confidence insider signals (75%+ confidence) "
            "that appear while their industry is in an accumulation phase. Fewer, "
            "better-timed trades with the strongest win rate of the top three."
        ),
    },
    {
        "key": "conviction",
        "name": "CONVICTION",
        "rank": 3,
        "csv_name": "top4_CONVICTION_90D_trade_log",
        "tagline": "C-Suite conviction buys only (CEO / CFO)",
        "description": (
            "The purest signal: only open-market purchases of $100,000+ made by a "
            "Chief Executive Officer or Chief Financial Officer with their own money. "
            "A smaller, cleaner book of trades built on the most trusted insider signal."
        ),
    },
]

# Predictions CSV -> strategy mapping rules. The predictor tags each row with the
# raw signal type that triggered it; each strategy inherits the entry targets that
# match how its backtest selects signals.
ACTIVE_RULES = {
    "combined": lambda d: d["action"] == "BUY_ENTRY_TARGET"
    and d["strategy_source"] in ("CONVICTION_BUY", "CLUSTER_BUY"),
    "industry_momentum": lambda d: d["action"] == "BUY_ENTRY_TARGET"
    and d["confidence_score"] >= 75,
    "conviction": lambda d: d["action"] == "BUY_ENTRY_TARGET"
    and d["strategy_source"] == "CONVICTION_BUY",
}

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _read_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def _iso_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _kpis_from_tracker(tracker: pd.DataFrame, strategy: str) -> Dict[str, Any]:
    """Pulls the KPI row for a strategy's 90-day configuration, if present."""
    if tracker.empty or "strategy" not in tracker.columns:
        return {
            "holding_days": 90,
            "total_trades": 0,
            "win_rate_pct": 0.0,
            "profit_factor": 0.0,
            "sharpe_ratio": 0.0,
            "max_drawdown_pct": 0.0,
            "total_return_pct": 0.0,
            "final_equity": 100000.0,
            "initial_capital": 100000.0,
            "stop_loss_pct": 12.0,
            "take_profit_pct": 40.0,
        }
    row = tracker[
        (tracker["strategy"].str.upper() == strategy)
        & (tracker["holding_days"] == 90)
    ]
    if row.empty:
        return {
            "holding_days": 90,
            "total_trades": 0,
            "win_rate_pct": 0.0,
            "profit_factor": 0.0,
            "sharpe_ratio": 0.0,
            "max_drawdown_pct": 0.0,
            "total_return_pct": 0.0,
            "final_equity": 100000.0,
            "initial_capital": 100000.0,
            "stop_loss_pct": 12.0,
            "take_profit_pct": 40.0,
        }
    r = row.iloc[0]
    return {
        "holding_days": int(r["holding_days"]),
        "total_trades": int(r["total_trades"]),
        "win_rate_pct": round(float(r["win_rate_pct"]), 2),
        "profit_factor": round(float(r["profit_factor"]), 2),
        "sharpe_ratio": float(r["sharpe_ratio"]),
        "max_drawdown_pct": round(float(r["max_drawdown_pct"]), 2),
        "total_return_pct": round(float(r["total_return_pct"]), 2),
        "final_equity": round(float(r["final_equity"]), 2),
        "initial_capital": 100000.0,
        "stop_loss_pct": float(r["stop_loss_pct"]),
        "take_profit_pct": float(r["take_profit_pct"]),
    }


def _trade_rows(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Normalizes a full trade log into compact JSON rows (newest first)."""
    rows = []
    for _, r in df.iterrows():
        rows.append(
            {
                "ticker": str(r["ticker"]),
                "company": str(r["company_name"]),
                "sector": str(r["sector"]),
                "industry": str(r["industry"]),
                "entry_date": str(r["entry_date"]),
                "entry_signal": str(r["entry_signal"]),
                "entry_price": round(float(r["entry_price"]), 2),
                "exit_date": str(r["exit_date"]),
                "exit_reason": str(r["exit_reason"]),
                "exit_price": round(float(r["exit_price"]), 2),
                "holding_days": int(r["holding_days"]),
                "return_pct": round(float(r["return_pct"]), 2),
                "pnl_dollar": round(float(r["pnl_dollar"]), 2),
                "confidence": int(r["confidence_score"]),
                "reason": str(r["trigger_reason"]),
                "url": str(r["trigger_url"]),
            }
        )
    rows.sort(key=lambda t: (t["entry_date"], t["ticker"]), reverse=True)
    return rows


def _active_rows(df: pd.DataFrame, rule) -> List[Dict[str, Any]]:
    """Normalizes active entry targets for a strategy (newest trigger first)."""
    rows = []
    for _, r in df.iterrows():
        d = r.to_dict()
        if not rule(d):
            continue
        rows.append(
            {
                "ticker": str(d["ticker"]),
                "company": str(d["company_name"]),
                "sector": str(d["sector"]),
                "industry": str(d["industry"]),
                "trigger_date": str(d["trigger_date"]),
                "entry_price": round(float(d["recommended_entry_price"]), 2),
                "take_profit": round(float(d["target_take_profit_price"]), 2),
                "stop_loss": round(float(d["target_stop_loss_price"]), 2),
                "holding_days": int(d["recommended_holding_days"]),
                "confidence": int(d["confidence_score"]),
                "expected_alpha": round(float(d["expected_alpha_pct"]), 2),
                "reason": str(d["trigger_reason"]),
                "accession": str(d["trigger_accession"]),
                "url": str(d["trigger_url"]),
            }
        )
    rows.sort(key=lambda t: (t["trigger_date"], t["ticker"]), reverse=True)
    return rows


def _entry_mix(trades: List[Dict[str, Any]]) -> Dict[str, int]:
    mix: Dict[str, int] = {}
    for t in trades:
        mix[t["entry_signal"]] = mix.get(t["entry_signal"], 0) + 1
    return mix


def build_site_data(
    data_dir: str = None, out_dir: str = None, mirror_root: bool = False
) -> Dict[str, Any]:
    """
    Builds the dashboard JSON payloads and writes them to out_dir.

    If mirror_root is True, also copies the dashboard's static files
    (index.html, styles.css, js/, data JSONs) to the repository root so the
    currently-enabled GitHub Pages setup (which serves the repo root of main)
    publishes the dashboard without needing admin Pages settings.

    Returns a summary dict of what was written (also used by tests).
    """
    data_dir = data_dir or os.path.join(ROOT_DIR, "data")
    out_dir = out_dir or os.path.join(ROOT_DIR, "site", "data")
    os.makedirs(out_dir, exist_ok=True)

    tracker = _read_csv(os.path.join(data_dir, "full_dataset_backtest_tracker.csv"))
    predictions = _read_csv(os.path.join(data_dir, "active_entry_exit_predictions.csv"))
    if predictions.empty:
        predictions = pd.DataFrame(
            columns=[
                "action", "strategy_source", "confidence_score", "ticker",
                "company_name", "sector", "industry", "trigger_date",
                "recommended_entry_price", "target_take_profit_price",
                "target_stop_loss_price", "recommended_holding_days",
                "expected_alpha_pct", "trigger_reason", "trigger_accession",
                "trigger_url",
            ]
        )

    overview: List[Dict[str, Any]] = []
    source_files: List[str] = []
    summary = {"generated_at": _iso_now(), "strategies": {}}

    for cfg in STRATEGIES:
        key = cfg["key"]
        trades_df = _read_csv(os.path.join(data_dir, f"{cfg['csv_name']}.csv"))
        trades = _trade_rows(trades_df) if not trades_df.empty else []
        active = _active_rows(predictions, ACTIVE_RULES[key])
        kpis = _kpis_from_tracker(tracker, cfg["name"])
        kpis["winning_trades"] = sum(1 for t in trades if t["pnl_dollar"] > 0)
        kpis["losing_trades"] = sum(1 for t in trades if t["pnl_dollar"] < 0)

        payload = {
            "key": key,
            "name": cfg["name"],
            "rank": cfg["rank"],
            "tagline": cfg["tagline"],
            "description": cfg["description"],
            "csv_name": cfg["csv_name"],
            "csv_url": f"data/{cfg['csv_name']}_trade_log.csv",
            "kpis": kpis,
            "entry_mix": _entry_mix(trades),
            "active": active,
            "trades": trades,
        }
        with open(os.path.join(out_dir, f"{key}.json"), "w", encoding="utf-8") as f:
            json.dump(payload, f, separators=(",", ":"))

        overview.append(
            {
                "key": key,
                "name": cfg["name"],
                "rank": cfg["rank"],
                "tagline": cfg["tagline"],
                "description": cfg["description"],
                "kpis": kpis,
                "active_count": len(active),
                "trade_count": len(trades),
            }
        )
        source_files.extend(
            [
                f"data/{cfg['csv_name']}.csv",
                f"data/{cfg['csv_name']}.json",
            ]
        )
        summary["strategies"][key] = {
            "trades": len(trades),
            "active": len(active),
        }

    meta = {
        "generated_at": _iso_now(),
        "site_title": "Insider Trades — Top 3 Strategy Dashboard",
        "universe_note": (
            "Insider transactions come only from official SEC EDGAR Form 4 filings "
            "after `python main.py collect`. This repository ships a curated 89-name "
            "large-cap sample (not the complete S&P 500 or Nasdaq). Backtests are "
            "research simulations on collected filings, not audited live performance."
        ),
        "source_files": sorted(set(source_files)),
        "strategy_count": len(overview),
    }
    with open(os.path.join(out_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, separators=(",", ":"))
    with open(os.path.join(out_dir, "strategies.json"), "w", encoding="utf-8") as f:
        json.dump(overview, f, separators=(",", ":"))

    summary["meta"] = meta
    summary["output_dir"] = out_dir

    # Mirror the dashboard to the repository root for root-based Pages serving
    if mirror_root:
        site_dir = os.path.join(ROOT_DIR, "site")
        mirrored: List[str] = []
        for rel in ("index.html", "styles.css", "js/app.js"):
            _copy_if_changed(os.path.join(site_dir, rel), os.path.join(ROOT_DIR, rel), mirrored)
        for name in ("meta.json", "strategies.json", "combined.json", "industry_momentum.json", "conviction.json"):
            _copy_if_changed(
                os.path.join(out_dir, name),
                os.path.join(ROOT_DIR, "data", name),
                mirrored,
            )
        summary["mirrored_to_root"] = mirrored

    return summary


def _copy_if_changed(src: str, dst: str, copied: List[str]) -> None:
    """Copies src -> dst only when content differs (keeps git history clean)."""
    if not os.path.exists(src):
        return
    try:
        with open(src, "rb") as f:
            new_bytes = f.read()
        if os.path.exists(dst):
            with open(dst, "rb") as f:
                if f.read() == new_bytes:
                    return
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as f:
            f.write(new_bytes)
        copied.append(os.path.relpath(dst, ROOT_DIR))
    except OSError:
        return


if __name__ == "__main__":
    import sys

    out = sys.argv[1] if len(sys.argv) > 1 else None
    res = build_site_data(out_dir=out)
    print(f"Dashboard data written to: {res['output_dir']}")
    for key, counts in res["strategies"].items():
        print(
            f"  {key:<18} trades={counts['trades']:>5}  active_entries={counts['active']:>3}"
        )
