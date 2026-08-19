# Stored daily prices — not official exchange prints

Files in this folder are a **local cache** used by the backtester.

1. When the network is available, `python main.py prices --seed` tries Yahoo Finance
   chart history (`query1.finance.yahoo.com`).
2. If that fetch fails, the seeder writes a **deterministic interpolated fallback**
   (yearly anchors + hash noise). Those fallback rows are **not** NYSE/Nasdaq official
   last-sale prints and must not be cited as such.

SEC EDGAR does not publish daily equity prices. Official last-sale data comes from
the listing exchange.
