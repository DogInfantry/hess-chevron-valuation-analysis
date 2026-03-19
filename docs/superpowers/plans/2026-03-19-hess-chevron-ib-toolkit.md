# Hess/Chevron IB Toolkit — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a professional Jupyter Notebook analyzing the Chevron/Hess $53B acquisition using trading comps, precedent transactions, DCF, LBO, and accretion/dilution — all with publication-quality charts and interview-ready commentary.

**Architecture:** Python utility modules (config/constants, utils/styling, utils/data_fetch) provide data and chart functions. A single Jupyter notebook imports these modules and builds the analysis section by section. All charts use matplotlib/seaborn (no plotly). Live data from yfinance and FRED, hardcoded data from SEC filings.

**Tech Stack:** Python 3, Jupyter, yfinance, fredapi, pandas, numpy, scipy, matplotlib, seaborn, python-dotenv

**Spec:** `docs/superpowers/specs/2026-03-19-hess-chevron-ib-toolkit-design.md`

---

## File Map

| File | Responsibility | Created in Task |
|------|---------------|-----------------|
| `.gitignore` | Ignore .env, __pycache__, .ipynb_checkpoints, output/ | 1 |
| `.env.example` | Show expected FRED_API_KEY variable | 1 |
| `.env` | Actual FRED key (gitignored) | 1 |
| `requirements.txt` | All dependencies | 1 |
| `config/__init__.py` | Package init | 2 |
| `config/constants.py` | Hess financials, deal terms, precedent txns, CVX data | 2 |
| `config/fallback_data.py` | Cached peer data snapshot for yfinance outages | 2 |
| `utils/__init__.py` | Package init | 3 |
| `utils/styling.py` | IB_COLORS, matplotlib rcParams, chart helper functions | 3 |
| `utils/data_fetch.py` | yfinance + FRED wrappers with try/except fallbacks | 4 |
| `hess_chevron_analysis.ipynb` | The main deliverable notebook | 5-12 |
| `README.md` | GitHub landing page | 13 |

---

## Task 1: Project Scaffolding

**Files:**
- Create: `.gitignore`, `.env.example`, `.env`, `requirements.txt`

- [ ] **Step 1: Create .gitignore**

```
.env
__pycache__/
*.pyc
.ipynb_checkpoints/
output/
.DS_Store
```

- [ ] **Step 2: Create .env.example**

```
FRED_API_KEY=your_api_key_here
```

- [ ] **Step 3: Create .env with actual key**

Create `.env` file with the user's FRED API key (ask user or retrieve from memory). Do NOT hardcode the key in any committed file — only in `.env` which is gitignored.

- [ ] **Step 4: Create requirements.txt**

```
yfinance>=0.2.36
fredapi>=0.5.0
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0
seaborn>=0.12.0
python-dotenv>=1.0.0
```

- [ ] **Step 5: Install dependencies**

Run: `pip install -r requirements.txt`
Expected: All packages install successfully.

- [ ] **Step 6: Create output directory**

Run: `mkdir -p output`

- [ ] **Step 7: Clean up sample files from research phase**

Delete the sample PNGs (`01_football_field.png` through `08_stock_price.png`) and `ib_chart_samples.py` from the project root. These were research artifacts.

- [ ] **Step 8: Initialize git repo and commit**

```bash
git init
git add .gitignore .env.example requirements.txt
git commit -m "chore: project scaffolding with dependencies and gitignore"
```

---

## Task 2: Config — Constants & Hardcoded Data

**Files:**
- Create: `config/__init__.py`, `config/constants.py`, `config/fallback_data.py`

- [ ] **Step 1: Create config/__init__.py**

```python
"""Configuration and hardcoded financial data."""
```

- [ ] **Step 2: Create config/constants.py with Hess financials**

This file contains ALL hardcoded data from SEC filings. Structure it as Python dictionaries/dataframes.

Must include:
- `HESS_FINANCIALS`: dict with FY2022 and FY2023 income statement, balance sheet, cash flow items
  - Revenue, COGS/Production Costs, Exploration Expense, DD&A, G&A, EBITDA, EBIT, Net Income
  - Total Debt, Cash, Shares Outstanding (306.2M), Market Cap at unaffected price
  - Production: ~391 KBOEPD (2023), Guyana net ~195 KBOEPD
- `HESS_UNAFFECTED_PRICE`: 155.39
- `DEAL_TERMS`: dict with announcement date, exchange ratio (1.025), implied price (~171), equity value, EV, close date, premium
- `CVX_FINANCIALS`: dict with FY2023 EPS ($13.17), shares outstanding (~1.93B), projected EPS growth
- `PRECEDENT_TRANSACTIONS`: list of dicts, one per deal, with fields: acquirer, target, date, ev_billions, ev_ebitda, premium_1day (None for private targets)
- `PEER_TICKERS`: list of 10 tickers: ['CVX', 'XOM', 'COP', 'EOG', 'DVN', 'FANG', 'OXY', 'APA', 'CTRA', 'EQT']
- `HESS_PRODUCTION_HISTORY`: dict mapping year to KBOEPD for bar chart
- `DAMODARAN_EP`: dict with industry unlevered beta (~1.1), equity risk premium (5.5%), debt-to-equity ratio
- `SYNERGY_SCENARIOS`: list [0, 500, 1000, 1500] in $M
- `PEER_PRODUCTION_KBOEPD`: dict mapping ticker to approximate 2023 production in KBOEPD (for EV/BOEPD calculation). Source: company 10-Ks. E.g., {'CVX': 3100, 'XOM': 3700, 'COP': 1700, ...}

Source for Hess numbers: Hess 10-K FY2023, Hess proxy statement, Chevron merger announcement press release.

- [ ] **Step 3: Create config/fallback_data.py**

Cached snapshot of peer comps data (will be populated after first successful yfinance pull in Task 4). For now, create the file with a docstring and empty dict:

```python
"""
Fallback peer data cache.
Populated from last successful yfinance pull.
Used when yfinance is unavailable.
"""

FALLBACK_PEER_DATA = {}
```

- [ ] **Step 4: Verify imports work**

Run in Python:
```python
from config.constants import HESS_FINANCIALS, DEAL_TERMS, PRECEDENT_TRANSACTIONS, PEER_TICKERS
print(f"Hess FY2023 Revenue: ${HESS_FINANCIALS['FY2023']['revenue']/1e9:.1f}B")
print(f"Deal premium: {DEAL_TERMS['premium_1day_pct']}%")
print(f"Precedent deals: {len(PRECEDENT_TRANSACTIONS)}")
print(f"Peers: {PEER_TICKERS}")
```
Expected: Clean output with correct values.

- [ ] **Step 5: Commit**

```bash
git add config/
git commit -m "feat: add hardcoded Hess financials, deal terms, and precedent transactions"
```

---

## Task 3: Utils — Styling & Chart Helpers

**Files:**
- Create: `utils/__init__.py`, `utils/styling.py`

- [ ] **Step 1: Create utils/__init__.py**

```python
"""Utility functions for data fetching, styling, and chart generation."""
```

- [ ] **Step 2: Create utils/styling.py — Part 1: Colors, Style Setup, and Simple Charts**

Must include:

**IB_COLORS** dict — the full navy-blue palette from the spec (13 colors).

**`setup_ib_style()`** function — applies matplotlib rcParams:
- DPI: 100 for inline notebook rendering
- savefig.dpi: 150 for saved PNGs
- Font: sans-serif (Segoe UI, Calibri, Arial)
- Spines: top/right removed
- Grid: #E8E8E8, 0.5 linewidth, behind data
- Background: white
- Title: bold, 14pt
- Returns None, just sets global style

**Simple chart functions** (each returns a matplotlib Figure):

1. `plot_bar_chart(labels, values, title, xlabel, ylabel, highlight_idx=None, horizontal=False) -> Figure`
   - Generic bar chart with IB styling
   - Optional highlight bar in accent color
   - Value labels on bars
   - Figure size: 12×6

2. `plot_grouped_bar(labels, group_data: dict, title, ylabel) -> Figure`
   - Multiple groups side by side
   - Legend with group names
   - Figure size: 12×6

3. `plot_area_chart(df, title, ylabel) -> Figure`
   - Stacked area chart (for debt paydown schedule)
   - Figure size: 12×6

4. `plot_oil_price_chart(wti_series, brent_series, events: dict, title) -> Figure`
   - Dual line chart with event annotations using `ax.annotate()` with arrow
   - Figure size: 14×6

5. `format_comps_table(df) -> Styler`
   - Pandas Styler that formats a comps dataframe with proper number formatting
   - Alternating row colors (white / pale blue)
   - Bold header row
   - Returns styled dataframe for notebook display

- [ ] **Step 3: Create utils/styling.py — Part 2: Complex IB-Specific Charts**

Add these functions to `utils/styling.py`. These are the complex chart types that need detailed implementation guidance:

6. `plot_football_field(valuations: dict, offer_price: float, title: str) -> Figure`
   - `valuations`: dict like `{'Trading Comps': (low, mid, high), 'DCF': (low, mid, high), ...}`
   - Implementation approach:
     ```python
     fig, ax = plt.subplots(figsize=(14, 8))
     methods = list(valuations.keys())
     y_positions = range(len(methods))
     for i, (method, (lo, mid, hi)) in enumerate(valuations.items()):
         # Draw horizontal bar from lo to hi
         ax.barh(i, hi - lo, left=lo, height=0.5, color=IB_COLORS['navy'], alpha=0.8)
         # White diamond at midpoint
         ax.plot(mid, i, 'D', color='white', markersize=8, zorder=5)
         # Value labels at lo and hi ends
         ax.text(lo - 2, i, f'${lo:.0f}', ha='right', va='center')
         ax.text(hi + 2, i, f'${hi:.0f}', ha='left', va='center')
     # Dashed vertical line for offer price
     ax.axvline(offer_price, color=IB_COLORS['accent_red'], linestyle='--', linewidth=2, label=f'Offer: ${offer_price:.0f}')
     ax.set_yticks(y_positions)
     ax.set_yticklabels(methods)
     ax.set_xlabel('Implied Share Price ($)')
     ```
   - Figure size: 14×8

7. `plot_sensitivity_heatmap(row_values, col_values, data_matrix, row_label, col_label, title, highlight_row_idx, highlight_col_idx, fmt='$.0f') -> Figure`
   - Implementation approach:
     ```python
     fig, ax = plt.subplots(figsize=(10, 8))
     sns.heatmap(data_matrix, annot=True, fmt='', cmap='RdYlGn',
                 xticklabels=[f'{v:.1%}' for v in col_values],
                 yticklabels=[f'{v:.1%}' for v in row_values], ax=ax)
     # Highlight base case cell with red rectangle
     ax.add_patch(plt.Rectangle((highlight_col_idx, highlight_row_idx), 1, 1,
                                fill=False, edgecolor='red', linewidth=3))
     ```
   - Format cell annotations as dollar amounts
   - Figure size: 10×8

8. `plot_waterfall(labels, values, title) -> Figure`
   - First value is the starting total (e.g., Revenue), subsequent values are changes (negative for costs)
   - Implementation approach:
     ```python
     cumulative = [values[0]]
     for v in values[1:-1]:
         cumulative.append(cumulative[-1] + v)  # v is negative for costs
     cumulative.append(values[-1])  # final total
     # Draw bars: green for positive changes, red for negative, navy for totals (first and last)
     # Use bottom= parameter to stack bars from the running total
     # Draw thin connector lines between bar tops/bottoms
     ```
   - Value annotations formatted as $B on each bar
   - Figure size: 14×7

9. `plot_tornado(labels, low_values, high_values, base_value, title) -> Figure`
   - Sort by total range (widest at top)
   - Implementation approach:
     ```python
     ranges = [abs(h - l) for l, h in zip(low_values, high_values)]
     sorted_idx = sorted(range(len(labels)), key=lambda i: ranges[i], reverse=True)
     # For each assumption, draw two bars extending from base_value
     # Left bar: base_value to low_value (if low < base)
     # Right bar: base_value to high_value (if high > base)
     ```
   - Label each bar end with the dollar value
   - Figure size: 12×7

10. `plot_monte_carlo_hist(simulations, offer_price, title) -> Figure`
    - Implementation approach:
      ```python
      fig, ax = plt.subplots(figsize=(12, 7))
      # Two-tone histogram: bins below offer in navy, bins above in steel_blue
      ax.hist(simulations, bins=80, color=IB_COLORS['navy'], alpha=0.7, edgecolor='white')
      # Vertical lines for percentiles
      for pct, label in [(10, '10th'), (50, 'Median'), (90, '90th')]:
          val = np.percentile(simulations, pct)
          ax.axvline(val, color=IB_COLORS['dark_gray'], linestyle=':', alpha=0.8)
          ax.text(val, ax.get_ylim()[1]*0.95, f'{label}\n${val:.0f}', ha='center')
      # Offer price line
      ax.axvline(offer_price, color=IB_COLORS['accent_red'], linestyle='--', linewidth=2)
      # Probability callout box
      pct_above = (simulations > offer_price).mean() * 100
      ax.text(0.98, 0.95, f'{pct_above:.1f}% of simulations\nabove offer price',
              transform=ax.transAxes, ha='right', va='top',
              bbox=dict(boxstyle='round', facecolor=IB_COLORS['pale_blue']))
      ```

11. `plot_comps_scatter(peer_data_df, hess_point, x_col, y_col, size_col, title) -> Figure`
    - `hess_point`: tuple (x_val, y_val, size_val, 'Hess')
    - Implementation approach:
      ```python
      fig, ax = plt.subplots(figsize=(12, 8))
      # Scale bubble sizes: sizes = peer_data_df[size_col] / peer_data_df[size_col].max() * 500
      ax.scatter(peer_data_df[x_col], peer_data_df[y_col], s=sizes,
                 color=IB_COLORS['steel_blue'], alpha=0.6, edgecolors=IB_COLORS['navy'])
      # Annotate each peer with company name
      for _, row in peer_data_df.iterrows():
          ax.annotate(row['shortName'], (row[x_col], row[y_col]), fontsize=8)
      # Hess as star marker
      ax.plot(hess_point[0], hess_point[1], '*', color=IB_COLORS['accent_red'],
              markersize=20, zorder=5, label='Hess (implied)')
      # Regression line
      z = np.polyfit(peer_data_df[x_col], peer_data_df[y_col], 1)
      p = np.poly1d(z)
      x_line = np.linspace(peer_data_df[x_col].min(), peer_data_df[x_col].max(), 100)
      ax.plot(x_line, p(x_line), '--', color=IB_COLORS['gray'], alpha=0.5)
      ```
    - Axis range for E&P: 3x-12x EV/EBITDA

- [ ] **Step 4: Verify styling imports and a test chart renders**

Run in Python:
```python
from utils.styling import setup_ib_style, plot_bar_chart, IB_COLORS
import matplotlib.pyplot as plt

setup_ib_style()
fig = plot_bar_chart(
    labels=['CVX', 'XOM', 'COP', 'EOG', 'DVN'],
    values=[5.8, 6.2, 5.5, 7.1, 4.9],
    title='Test: E&P EV/EBITDA Multiples',
    xlabel='Company',
    ylabel='EV/EBITDA (x)',
    highlight_idx=2
)
fig.savefig('output/test_bar.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to output/test_bar.png")
```
Expected: A clean PNG with navy bars, one highlighted, proper labels. Verify visually.

- [ ] **Step 5: Commit**

```bash
git add utils/
git commit -m "feat: add IB styling system and chart helper functions"
```

---

## Task 4: Utils — Data Fetching with Fallbacks

**Files:**
- Create: `utils/data_fetch.py`
- Modify: `config/fallback_data.py` (populate with real cache after first successful pull)

- [ ] **Step 1: Create utils/data_fetch.py**

Must include:

**`fetch_peer_comps(tickers: list) -> pd.DataFrame`**
- Iterates through tickers, calls `yf.Ticker(t).info` for each
- Extracts: marketCap, enterpriseValue, enterpriseToEbitda, enterpriseToRevenue, trailingPE, forwardPE, sector, shortName
- Each ticker wrapped in try/except — failed tickers logged and skipped
- Returns DataFrame with one row per successful ticker
- If fewer than 5 tickers return data, falls back to `config.fallback_data.FALLBACK_PEER_DATA`
- Prints status: "Fetched 8/10 peers (skipped: FANG, APA)"

**`fetch_commodity_prices(start='2020-01-01') -> dict`**
- Downloads WTI (CL=F), Brent (BZ=F), NatGas (NG=F), 10Y yield (^TNX), XLE, XOP, ^GSPC via `yf.download()`
- Returns dict of DataFrames keyed by name
- try/except per ticker, returns what's available

**`fetch_fred_data(api_key: str) -> dict`**
- Uses fredapi to pull: BAMLH0A0HYM2, DHHNGSP, DFF, T10Y2Y
- Returns dict of Series keyed by code
- try/except — if FRED fails entirely, returns empty dict with warning

**`validate_tickers(tickers: list) -> tuple[list, list]`**
- Quick validation: tries `yf.Ticker(t).info.get('shortName')` for each
- Returns (valid_tickers, failed_tickers)

**`save_fallback_cache(peer_df: pd.DataFrame)`**
- Saves the peer DataFrame as a Python dict literal to `config/fallback_data.py`
- Only called on successful full pull

- [ ] **Step 2: Verify data fetch works**

Run in Python:
```python
from utils.data_fetch import fetch_peer_comps, fetch_commodity_prices, fetch_fred_data
from config.constants import PEER_TICKERS
import os

# Test peer comps
peers = fetch_peer_comps(PEER_TICKERS)
print(f"Peers fetched: {len(peers)}")
print(peers[['shortName', 'enterpriseToEbitda']].to_string())

# Test commodities
commodities = fetch_commodity_prices()
for name, df in commodities.items():
    print(f"{name}: {len(df)} rows, latest: {df.index[-1].date()}")

# Test FRED
fred = fetch_fred_data(os.getenv('FRED_API_KEY'))
for code, series in fred.items():
    print(f"FRED {code}: {len(series)} obs, latest: {series.index[-1].date()}")
```
Expected: Peer data for 8-10 companies, commodity data from 2020, FRED data.

- [ ] **Step 3: Populate fallback_data.py with real cached data**

After a successful `fetch_peer_comps()` run, call `save_fallback_cache()` to write the snapshot.

- [ ] **Step 4: Commit**

```bash
git add utils/data_fetch.py config/fallback_data.py
git commit -m "feat: add data fetching with yfinance/FRED and fallback caching"
```

---

## Task 5: Notebook — Setup & Executive Summary (Section 1)

**Files:**
- Create: `hess_chevron_analysis.ipynb`

- [ ] **Step 1: Create notebook with setup cells**

Cell 1 (code): Imports + style setup
```python
import sys, os, warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from dotenv import load_dotenv

load_dotenv()

from config.constants import (HESS_FINANCIALS, HESS_UNAFFECTED_PRICE, DEAL_TERMS,
    CVX_FINANCIALS, PRECEDENT_TRANSACTIONS, PEER_TICKERS, HESS_PRODUCTION_HISTORY,
    DAMODARAN_EP, SYNERGY_SCENARIOS)
from utils.styling import (setup_ib_style, IB_COLORS, plot_football_field,
    plot_sensitivity_heatmap, plot_waterfall, plot_tornado, plot_monte_carlo_hist,
    plot_comps_scatter, plot_bar_chart, plot_grouped_bar, plot_area_chart,
    plot_oil_price_chart, format_comps_table)
from utils.data_fetch import fetch_peer_comps, fetch_commodity_prices, fetch_fred_data, validate_tickers

setup_ib_style()
np.random.seed(42)
```

Cell 2 (code): Data loading — fetch all live data upfront
```python
# Validate and fetch peer data
valid_tickers, failed_tickers = validate_tickers(PEER_TICKERS)
print(f"✓ {len(valid_tickers)}/{len(PEER_TICKERS)} peers available")
if failed_tickers:
    print(f"  Skipped: {failed_tickers}")

peer_data = fetch_peer_comps(valid_tickers)
commodities = fetch_commodity_prices()
fred_data = fetch_fred_data(os.getenv('FRED_API_KEY'))
```

- [ ] **Step 2: Add Executive Summary markdown and placeholder football field**

Cell 3 (markdown): Executive Summary header + deal overview bullets + key findings table (uses placeholder values that will be replaced in Task 12 after all analyses are computed).

Cell 4 (code): Football field chart — initially with placeholder valuation ranges. Will be updated in Task 12 with real computed values. Comment clearly: `# PLACEHOLDER — updated in Section 8 after all analyses`.

- [ ] **Step 3: Run notebook top-to-bottom, verify setup cells execute clean**

Run: `jupyter nbconvert --execute hess_chevron_analysis.ipynb --to notebook --output hess_chevron_analysis.ipynb`
Expected: No errors. Data loads. Placeholder chart renders.

- [ ] **Step 4: Commit**

```bash
git add hess_chevron_analysis.ipynb
git commit -m "feat: notebook setup with data loading and executive summary placeholder"
```

---

## Task 6: Notebook — Company & Industry Overview (Section 2)

**Files:**
- Modify: `hess_chevron_analysis.ipynb` (add cells after Section 1)

- [ ] **Step 1: Add Section 2 markdown cells**

Markdown cells covering:
- Hess Corporation profile (founded 1933, upstream E&P, HQ NYC)
- Key assets: Guyana Stabroek Block (30% interest, operator: Exxon, ~11B BOE recoverable), Bakken, Gulf of Mexico, Southeast Asia
- Why Guyana matters: giant resource, low-cost barrel (~$35/bbl breakeven), production ramp from 0 in 2019 to ~640 KBOEPD gross by 2027
- E&P consolidation wave: 2023-2024 saw $200B+ in deals as majors locked up Permian and international acreage
- Why Chevron wants Hess: Guyana diversifies CVX's Permian-heavy portfolio, adds decades of production growth

Use the "What we're doing / Key assumptions / So what / Limitations" framework.

- [ ] **Step 2: Add oil price chart**

Code cell using `plot_oil_price_chart()` with WTI and Brent from `commodities` dict. Annotate events:
- Mar 2020: "COVID crash"
- Feb 2022: "Russia invades Ukraine"
- Oct 2022: "OPEC+ cuts"
- Oct 2023: "CVX-HES announced"

- [ ] **Step 3: Add Hess production growth bar chart**

Code cell using `plot_bar_chart()` with `HESS_PRODUCTION_HISTORY` data. Show KBOEPD by year (2019-2023).

- [ ] **Step 4: Add E&P sector performance chart**

Code cell: plot XLE and XOP ETF performance (normalized to 100) vs S&P 500 (^GSPC) from 2020-present using data from `commodities` dict. Shows energy sector's relative performance in the consolidation era.

- [ ] **Step 5: Run notebook, verify Section 2 renders**

Expected: Three charts render cleanly with proper annotations.

- [ ] **Step 6: Commit**

```bash
git add hess_chevron_analysis.ipynb
git commit -m "feat: add company overview with oil price, production, and sector charts"
```

---

## Task 7: Notebook — Trading Comps (Section 3)

**Files:**
- Modify: `hess_chevron_analysis.ipynb`

- [ ] **Step 1: Add Section 3 markdown — methodology explanation**

Explain: what trading comps are, why we use them, peer selection rationale (large-cap E&P, diverse basins, similar risk profile). Note EQT divergence as gas-weighted.

- [ ] **Step 2: Add comps table code cell**

- Build DataFrame from `peer_data` with columns: Company, Market Cap, EV, EV/EBITDA, EV/Revenue, P/E, EV/BOEPD
- EV/BOEPD calculated using `PEER_PRODUCTION_KBOEPD` from constants (production data from 10-Ks, not available in yfinance)
- Add Hess row derived from hardcoded financials + unaffected price
- Calculate Hess EV = (unaffected price × shares_outstanding) + total_debt - cash
- Calculate Hess multiples from that EV and hardcoded EBITDA/Revenue
- Add summary row: Mean, Median, 25th percentile, 75th percentile
- Display with `format_comps_table()`

- [ ] **Step 3: Add implied valuation range calculation**

Code cell:
- Apply peer median and mean EV/EBITDA to Hess EBITDA → implied EV → implied equity → implied share price
- Same for EV/Revenue
- Store results in a dict for use in football field later: `comps_valuation = {'low': ..., 'mid': ..., 'high': ...}`

- [ ] **Step 4: Add comps scatter plot**

Code cell using `plot_comps_scatter()`:
- x-axis: EV/EBITDA (range 3x-12x)
- y-axis: production growth % (if available from info, else revenue growth)
- Bubble size: market cap
- Star marker for Hess
- Regression line

- [ ] **Step 5: Add peer EV/EBITDA bar chart**

Code cell using `plot_bar_chart()`:
- Peers ranked by EV/EBITDA
- Hess implied range shown as horizontal shaded band

- [ ] **Step 6: Add "So what" markdown**

Commentary: where Hess sits relative to peers, what the premium implies about market expectations for Guyana.

- [ ] **Step 7: Run notebook, verify Section 3**

Expected: Formatted table, scatter plot, bar chart all render. Implied valuation computed.

- [ ] **Step 8: Commit**

```bash
git add hess_chevron_analysis.ipynb
git commit -m "feat: add trading comps analysis with scatter plot and implied valuation"
```

---

## Task 8: Notebook — Precedent Transactions (Section 4)

**Files:**
- Modify: `hess_chevron_analysis.ipynb`

- [ ] **Step 1: Add Section 4 markdown — methodology explanation**

Explain: what precedent transactions analysis is, why 2020-2024 window, the E&P M&A wave context.

- [ ] **Step 2: Add precedent transactions table**

Code cell:
- Build DataFrame from `PRECEDENT_TRANSACTIONS`
- Display as formatted table with: Acquirer, Target, Date, EV ($B), EV/EBITDA, Premium
- Highlight the Chevron/Hess row

- [ ] **Step 3: Add EV/EBITDA bar chart for precedent deals**

Code cell using `plot_bar_chart()`:
- All 11 deals sorted by EV/EBITDA
- Chevron/Hess bar highlighted in accent color
- Median line drawn horizontally

- [ ] **Step 4: Add premium analysis bar chart**

Code cell using `plot_bar_chart()`:
- Only 7 public deals with premium data
- 1-day premium bars
- Chevron/Hess highlighted

- [ ] **Step 5: Calculate implied valuation range**

Code cell:
- Apply median/mean EV/EBITDA from precedents to Hess EBITDA → implied share price
- Store: `precedent_valuation = {'low': ..., 'mid': ..., 'high': ...}`

- [ ] **Step 6: Add "So what" markdown**

Commentary: Chevron's 8.4x EV/EBITDA is above median (~5.8x), suggesting premium for Guyana optionality. 10% premium is below median (~13%), suggesting Hess shareholders may not be getting full value.

- [ ] **Step 7: Commit**

```bash
git add hess_chevron_analysis.ipynb
git commit -m "feat: add precedent transactions analysis with premium and multiples charts"
```

---

## Task 9: Notebook — DCF Valuation (Section 5)

**Files:**
- Modify: `hess_chevron_analysis.ipynb`

This is the largest section — contains the waterfall, sensitivity heatmap, Monte Carlo, and tornado charts.

- [ ] **Step 1: Add Section 5 markdown — DCF methodology explanation**

Explain DCF in plain English: project future cash flows, discount back to today. State all key assumptions upfront.

- [ ] **Step 2: Add revenue projection build**

Code cell:
- Base oil price deck: $75/bbl WTI (from current futures)
- Production growth: 5% CAGR (Guyana ramp)
- 5-year revenue projection table
- Display as formatted DataFrame

- [ ] **Step 3: Add UFCF derivation and waterfall chart**

Code cell — **IMPORTANT: DD&A treatment in UFCF calculation:**
The correct UFCF formula is:
```
EBITDA = Revenue - Production Costs - Exploration - G&A
EBIT = EBITDA - DD&A
NOPAT = EBIT × (1 - tax_rate)
UFCF = NOPAT + DD&A (add back, non-cash) - CapEx - Change in NWC
```
DD&A is subtracted to compute EBIT and taxes, then ADDED BACK because it is non-cash. The waterfall chart should show this explicitly:
- Revenue → (-) Production Costs (~45%) → (-) Exploration (~5%) → (-) G&A (~3%) → = EBITDA → (-) DD&A (~15%) → = EBIT → (-) Taxes (21% of EBIT) → (+) DD&A Add-Back → (-) CapEx (~25% of revenue) → = UFCF

Use Hess FY2023 margins as base, adjust for Guyana mix improvement.
Display waterfall using `plot_waterfall()` with E&P-specific line items.

- [ ] **Step 4: Add WACC calculation**

Code cell:
- Risk-free rate: pulled from ^TNX (live) or 4.2% fallback
- Beta: 1.1 (Damodaran E&P industry unlevered, relevered for Hess capital structure)
- ERP: 5.5% (Damodaran)
- Cost of equity via CAPM
- Cost of debt: ~4.5% (Hess average)
- WACC: weighted by D/E ratio
- Display calculation table showing each input

- [ ] **Step 5: Add terminal value and implied share price**

Code cell:
- Terminal growth rate: 2.0% (base case)
- Terminal value via perpetuity growth method
- PV of FCFs + PV of terminal value = Enterprise value
- Subtract net debt, divide by shares → implied share price
- Store: `dcf_base_case = implied_price`

- [ ] **Step 6: Add sensitivity heatmap**

Code cell:
- WACC range: 8% to 12% (0.5% steps)
- Terminal growth range: 1% to 3% (0.25% steps)
- 2D matrix of implied share prices
- Use `plot_sensitivity_heatmap()` with base case highlighted
- Store min/max for football field: `dcf_valuation = {'low': ..., 'mid': dcf_base_case, 'high': ...}`

- [ ] **Step 7: Add Monte Carlo simulation**

Code cell:
- 10,000 iterations with `np.random.seed(42)`
- Randomize: oil price (normal, μ=$75, σ=$10), production growth (normal, μ=5%, σ=2%), EBITDA margin (normal, μ=55%, σ=5%), WACC (normal, μ=10%, σ=1%), terminal growth (normal, μ=2%, σ=0.5%)
- **IMPORTANT: Clip WACC draws** to ensure `WACC > terminal_growth + 1%` (minimum ~3.5%). Without this floor, the perpetuity growth terminal value formula produces negative/infinite values when WACC ≤ terminal growth. Use `np.clip()` after drawing.
- Calculate implied share price for each run
- Use `plot_monte_carlo_hist()` with Chevron offer at $171
- Print: median, mean, % of runs above offer price, 10th/90th percentile

- [ ] **Step 8: Add tornado chart**

Code cell:
- For each assumption, hold others at base case, vary ±1σ
- Calculate implied share price at each extreme
- Use `plot_tornado()` sorted by impact range
- Clearly shows which assumption matters most

- [ ] **Step 9: Add "So what" and "Limitations" markdown**

Commentary: DCF base case vs. offer price, what Monte Carlo tells us about probability, key swing factors (oil price is probably #1).

- [ ] **Step 10: Commit**

```bash
git add hess_chevron_analysis.ipynb
git commit -m "feat: add DCF valuation with sensitivity, Monte Carlo, and tornado analysis"
```

---

## Task 10: Notebook — LBO Analysis (Section 6)

**Files:**
- Modify: `hess_chevron_analysis.ipynb`

- [ ] **Step 1: Add Section 6 markdown — LBO methodology + caveat**

Explain LBO in plain English. State explicitly: "$53B LBO is hypothetical — no PE fund could finance this at scale. This demonstrates methodology, not a real-world scenario." Debt pricing uses IG-adjacent spreads.

- [ ] **Step 2: Add sources & uses**

Code cell:
- Purchase price: ~$60B EV (at offer)
- Sources: Senior Secured (~30% EV, SOFR+200bps), Senior Unsecured (~20%, SOFR+350bps), Subordinated (~10%, 8.5% fixed), Equity (~40%)
- Uses: Purchase price, fees (~2%), existing debt refinancing
- Display as formatted table
- Add stacked bar chart using `plot_grouped_bar()` showing sources vs uses side by side

- [ ] **Step 3: Add 5-year financial projections and debt schedule**

Code cell:
- Project EBITDA (5% growth from base)
- Mandatory debt repayment schedule (Senior Secured amortizes, others bullet)
- Interest expense calculation per tranche
- Free cash flow available for debt paydown
- Cash sweep: excess FCF pays down most expensive tranche first
- Display as year-by-year table

- [ ] **Step 4: Add debt paydown area chart**

Code cell using `plot_area_chart()`:
- Stacked areas showing Senior Secured, Senior Unsecured, Subordinated balance over 5 years
- Shows deleveraging trajectory

- [ ] **Step 5: Add exit analysis and IRR/MOIC**

Code cell:
- Exit at year 5 at range of EV/EBITDA multiples (5x to 9x, 0.5x steps)
- Calculate equity value at exit = Exit EV - remaining debt
- IRR = (equity_exit / equity_entry)^(1/5) - 1
- MOIC = equity_exit / equity_entry
- Display as table

- [ ] **Step 6: Add IRR/MOIC sensitivity heatmap**

Code cell using `plot_sensitivity_heatmap()`:
- Rows: entry EV/EBITDA (7x to 10x)
- Cols: exit EV/EBITDA (5x to 9x)
- Values: IRR (formatted as %)
- Base case highlighted
- Store: `lbo_valuation = {'low': ..., 'mid': ..., 'high': ...}` (implied share prices where IRR = 15-25%)

- [ ] **Step 7: Add "So what" markdown**

Commentary: what IRR ranges PE firms target (20-25%), what entry price makes this work, why the Chevron all-stock deal makes more sense than LBO at this scale.

- [ ] **Step 8: Commit**

```bash
git add hess_chevron_analysis.ipynb
git commit -m "feat: add LBO analysis with debt schedule and IRR sensitivity"
```

---

## Task 11: Notebook — Accretion/Dilution & Synergy Analysis (Section 7)

**Files:**
- Modify: `hess_chevron_analysis.ipynb`

- [ ] **Step 1: Add Section 7 markdown — methodology**

Explain accretion/dilution: does the deal increase or decrease the acquirer's EPS? This is the first question a banker asks about any all-stock deal.

- [ ] **Step 2: Add standalone EPS calculations**

Code cell:
- CVX standalone: EPS $13.17 (FY2023), ~1.93B shares
- HES standalone: net income from hardcoded financials, ~306M shares
- Combined shares: CVX shares + (HES shares × 1.025)
- Combined net income: CVX + HES (no synergies)
- Pro forma EPS without synergies

- [ ] **Step 3: Add synergy sensitivity**

Code cell:
- Loop through synergy scenarios: $0, $500M, $1B, $1.5B (after-tax at 21%)
- Combined net income + after-tax synergies
- Pro forma EPS at each level
- Accretion/(dilution) = (pro_forma_EPS - CVX_standalone_EPS) / CVX_standalone_EPS
- Display as formatted table

- [ ] **Step 4: Add accretion/dilution bar chart**

Code cell using `plot_bar_chart()`:
- x-axis: synergy levels
- y-axis: accretion/dilution %
- Bars: green if accretive, red if dilutive
- Horizontal line at 0%

- [ ] **Step 5: Add break-even synergy calculation**

Code cell:
- Solve for synergy level where pro forma EPS = CVX standalone EPS
- Display as single number with commentary
- Add waterfall chart showing: CVX EPS → dilution from share issuance → accretion from HES earnings → synergy needed to break even

- [ ] **Step 6: Add "So what" markdown**

Commentary: deal is likely dilutive in Year 1 without synergies, but Chevron's $1B+ synergy guidance brings it to roughly breakeven or slightly accretive. Strategic value of Guyana justifies near-term dilution.

- [ ] **Step 7: Commit**

```bash
git add hess_chevron_analysis.ipynb
git commit -m "feat: add accretion/dilution analysis with synergy sensitivity"
```

---

## Task 12: Notebook — Deal Assessment & Final Football Field (Section 8)

**Files:**
- Modify: `hess_chevron_analysis.ipynb`

- [ ] **Step 1: Add Section 8 markdown — pulling it all together**

Summary narrative that synthesizes all analyses.

- [ ] **Step 2: Build comprehensive football field chart**

Code cell:
- Gather all valuation ranges computed in Tasks 7-11:
  - `comps_valuation` from Section 3
  - `precedent_valuation` from Section 4
  - `dcf_valuation` from Section 5
  - `lbo_valuation` from Section 6
- Also add: "52-Week Range" from hardcoded Hess pre-deal trading range
- Use `plot_football_field()` with Chevron offer at $171
- This is THE chart — make sure it renders at 14×8 with clear labels

- [ ] **Step 3: Add valuation summary table**

Code cell:
- One row per methodology
- Columns: Method, Low, Mid, High, Implied Premium/(Discount) to Offer
- Formatted with proper $ and % symbols

- [ ] **Step 4: Add Exxon arbitration risk discussion**

Markdown cell:
- Exxon claimed preemptive rights over Hess's Stabroek interest
- ICC arbitration proceedings
- September 2024: tribunal ruled in favor of Chevron/Hess
- Risk was: if Exxon won, Chevron loses the primary deal rationale
- Impact: deal uncertainty depressed Hess's stock during arbitration period

- [ ] **Step 5: Add final recommendation**

Markdown cell:
- Synthesize: Chevron's offer sits within/above/below the implied range
- The 10% premium is relatively thin for E&P deals (median ~13%)
- But Guyana optionality and certainty of an all-stock deal with a supermajor provide strategic value
- Recommendation: Fair deal for Hess shareholders, with the Guyana growth premium not fully captured in traditional valuation methods

- [ ] **Step 6: Go back and update Executive Summary (Section 1)**

Update the placeholder football field and summary table in Section 1 with the real computed values. Use the same `plot_football_field()` call but smaller (12×6) for the summary version.

- [ ] **Step 7: Run full notebook top-to-bottom, verify all cells execute**

Run: `jupyter nbconvert --execute hess_chevron_analysis.ipynb --to notebook --output hess_chevron_analysis.ipynb`
Expected: Clean execution, all charts render, no errors.

- [ ] **Step 8: Check notebook file size**

Run: `ls -lh hess_chevron_analysis.ipynb`
If over 1MB: reduce DPI to 80 for inline charts, or save charts to `output/` and reference via markdown images.

- [ ] **Step 9: Commit**

```bash
git add hess_chevron_analysis.ipynb
git commit -m "feat: add deal assessment with comprehensive football field and recommendation"
```

---

## Task 13: README & Final Polish

**Files:**
- Create: `README.md`
- Modify: `hess_chevron_analysis.ipynb` (final polish pass)

- [ ] **Step 1: Create README.md**

Professional GitHub landing page:

```markdown
# Hess Corporation: Investment Banking Analysis
## Chevron's $53B Acquisition — Valuation & Deal Assessment

A comprehensive investment banking analysis of Chevron's acquisition of Hess Corporation,
built in Python with live market data.

### Analyses Included
- **Trading Comps** — 10 E&P peers, live multiples via Yahoo Finance
- **Precedent Transactions** — 11 recent E&P M&A deals (2020-2024)
- **DCF Valuation** — 5-year projections, Monte Carlo simulation (10,000 runs), sensitivity analysis
- **LBO Analysis** — Hypothetical buyout, IRR/MOIC sensitivity
- **Accretion/Dilution** — Synergy sensitivity, break-even analysis
- **Deal Assessment** — Football field valuation, Exxon arbitration risk, recommendation

### Data Sources
| Source | Data | API Key Required? |
|--------|------|-------------------|
| Yahoo Finance (`yfinance`) | Peer financials, stock prices, commodities | No |
| FRED (`fredapi`) | Treasury yields, credit spreads, macro data | Yes (free) |
| SEC EDGAR (hardcoded) | Hess 10-K financials, deal terms | No |
| Damodaran Online (hardcoded) | Industry betas, equity risk premium | No |

### Tech Stack
Python · Jupyter · pandas · numpy · scipy · matplotlib · seaborn · yfinance · fredapi

### How to Run
1. Clone this repo
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your FRED API key
4. Open `hess_chevron_analysis.ipynb` in Jupyter

Or just scroll through the notebook on GitHub — all charts render as static images.
```

- [ ] **Step 2: Final polish pass on notebook**

Review every markdown cell for:
- Typos
- Consistent formatting
- Every section has: What we're doing / Key assumptions / So what / Limitations
- All charts have: title, axis labels, source annotations
- No debug print statements left in code cells

- [ ] **Step 3: Run final execution**

Run: `jupyter nbconvert --execute hess_chevron_analysis.ipynb --to notebook --output hess_chevron_analysis.ipynb`
Verify: clean execution, all charts, no warnings visible.

- [ ] **Step 4: Commit everything**

```bash
git add README.md hess_chevron_analysis.ipynb
git commit -m "feat: add README and final polish on notebook"
```

- [ ] **Step 5: Final git status check**

Run: `git status` — should be clean.
Run: `git log --oneline` — should show clean commit history.

---

## Execution Notes

- **Tasks 1-4** (scaffolding, config, styling, data fetch) are independent infrastructure — can be parallelized
- **Tasks 5-12** (notebook sections) must be sequential — each section builds on prior data
- **Task 13** (README + polish) depends on all prior tasks
- Each task produces a working, committable state
- The notebook should execute cleanly after every task (even if later sections don't exist yet)
