/* ==========================================================================
   Insider Trades — Top 3 Strategy Dashboard
   Renders the overview, per-strategy KPI cards, the active/upcoming trades
   table, and the full trade-history table for each of the top 3 strategies.
   Pure vanilla JS — no frameworks, no external CDNs.
   ========================================================================== */

"use strict";

const REPO = "buffedlizard55-lab/Insider-trades";
const REFRESH_URL = `https://github.com/${REPO}/actions/workflows/daily_insider_update.yml`;
const HISTORY_CSV_URL = (csvName) => `https://github.com/${REPO}/blob/main/data/${csvName}_trade_log.csv`;

const SIGNAL_LABELS = {
  CONVICTION_BUY: "C-Suite buy",
  CLUSTER_BUY: "Cluster buy",
  HEAVY_SELL_EXIT: "Heavy selling",
};

const SIGNAL_SHORT = {
  CONVICTION_BUY: "Conviction",
  CLUSTER_BUY: "Cluster",
  HEAVY_SELL_EXIT: "Sell-cluster",
};

const EXIT_LABELS = {
  HOLDING_PERIOD_EXIT: "90-day hold",
  STOP_LOSS_EXIT: "Stop-loss",
  TAKE_PROFIT_TARGET: "Take-profit",
};

const RANK_BADGE = { 1: "r1", 2: "r2", 3: "r3" };
const RANK_TEXT = { 1: "#1 · Highest ROI", 2: "#2", 3: "#3" };
const RANK_CARD = { 1: "rank-1", 2: "rank-2", 3: "rank-3" };

const state = {
  meta: null,
  strategies: [],
  data: {}, // key -> {kpis, active, trades, ...}
  generatedAt: null,
  // table view state
  activeFilter: {}, // key -> "all" | "30" | "14"
  history: {},      // key -> {search, year, sortKey, sortDir, page}
};

/* ------------------------------------------------------------------ *
 *  Helpers
 * ------------------------------------------------------------------ */

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text !== undefined && text !== null) node.textContent = text;
  return node;
}

function fmtMoney(v, decimals = 2) {
  if (v === null || v === undefined || isNaN(v)) return "—";
  const sign = v < 0 ? "−" : "";
  return sign + "$" + Math.abs(v).toLocaleString("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

function fmtMoneyCompact(v) {
  if (v === null || v === undefined || isNaN(v)) return "—";
  const abs = Math.abs(v);
  const sign = v < 0 ? "−" : "";
  if (abs >= 1e6) return sign + "$" + (abs / 1e6).toFixed(2) + "M";
  if (abs >= 1e3) return sign + "$" + (abs / 1e3).toFixed(1) + "k";
  return sign + "$" + abs.toFixed(0);
}

function fmtPct(v, signed = true) {
  if (v === null || v === undefined || isNaN(v)) return "—";
  const sign = signed && v > 0 ? "+" : v < 0 ? "−" : "";
  return sign + v.toLocaleString("en-US", { maximumFractionDigits: 2 }) + "%";
}

function pctClass(v) {
  if (v > 0) return "pos";
  if (v < 0) return "neg";
  return "";
}

function escapeHtml(s) {
  const div = document.createElement("div");
  div.textContent = s == null ? "" : String(s);
  return div.innerHTML;
}

function daysAgo(dateStr, fromStr) {
  const a = new Date(dateStr + "T00:00:00Z");
  const b = new Date((fromStr || new Date().toISOString()).slice(0, 10) + "T00:00:00Z");
  return Math.round((b - a) / 86400000);
}

function statusFor(dateStr) {
  const days = daysAgo(dateStr, state.generatedAt);
  if (days <= 14) return { label: "New", cls: "badge-new", hint: `Triggered ${days} day${days === 1 ? "" : "s"} ago` };
  if (days <= 30) return { label: "Recent", cls: "badge-recent", hint: `Triggered ${days} days ago` };
  return { label: "Active", cls: "badge-active", hint: `Triggered ${days} days ago` };
}

function signalBadge(signal) {
  const isSell = signal === "HEAVY_SELL_EXIT";
  return `<span class="badge ${isSell ? "badge-sell" : "badge-buy"}">${escapeHtml(SIGNAL_SHORT[signal] || signal)}</span>`;
}

function exitBadge(reason) {
  return `<span class="badge badge-active">${escapeHtml(EXIT_LABELS[reason] || reason)}</span>`;
}

/* ------------------------------------------------------------------ *
 *  Generic sortable / filterable / paginated table
 * ------------------------------------------------------------------ */

/**
 * columns: [{ key, label, render(row), sortValue(row) (optional), num (bool) }]
 * rows: array
 * opts: { pageSize (0 = no pagination), defaultSort: {key, dir} }
 */
function createTable(columns, rows, opts = {}) {
  const pageSize = opts.pageSize || 0;
  const block = el("div", "table-block");
  const sort = { key: opts.defaultSort?.key || columns[0].key, dir: opts.defaultSort?.dir || "desc" };

  const tableWrap = el("div", "table-wrap");
  const table = el("table", "data-table");
  const thead = el("thead");
  const tbody = el("tbody");

  const headerRow = el("tr");
  columns.forEach((col) => {
    const th = el("th", col.num ? "num" : "");
    th.innerHTML = `<span>${escapeHtml(col.label)}</span><span class="arrow">▾</span>`;
    th.addEventListener("click", () => {
      if (sort.key === col.key) {
        sort.dir = sort.dir === "asc" ? "desc" : "asc";
      } else {
        sort.key = col.key;
        sort.dir = "desc";
      }
      render();
    });
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);
  table.appendChild(tbody);
  tableWrap.appendChild(table);
  block.appendChild(tableWrap);

  const pagination = el("div", "pagination");
  block.appendChild(pagination);

  let page = 0;
  let filtered = rows;

  function applySort(list) {
    const col = columns.find((c) => c.key === sort.key);
    const sv = (row) => (col.sortValue ? col.sortValue(row) : row[col.key]);
    const dir = sort.dir === "asc" ? 1 : -1;
    return [...list].sort((a, b) => {
      const va = sv(a), vb = sv(b);
      if (va === vb) return 0;
      if (va === null || va === undefined || va === "") return 1;
      if (vb === null || vb === undefined || vb === "") return -1;
      return va < vb ? -dir : dir;
    });
  }

  function render() {
    // update header arrows
    Array.from(headerRow.children).forEach((th, i) => {
      const active = columns[i].key === sort.key;
      th.classList.toggle("sorted-asc", active && sort.dir === "asc");
      th.classList.toggle("sorted-desc", active && sort.dir === "desc");
    });

    const sorted = applySort(filtered);
    const total = sorted.length;
    const maxPage = pageSize > 0 ? Math.max(0, Math.ceil(total / pageSize) - 1) : 0;
    if (page > maxPage) page = maxPage;
    const start = pageSize > 0 ? page * pageSize : 0;
    const end = pageSize > 0 ? start + pageSize : total;
    const visible = sorted.slice(start, end);

    tbody.innerHTML = "";
    if (visible.length === 0) {
      const tr = el("tr");
      const td = el("td", "empty-state");
      td.colSpan = columns.length;
      td.innerHTML = `<span class="big">🔍</span>No trades match this view. Try clearing the search or choosing a different filter.`;
      tr.appendChild(td);
      tbody.appendChild(tr);
    } else {
      visible.forEach((row) => {
        const tr = el("tr");
        columns.forEach((col) => {
          const td = el("td", col.num ? "num" : "");
          td.innerHTML = col.render ? col.render(row) : escapeHtml(row[col.key]);
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });
    }

    // pagination
    pagination.innerHTML = "";
    if (pageSize > 0 && total > pageSize) {
      const mkBtn = (label, p, disabled, current) => {
        const b = el("button", "page-btn" + (current ? " current" : ""), label);
        if (disabled) b.disabled = true;
        else b.addEventListener("click", () => { page = p; render(); });
        return b;
      };
      pagination.appendChild(mkBtn("‹ Prev", page - 1, page === 0));
      const startPage = Math.max(0, page - 2);
      const endPage = Math.min(maxPage, startPage + 4);
      for (let p = startPage; p <= endPage; p++) pagination.appendChild(mkBtn(String(p + 1), p, false, p === page));
      pagination.appendChild(mkBtn("Next ›", page + 1, page === maxPage));
      pagination.appendChild(el("span", "table-count", `${start + 1}–${end} of ${total}`));
    }
  }

  block.setFilter = (fn) => {
    filtered = rows.filter(fn);
    page = 0;
    render();
  };

  block.setSort = (key, dir) => {
    sort.key = key;
    sort.dir = dir;
    page = 0;
    render();
  };

  block.getSorted = () => applySort(filtered);
  block.render = render;
  render();
  return block;
}

/* ------------------------------------------------------------------ *
 *  Active / upcoming trades table
 * ------------------------------------------------------------------ */

function buildActiveTable(strategy, rows) {
  const container = el("div");
  container.appendChild(el("div", "table-sub",
    "What this strategy wants to buy right now — newest signals first. " +
    "“New” = triggered in the last 14 days, “Recent” = last 30 days."));

  const toolbar = el("div", "toolbar");
  const search = el("input", "search-input");
  search.type = "search";
  search.placeholder = "Filter by ticker or company… e.g. NVDA";
  toolbar.appendChild(search);

  const chipsWrap = el("div", "filter-chips");
  const chipDefs = [
    { id: "all", label: "All signals" },
    { id: "30", label: "Last 30 days" },
    { id: "14", label: "New (14 days)" },
  ];
  const chips = {};
  chipDefs.forEach((def) => {
    const b = el("button", "chip-btn" + (def.id === "all" ? " active" : ""), def.label);
    b.addEventListener("click", () => {
      state.activeFilter[strategy.key] = def.id;
      chipDefs.forEach((d) => chips[d.id].classList.toggle("active", d.id === def.id));
      table.setFilter((row) => matchesActiveFilter(row, search.value, def.id));
    });
    chips[def.id] = b;
    chipsWrap.appendChild(b);
  });
  toolbar.appendChild(chipsWrap);
  container.appendChild(toolbar);

  const columns = [
    {
      key: "ticker",
      label: "Stock",
      render: (r) => `<div class="ticker-cell">
          <span class="ticker">${escapeHtml(r.ticker)}</span>
          <span class="company">${escapeHtml(r.company)}</span>
          <span class="industry">${escapeHtml(r.industry)}</span>
        </div>`,
      sortValue: (r) => r.ticker,
    },
    {
      key: "trigger_date",
      label: "Triggered",
      render: (r) => {
        const st = statusFor(r.trigger_date);
        return `<span class="badge ${st.cls}" title="${escapeHtml(st.hint)}">${st.label}</span>
                <div class="table-sub" style="margin-top:2px">${escapeHtml(r.trigger_date)}</div>`;
      },
      sortValue: (r) => r.trigger_date,
    },
    { key: "entry_price", label: "Entry", num: true, render: (r) => fmtMoney(r.entry_price), sortValue: (r) => r.entry_price },
    { key: "take_profit", label: "Take-profit", num: true, render: (r) => `<span class="pos">${fmtMoney(r.take_profit)}</span>`, sortValue: (r) => r.take_profit },
    { key: "stop_loss", label: "Stop-loss", num: true, render: (r) => `<span class="neg">${fmtMoney(r.stop_loss)}</span>`, sortValue: (r) => r.stop_loss },
    {
      key: "holding_days",
      label: "Hold",
      num: true,
      render: (r) => `${r.holding_days}d`,
      sortValue: (r) => r.holding_days,
    },
    {
      key: "confidence",
      label: "Conf.",
      num: true,
      render: (r) => `<b>${r.confidence}%</b>`,
      sortValue: (r) => r.confidence,
    },
    {
      key: "expected_alpha",
      label: "Exp. alpha",
      num: true,
      render: (r) => `<span class="pos strong">${fmtPct(r.expected_alpha)}</span>`,
      sortValue: (r) => r.expected_alpha,
    },
    {
      key: "reason",
      label: "Why the strategy wants this trade",
      render: (r) => `<span class="reason-cell" title="${escapeHtml(r.reason)}">${escapeHtml(r.reason)}</span>`,
      sortValue: (r) => r.reason,
    },
    {
      key: "url",
      label: "SEC filing",
      render: (r) => `<a class="sec-link" href="${escapeHtml(r.url)}" target="_blank" rel="noopener" title="${escapeHtml(r.accession)}">View ↗</a>`,
      sortValue: () => "",
    },
  ];

  const table = createTable(columns, rows, { defaultSort: { key: "trigger_date", dir: "desc" } });
  container.appendChild(table);

  function matchesActiveFilter(row, q, chip) {
    const text = (row.ticker + " " + row.company + " " + row.industry).toLowerCase();
    if (q && !text.includes(q.toLowerCase())) return false;
    const days = daysAgo(row.trigger_date, state.generatedAt);
    if (chip === "14" && days > 14) return false;
    if (chip === "30" && days > 30) return false;
    return true;
  }

  search.addEventListener("input", () => {
    const chip = state.activeFilter[strategy.key] || "all";
    table.setFilter((row) => matchesActiveFilter(row, search.value, chip));
  });

  return container;
}

/* ------------------------------------------------------------------ *
 *  History table (trades that drove the ROI)
 * ------------------------------------------------------------------ */

function buildHistoryTable(strategy, rows, kpis) {
  const container = el("div");
  container.id = strategy.key + "-history";
  container.classList.add("scroll-anchor");

  const header = el("div", "table-title-row");
  const title = el("div", "table-title");
  title.innerHTML = `<span class="flag" aria-hidden="true">📈</span> Trades that drove the ROI`;
  header.appendChild(title);

  const dl = el("a", "btn btn-ghost btn-sm", "⬇ Download full CSV");
  dl.href = HISTORY_CSV_URL(strategy.csv_name);
  dl.target = "_blank";
  dl.rel = "noopener";
  dl.title = "Open the full trade log in the repository";
  header.appendChild(dl);
  container.appendChild(header);

  container.appendChild(el("div", "table-sub",
    `All ${rows.length.toLocaleString()} backtested trades (2021–2026) behind the +${kpis.total_return_pct.toFixed(2)}% ROI — ` +
    `simulated at ${kpis.holding_days}-day holding with ${kpis.stop_loss_pct}% stop-loss / ${kpis.take_profit_pct}% take-profit.`));

  const toolbar = el("div", "toolbar");
  const search = el("input", "search-input");
  search.type = "search";
  search.placeholder = "Filter by ticker, company or trigger reason…";
  toolbar.appendChild(search);

  const yearChipsWrap = el("div", "filter-chips");
  const years = ["All", "2026", "2025", "2024", "2023", "2022", "2021"];
  const yearChips = {};
  years.forEach((y, i) => {
    const b = el("button", "chip-btn" + (i === 0 ? " active" : ""), y === "All" ? "All years" : y);
    b.addEventListener("click", () => {
      years.forEach((yy) => yearChips[yy].classList.toggle("active", yy === y));
      table.setFilter((row) => matchesHistoryFilter(row, search.value, y));
    });
    yearChips[y] = b;
    yearChipsWrap.appendChild(b);
  });
  toolbar.appendChild(yearChipsWrap);
  container.appendChild(toolbar);

  const columns = [
    {
      key: "ticker",
      label: "Stock",
      render: (r) => `<div class="ticker-cell">
          <span class="ticker">${escapeHtml(r.ticker)}</span>
          <span class="company">${escapeHtml(r.company)}</span>
        </div>`,
      sortValue: (r) => r.ticker,
    },
    {
      key: "entry_date",
      label: "Entered",
      render: (r) => `${escapeHtml(r.entry_date)}<div class="table-sub">${signalBadge(r.entry_signal)}</div>`,
      sortValue: (r) => r.entry_date,
    },
    { key: "entry_price", label: "Entry $", num: true, render: (r) => fmtMoney(r.entry_price), sortValue: (r) => r.entry_price },
    {
      key: "exit_date",
      label: "Exited",
      render: (r) => `${escapeHtml(r.exit_date)}<div class="table-sub">${exitBadge(r.exit_reason)}</div>`,
      sortValue: (r) => r.exit_date,
    },
    { key: "exit_price", label: "Exit $", num: true, render: (r) => fmtMoney(r.exit_price), sortValue: (r) => r.exit_price },
    { key: "holding_days", label: "Days", num: true, render: (r) => r.holding_days, sortValue: (r) => r.holding_days },
    {
      key: "return_pct",
      label: "Return",
      num: true,
      render: (r) => `<span class="strong ${pctClass(r.return_pct)}">${fmtPct(r.return_pct)}</span>`,
      sortValue: (r) => r.return_pct,
    },
    {
      key: "pnl_dollar",
      label: "P&L",
      num: true,
      render: (r) => `<span class="${pctClass(r.pnl_dollar)}">${fmtMoney(r.pnl_dollar, 0)}</span>`,
      sortValue: (r) => r.pnl_dollar,
    },
    {
      key: "confidence",
      label: "Conf.",
      num: true,
      render: (r) => `${r.confidence}%`,
      sortValue: (r) => r.confidence,
    },
    {
      key: "reason",
      label: "Trigger reason",
      render: (r) => `<span class="reason-cell" title="${escapeHtml(r.reason)}">${escapeHtml(r.reason)}</span>`,
      sortValue: (r) => r.reason,
    },
    {
      key: "url",
      label: "SEC filing",
      render: (r) => `<a class="sec-link" href="${escapeHtml(r.url)}" target="_blank" rel="noopener">View ↗</a>`,
      sortValue: () => "",
    },
  ];

  const table = createTable(columns, rows, {
    pageSize: 25,
    defaultSort: { key: "entry_date", dir: "desc" },
  });
  container.appendChild(table);

  function matchesHistoryFilter(row, q, year) {
    if (year !== "All" && !row.entry_date.startsWith(year)) return false;
    if (!q) return true;
    const text = (row.ticker + " " + row.company + " " + row.reason + " " + row.industry).toLowerCase();
    return text.includes(q.toLowerCase());
  }

  search.addEventListener("input", () => {
    const year = years.find((y) => yearChips[y].classList.contains("active"));
    table.setFilter((row) => matchesHistoryFilter(row, search.value, year));
  });

  return container;
}

/* ------------------------------------------------------------------ *
 *  Strategy section rendering
 * ------------------------------------------------------------------ */

function buildStrategySection(strategy) {
  const section = el("section", "strategy-section");
  section.id = strategy.key;
  section.setAttribute("aria-label", `${strategy.name} strategy details`);

  // Header
  const head = el("div", "section-head");
  const h2 = el("h2");
  h2.innerHTML = `<span class="rank-badge ${RANK_BADGE[strategy.rank]}">${escapeHtml(RANK_TEXT[strategy.rank])}</span>
                  <span class="mono-name">${escapeHtml(strategy.name)}</span>
                  <span class="chip">90-day holding</span>
                  <span class="chip">2021–2026 backtest</span>`;
  head.appendChild(h2);
  section.appendChild(head);

  section.appendChild(el("p", "strategy-desc", strategy.description));

  // KPI chips
  const k = strategy.kpis;
  const kpis = [
    { label: "Total return (ROI)", value: fmtPct(k.total_return_pct), cls: "pos", note: "over 6 years" },
    { label: "Final equity", value: fmtMoneyCompact(k.final_equity), note: "from $100k start" },
    { label: "Win rate", value: fmtPct(k.win_rate_pct, false), note: `${k.winning_trades}W / ${k.losing_trades}L` },
    { label: "Profit factor", value: k.profit_factor.toFixed(2), note: "won ÷ lost" },
    { label: "Sharpe ratio", value: k.sharpe_ratio.toFixed(2), note: "risk-adjusted" },
    { label: "Max drawdown", value: fmtPct(k.max_drawdown_pct, false), note: "worst dip" },
    { label: "Trades", value: k.total_trades.toLocaleString(), note: "all completed" },
    { label: "Holding period", value: `${k.holding_days} days`, note: `${k.stop_loss_pct}% stop · ${k.take_profit_pct}% target` },
  ];
  const grid = el("div", "kpi-grid");
  kpis.forEach((item) => {
    const box = el("div", "kpi");
    box.appendChild(el("div", "kpi-label", item.label));
    const val = el("div", "kpi-value" + (item.cls ? " " + item.cls : ""), item.value);
    if (item.note) val.appendChild(el("small", "", ` ${item.note}`));
    box.appendChild(val);
    grid.appendChild(box);
  });
  section.appendChild(grid);

  // --- Table 1: Active & upcoming trades (the action table) ---
  const activeBlock = el("div", "active-block");
  const activeTitle = el("div", "table-title");
  activeTitle.innerHTML = `<span class="flag" aria-hidden="true">🎯</span> Active &amp; upcoming trades`;
  activeBlock.appendChild(activeTitle);
  const countBadge = el("span", "chip", `${strategy.active.length} signal${strategy.active.length === 1 ? "" : "s"}`);
  activeTitle.appendChild(countBadge);

  if (strategy.active.length === 0) {
    const empty = el("div", "empty-state");
    empty.innerHTML = `<span class="big">🌤️</span>No fresh entry signals right now.
      Signals are re-scanned on every data refresh — hit <b>Refresh data</b> to re-pull the latest SEC filings.`;
    activeBlock.appendChild(empty);
  } else {
    activeBlock.appendChild(buildActiveTable(strategy, strategy.active));
  }
  section.appendChild(activeBlock);

  // --- Table 2: Full trade history ---
  section.appendChild(buildHistoryTable(strategy, strategy.trades, k));

  return section;
}

function buildOverviewCards(strategies) {
  const wrap = document.getElementById("strategyCards");
  wrap.innerHTML = "";

  strategies.forEach((s) => {
    const k = s.kpis;
    const card = el("div", "card");

    const rank = el("span", `card-rank ${RANK_CARD[s.rank]}`, RANK_TEXT[s.rank]);
    card.appendChild(rank);
    card.appendChild(el("div", "card-name", s.name));
    card.appendChild(el("p", "card-tagline", s.tagline));

    const roi = el("div", "card-roi");
    roi.innerHTML = `${fmtPct(k.total_return_pct)} <small>ROI · 2021–2026</small>`;
    card.appendChild(roi);

    const stats = el("div", "card-stats");
    stats.appendChild(el("span", "stat-chip", `Win rate <b>${fmtPct(k.win_rate_pct, false)}</b>`));
    stats.appendChild(el("span", "stat-chip", `Trades <b>${k.total_trades.toLocaleString()}</b>`));
    stats.appendChild(el("span", "stat-chip", `Sharpe <b>${k.sharpe_ratio.toFixed(2)}</b>`));
    stats.appendChild(el("span", "stat-chip", `Active <b>${s.active_count}</b>`));
    card.appendChild(stats);

    const actions = el("div", "card-actions");
    const seeActive = el("a", "btn btn-primary btn-sm", `🎯 ${s.active_count} active trade${s.active_count === 1 ? "" : "s"} — view`);
    seeActive.href = `#${s.key}`;
    actions.appendChild(seeActive);
    const seeHistory = el("a", "btn btn-ghost btn-sm", "Full trade history");
    seeHistory.href = `#${s.key}-history`;
    actions.appendChild(seeHistory);
    card.appendChild(actions);

    wrap.appendChild(card);
  });
}

/* ------------------------------------------------------------------ *
 *  Boot
 * ------------------------------------------------------------------ */

async function fetchJson(url) {
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to load ${url} (HTTP ${res.status})`);
  return res.json();
}

function showError(msg) {
  const cards = document.getElementById("strategyCards");
  cards.innerHTML = "";
  const err = el("div", "error-banner", msg);
  cards.appendChild(err);
}

async function init() {
  try {
    const [meta, strategies] = await Promise.all([fetchJson("data/meta.json"), fetchJson("data/strategies.json")]);
    state.meta = meta;
    state.strategies = strategies;
    state.generatedAt = meta.generated_at.slice(0, 10);

    // Header: updated badge + refresh link
    const updated = document.getElementById("updatedBadge");
    const date = new Date(meta.generated_at + "Z");
    updated.textContent = `Data updated: ${date.toUTCString().replace(" 00:00:00 GMT", "")}`;
    updated.title = "When the data on this page was last generated from SEC filings";
    const refreshBtn = document.getElementById("refreshBtn");
    refreshBtn.href = REFRESH_URL;
    refreshBtn.title =
      "One click: opens the “Daily Insider Trades & Heatmap Update” workflow in GitHub Actions — press “Run workflow” to re-pull the latest public insider trades from the SEC. The page also auto-updates every weekday at 22:00 UTC.";

    buildOverviewCards(strategies);

    // Render each strategy section (lazy per-strategy JSON)
    const sectionsHost = document.getElementById("strategySections");
    for (const s of strategies) {
      const placeholder = el("div", "container");
      placeholder.appendChild(el("div", "loading", `Loading ${s.name} trades…`));
      sectionsHost.appendChild(placeholder);
      try {
        const payload = await fetchJson(`data/${s.key}.json`);
        state.data[s.key] = payload;
        const section = buildStrategySection(payload);
        placeholder.replaceWith(section);
      } catch (e) {
        const err = el("div", "container");
        err.appendChild(el("div", "error-banner", `Could not load trades for ${s.name}: ${e.message}`));
        placeholder.replaceWith(err);
      }
    }
  } catch (e) {
    showError(`Could not load the dashboard data (${e.message}). If you’re viewing a local copy, serve the site folder over HTTP so the data files can be read.`);
  }
}

init();
