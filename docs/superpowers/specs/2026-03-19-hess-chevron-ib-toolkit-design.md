# Hess Corporation: Comprehensive IB Valuation & M&A Analysis Toolkit

## Design Specification

**Date:** 2026-03-19
**Deliverable:** Single Jupyter Notebook (.ipynb)
**Subject:** Chevron's $53B acquisition of Hess Corporation
**Purpose:** Investment banking work proof for generalist M&A recruiting — designed to impress recruiters, hiring managers, and bankers when viewed on GitHub

---

## 1. Project Overview

A self-contained Jupyter Notebook that performs a full investment banking analysis of the Chevron/Hess deal. The notebook combines five valuation methodologies (trading comps, precedent transactions, DCF, LBO, accretion/dilution) into a cohesive narrative with professional-grade visualizations, plain English commentary, and real market data.

The target audience views this on GitHub without running any code. Every chart renders as a static PNG. Every section includes explanatory markdown cells so the author can speak to the analysis in interviews.

---

## 2. Data Architecture

### 2.1 Live Data (yfinance — no API key)

| Data | Ticker/Symbol | Usage |
|------|---------------|-------|
| Peer financials & multiples | CVX, XOM, COP, EOG, DVN, FANG, OXY, APA, CTRA, EQT | Trading comps |
| WTI Crude Oil (front-month futures) | CL=F | Industry context |
| Brent Crude Oil (front-month futures) | BZ=F | Industry context |
| Natural Gas Futures (front-month) | NG=F | Industry context |
| 10-Year Treasury Yield | ^TNX | WACC (risk-free rate) |
| Energy ETFs | XLE, XOP | Sector performance |
| S&P 500 | ^GSPC | Market benchmark |

**Note:** CL=F, BZ=F, NG=F are continuous front-month futures contracts, not spot prices. This is standard for market context charts and is noted in the notebook.

### 2.2 Live Data (FRED API — free key required)

| Series | Code | Usage |
|--------|------|-------|
| High Yield OAS Spread | BAMLH0A0HYM2 | Credit market context |
| Henry Hub Natural Gas | DHHNGSP | Gas price context |
| Fed Funds Rate | DFF | Macro backdrop |
| 10Y-2Y Spread | T10Y2Y | Yield curve context |

**API key handling:** Key is loaded from a `.env` file (`FRED_API_KEY=...`) which is `.gitignore`-d. A `.env.example` file is committed showing the expected variable name without the actual key.

### 2.3 Hardcoded Data (from public SEC filings & press releases)

**Hess Corporation Financials (FY2022-2023 from 10-K):**
- Revenue, EBITDA, D&A, CapEx, Net Income
- Balance sheet: total debt, cash, shares outstanding
- Production volumes (BOEPD), reserve data
- Guyana Stabroek Block: 30% interest, gross/net production
- **Note:** HES is delisted from Yahoo Finance (deal closed Oct 2024). All Hess data is sourced from SEC filings and hardcoded. Hess's implied trading multiples are derived from hardcoded financials + the pre-deal unaffected share price ($155.39).

**Chevron Standalone Financials (for accretion/dilution):**
- CVX EPS (FY2023), shares outstanding, projected growth
- Combined entity share count post-deal (CVX shares + 1.025 × HES shares converted)
- Synergy assumptions ($1B+ annual run-rate per Chevron guidance)

**Deal Terms:**
- Announced: October 23, 2023
- Structure: All-stock, 1.0250 CVX shares per HES share
- Equity value: ~$53B, Enterprise value: ~$60B
- Premium: ~10% to prior close ($155.39), implied ~$171/share
- Closed: October 1, 2024
- Exxon arbitration: ICC ruled in favor of Chevron/Hess (Sept 2024)

**Precedent Transactions (11 deals, 2020-2024):**

| Acquirer | Target | Date | EV ($B) | EV/EBITDA | Premium (1-day) |
|----------|--------|------|---------|-----------|-----------------|
| ExxonMobil | Pioneer Natural Resources | Oct 2023 | 64.5 | 6.2x | 18% |
| Chevron | Hess Corporation | Oct 2023 | 60.0 | 8.4x | 10% |
| ConocoPhillips | Marathon Oil | May 2024 | 22.5 | 5.8x | 15% |
| Diamondback | Endeavor Energy | Feb 2024 | 26.0 | 7.1x | N/A (private) |
| Occidental | CrownRock | Dec 2023 | 12.0 | 5.5x | N/A (private) |
| Chesapeake | Southwestern Energy | Jan 2024 | 7.4 | 5.2x | 12% |
| Chevron | PDC Energy | May 2023 | 7.6 | 4.8x | 11% |
| APA Corp | Callon Petroleum | Jan 2024 | 4.5 | 4.1x | 8% |
| Civitas | Tap Rock + Hibernia | Jun 2023 | 4.7 | 4.5x | N/A (private) |
| Devon Energy | Validus Energy | Jul 2023 | 1.8 | 4.0x | N/A (private) |
| ConocoPhillips | Concho Resources | Oct 2020 | 13.3 | 5.9x | 15% |

**Note on premiums:** Only 1-day premium is available for all public deals. The premium analysis chart uses 1-day premium only (not 30/90-day) to avoid data gaps. Private targets are excluded from the premium chart but included in the multiples analysis.

---

## 3. Notebook Structure

### Section 1: Executive Summary
**Content:**
- 3-4 bullet point deal overview
- Key valuation findings table (range from each method)
- Football field chart (the signature deliverable)
- "Bottom line" assessment paragraph

**Visualizations:**
- Football field chart — horizontal range bars showing valuation from comps, precedents, DCF, LBO, with Chevron's implied offer (~$171/share) marked as vertical dashed line. Expected price range: ~$130-$220/share.

### Section 2: Company & Industry Overview
**Content:**
- Hess Corporation profile (upstream E&P, key assets)
- Guyana Stabroek Block deep dive (why this asset drives the deal)
- Energy sector context: oil price trends, E&P consolidation wave
- Commentary on why Chevron wants Hess

**Visualizations:**
- WTI/Brent crude oil price chart (2020-present) with key events annotated (COVID crash, Ukraine invasion, OPEC+ cuts)
- Hess production growth vs peers (bar chart, hardcoded from 10-Ks)

### Section 3: Trading Comps Analysis
**Content:**
- Peer group selection rationale (10 E&P companies)
- Live financial data pull via yfinance with try/except fallback (see Section 9)
- Comps table: EV/EBITDA, EV/Revenue, P/E, EV/BOEPD
- Statistical summary (mean, median, 25th/75th percentile)
- Hess implied multiples derived from hardcoded financials + $155.39 unaffected price
- Implied valuation range for Hess based on peer median/mean multiples
- Note on EQT: included as gas-weighted peer for diversification context, with explicit note that its multiples diverge from oil-weighted peers

**Visualizations:**
- Comps scatter plot: EV/EBITDA vs production growth, bubble size = market cap, Hess position highlighted with star marker (from hardcoded data), regression line. Axis range: 3x-12x EV/EBITDA.
- Bar chart: peer EV/EBITDA multiples ranked, Hess implied range shaded

### Section 4: Precedent Transactions Analysis
**Content:**
- 11 E&P M&A deals (2020-2024)
- Transaction multiples: EV/EBITDA, premium to 1-day unaffected price
- Commentary on the 2023-2024 E&P M&A wave and consolidation drivers
- Implied valuation range for Hess

**Visualizations:**
- Premium analysis bar chart: 1-day premium for public deals only (7 deals with premium data)
- Precedent transaction multiples bar chart (EV/EBITDA by deal, sorted, all 11 deals)

### Section 5: DCF Valuation
**Content:**
- Revenue projection build (5-year)
  - Oil price deck: base/bull/bear scenarios derived from current WTI futures (~$70-80 base) with explicit assumptions stated
  - Production growth tied to Guyana ramp-up schedule
- EBITDA margin assumptions (based on Hess historical, adjusted for Guyana mix shift)
- Unlevered free cash flow derivation (waterfall: Revenue → Production Costs → Exploration → DD&A → G&A → Taxes → CapEx → UFCF)
- WACC calculation (CAPM: risk-free from ^TNX, beta from Damodaran E&P industry, ERP 5.5%)
- Terminal value (perpetuity growth method)
- Implied enterprise value → equity value → per share value
- Sensitivity analysis on WACC × terminal growth rate
- Monte Carlo simulation: 10,000 runs (fixed seed: np.random.seed(42)) randomizing oil price, production growth, margins, WACC, terminal growth
- Tornado analysis: which assumption swings valuation most

**Visualizations:**
- Waterfall chart: Revenue → Production Costs → Exploration Expense → DD&A → G&A → Taxes → CapEx → UFCF (E&P-specific line items, not generic R&D)
- Sensitivity heatmap: WACC (x) vs terminal growth (y), color-coded, base case highlighted
- Monte Carlo histogram: distribution of implied share prices, percentiles marked, Chevron offer (~$171) overlaid
- Tornado chart: horizontal bars showing valuation impact of each assumption ±1σ

### Section 6: LBO Analysis
**Content:**
- Hypothetical PE buyout of Hess at Chevron's offer price
- Explicit caveat: a $53B LBO is unrealistic at scale — this is a modeling exercise to demonstrate methodology. Debt pricing uses IG-adjacent spreads (not pure HY) reflecting the scale and asset quality
- Sources & uses of funds
- Debt schedule: Senior Secured (SOFR + 200bps), Senior Unsecured (SOFR + 350bps), Subordinated (8-9% fixed). Spreads informed by FRED credit data but adjusted for deal scale.
- 5-year financial projections
- Exit at year 5, range of exit multiples
- IRR and MOIC calculation
- Sensitivity on entry multiple × exit multiple

**Visualizations:**
- Sources & uses stacked bar chart
- IRR/MOIC sensitivity heatmap: entry EV/EBITDA (x) vs exit EV/EBITDA (y)
- Debt paydown schedule area chart (showing deleveraging over 5 years)

### Section 7: Accretion/Dilution & Synergy Analysis
**Content:**
- CVX standalone EPS (FY2023 actual, FY2024-2025 projected)
- Combined entity: new share count (CVX shares + HES shares × 1.025 exchange ratio)
- Pro forma combined EPS without synergies
- Synergy sensitivity: $0, $500M, $1B, $1.5B annual cost synergies (Chevron guided $1B+)
- Accretion/dilution at each synergy level
- Break-even synergy analysis: what level of synergies makes the deal accretive?
- Commentary on strategic rationale beyond EPS math (Guyana reserves, portfolio diversification)

**Visualizations:**
- Accretion/dilution bar chart: EPS impact at different synergy levels
- Break-even synergy waterfall

### Section 8: Deal Assessment & Recommendation
**Content:**
- Summary of implied valuation ranges from all methods
- Football field chart (comprehensive version with all 5 methodologies)
- Chevron's offer (~$171/share) vs. implied value: is Hess getting a fair price?
- Exxon arbitration risk discussion and its impact on deal certainty
- Final recommendation paragraph

**Visualizations:**
- Football field chart (final, comprehensive version)
- Valuation summary table

---

## 4. Visualization Standards

### Color Palette (IB Professional)
```python
IB_COLORS = {
    'dark_navy':    '#0B1F3F',
    'navy':         '#003366',
    'blue':         '#1B4F72',
    'mid_blue':     '#2874A6',
    'steel_blue':   '#5B9BD5',
    'light_blue':   '#A9CCE3',
    'pale_blue':    '#D6EAF8',
    'dark_gray':    '#2C3E50',
    'gray':         '#7F8C8D',
    'light_gray':   '#BDC3C7',
    'accent_red':   '#C0392B',
    'accent_green': '#27AE60',
    'accent_orange':'#E67E22',
}
```

### matplotlib Configuration
- DPI: 150 (crisp on GitHub and retina displays)
- Font: Segoe UI / Calibri / Arial (sans-serif)
- Spines: top and right removed
- Grid: very light gray (#E8E8E8), 0.5 linewidth, behind data
- Background: always white
- Annotations: value labels directly on data points
- Figure sizes: 12×6 for wide charts, 10×8 for heatmaps, 14×8 for football field

### Chart Rendering
- All charts rendered via matplotlib/seaborn (static PNG)
- No plotly (doesn't render on GitHub)
- Every chart has: title, axis labels with units, source annotation, legend only when needed

### GitHub Notebook Size Management
- Target notebook size under 1MB to ensure GitHub renders it without issues
- Use 100 DPI for embedded chart outputs (150 DPI for any saved standalone PNGs)
- If notebook exceeds 1MB, charts are saved to `output/` directory and referenced via markdown image links in the notebook

---

## 5. Dependencies

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

---

## 6. Commentary & Interview Defensibility

Every notebook section includes markdown cells with:
1. **What we're doing** — plain English explanation of the methodology
2. **Key assumptions** — why we chose these numbers, what would change the answer
3. **So what** — what the output means in the context of the Chevron/Hess deal
4. **Limitations** — intellectual honesty about what the model doesn't capture

This ensures the notebook author can walk through any section in an interview and explain both the methodology and the judgment behind it.

---

## 7. File Structure

```
IB/
├── hess_chevron_analysis.ipynb    # The main deliverable
├── requirements.txt                # Dependencies
├── .env.example                    # Shows expected env vars (FRED_API_KEY=your_key_here)
├── .env                            # Actual keys (gitignored)
├── .gitignore                      # .env, __pycache__, .ipynb_checkpoints, output/
├── README.md                       # GitHub landing page (professional, concise)
├── config/
│   ├── __init__.py
│   └── constants.py                # Hardcoded financials, deal terms, precedent txns
├── utils/
│   ├── __init__.py
│   ├── styling.py                  # IB color palette, matplotlib config, chart helpers
│   └── data_fetch.py              # yfinance and FRED data pull functions (with fallbacks)
├── output/                         # Generated chart PNGs (gitignored if embedded in notebook)
└── docs/
    └── superpowers/
        └── specs/
            └── 2026-03-19-hess-chevron-ib-toolkit-design.md
```

---

## 8. Success Criteria

1. A recruiter opens the GitHub repo, scrolls through the notebook, and sees polished charts + clear analysis without running any code
2. The author can explain every section, assumption, and chart in a 30-minute interview
3. The notebook uses real, current market data (peer comps refresh on each run)
4. The output looks like it belongs in a pitch book, not a homework assignment
5. The README gives immediate context: who built this, what it analyzes, what tools it uses

---

## 9. Error Handling & Resilience

### yfinance Fallback Strategy
yfinance scrapes Yahoo Finance and can break without warning. Every yfinance call is wrapped in try/except:
- If a peer ticker fails, skip it gracefully and note the exclusion in the comps table
- If all yfinance calls fail, fall back to hardcoded cache data (snapshot from last successful run) stored in `config/fallback_data.py`
- The notebook always renders, even if all external data sources are down

### Peer Ticker Validation
At notebook startup, validate all 10 peer tickers return data. Log which tickers succeeded/failed. Proceed with available data. Minimum viable peer set: 5 tickers.

### Execution Order
The notebook is designed for strict top-to-bottom execution. Each section's dependencies are explicitly stated in comments. Running cells out of order will produce clear error messages pointing to the required preceding section.

### Reproducibility
All random processes (Monte Carlo) use `np.random.seed(42)` for deterministic, reproducible output.
