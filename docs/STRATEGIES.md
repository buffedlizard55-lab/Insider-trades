# Research strategies (methodology only)

This document describes **research rules** implemented in `src/strategies/`.
It does **not** claim live, audited, or historically official investment
returns. Any backtest output is a simulation that uses:

1. Official SEC Form 4 rows you have collected (`python main.py collect`)
2. Local prices (Yahoo when fetched; otherwise an interpolated fallback)

Past simulations do not predict future results. This is not investment advice.

---

## Signals

The generator looks only at Form 4 **transaction codes** defined in the
[official Form 4 instructions](https://www.sec.gov/files/form4.pdf):

| Research signal | Rule of thumb | Form 4 inputs |
| :--- | :--- | :--- |
| `CLUSTER_BUY` | ≥2 distinct insiders with code `P` inside 14 calendar days | `P` rows |
| `CONVICTION_BUY` | CEO/CFO title and code `P` with notional ≥ $100,000 | `P` rows + `officerTitle` |
| `HEAVY_SELL_EXIT` | Multiple code `S` rows totaling ≥ $1,000,000 in 14 days | `S` rows |
| `INDUSTRY_BULLISH` | Industry net `P` dollars / `S` dollars ≥ 1.5 | aggregated `P`/`S` |

Those dollar and window cutoffs are **research parameters**, not SEC rules.

---

## Backtester

`BacktestEngine` turns those signals into hypothetical trades with a holding
period, stop-loss, and take-profit. Reported KPIs (total return, win rate,
Sharpe-style ratio, max drawdown) describe **that simulation only**.

Run after collecting official filings:

```bash
python main.py backtest --strategy conviction --holding-days 45
python main.py heatmap --days 90
```

If no official Form 4 rows are on disk, the report will show zero trades.
That is expected — this repo no longer ships invented insider activity.
