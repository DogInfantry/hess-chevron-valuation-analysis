# Hess Corporation: Investment Banking Valuation & M&A Analysis
### Chevron's $53B Acquisition - A Comprehensive Analytical Framework

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Overview

This project presents a full investment banking-style analysis of Chevron Corporation's $53 billion acquisition of Hess Corporation, announced in October 2023. The notebook replicates the analytical framework used by M&A advisory teams;covering six distinct valuation methodologies, deal structuring analysis, and accretion/dilution modeling — implemented entirely in Python with live market data.

The analysis spans 49 cells across 8 structured sections, generating 15+ professional-grade visualizations styled after actual IB deliverables. Data is sourced dynamically from Yahoo Finance and FRED at runtime, with hardcoded fallbacks to ensure reproducibility. The goal is to demonstrate how Python can systematically replicate the analytical rigor of a bulge-bracket M&A pitch book.

---

## Key Visualizations

| Chart | Purpose |
|---|---|
| Football Field Valuation | Summary range across all 6 methodologies vs. deal price |
| DCF Sensitivity Heatmap | WACC vs. terminal growth rate sensitivity on implied share price |
| Monte Carlo Simulation | 10,000-path distribution of DCF outputs under parameter uncertainty |
| UFCF Waterfall Bridge | EBITDA-to-free-cash-flow bridge for the projection period |
| Tornado Sensitivity Chart | Ranked impact of each DCF input on valuation |
| Trading Comps Scatter | EV/EBITDA vs. EV/Production for peer E&P companies |
| Precedent Transactions | Historical M&A deal multiples with Hess deal highlighted |
| Accretion/Dilution Analysis | CVX EPS impact across synergy scenarios |
| Oil Price Chart | WTI crude with annotated deal milestones and macro events |
| Sector Performance | Hess vs. CVX vs. XLE since deal announcement |

---

## Methodologies Covered

1. **Trading Comparable Companies** - EV/EBITDA, EV/Production, P/E multiples for E&P peers (COP, DVN, MRO, APA, OVV)
2. **Precedent Transactions** - Historical upstream M&A comps with control premium analysis
3. **Discounted Cash Flow (DCF) with Monte Carlo** - 5-year UFCF projection, WACC-based discounting, 10,000-simulation probabilistic output
4. **Leveraged Buyout (LBO)** - Sponsor return framework implying floor valuation
5. **Accretion/Dilution & Synergy Analysis** - Pro forma EPS impact and breakeven synergy threshold for CVX
6. **Premium Analysis** - Implied premium vs. unaffected price across 1-day, 1-week, and 52-week benchmarks

---

## Data Sources

- **Yahoo Finance (yfinance)** - Live peer trading data, WTI crude prices, sector ETF (XLE) performance
- **FRED (Federal Reserve Economic Data)** - Investment grade credit spreads, Henry Hub natural gas, fed funds rate
- **SEC EDGAR (10-K filings)** - Hess historical financial statements (FY2020-FY2022, hardcoded from filings)
- **Damodaran Online** - Beta estimates, equity risk premium, and cost of capital inputs

---

## Tech Stack

- **Python 3.8+**, Jupyter Notebook
- **pandas**, **numpy**, **scipy** - financial modeling and statistical analysis
- **matplotlib**, **seaborn** - visualization engine
- **yfinance**, **fredapi** - live market and economic data sourcing
- **python-dotenv** - API key configuration management

---

## Project Structure

```
├── hess_chevron_analysis.ipynb   # Main analysis notebook (49 cells, 8 sections)
├── config/
│   ├── constants.py              # Hardcoded financials, deal terms, precedent transactions
│   └── fallback_data.py          # Cached peer data for offline execution
├── utils/
│   ├── styling.py                # IB-grade chart functions (11 chart types)
│   └── data_fetch.py             # yfinance/FRED wrappers with fallback logic
├── output/                       # Generated charts (PNG)
├── requirements.txt
└── .env.example                  # FRED API key template
```

---

## Setup & Running

```bash
git clone <repo-url>
cd IB
pip install -r requirements.txt
cp .env.example .env  # Add your FRED API key
jupyter notebook hess_chevron_analysis.ipynb
```

A FRED API key is free and available at [fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html). The notebook runs without it using cached fallback data.

---

## Key Findings

- Chevron's **$171/share offer** implies a ~10% premium to Hess's unaffected price, within the historical range for upstream M&A but modest relative to precedent mega-deals
- **Cash-flow methodologies (DCF, LBO)** value Hess significantly below the offer price - quantifying the "Guyana premium" embedded in the deal for undeveloped offshore reserves
- **Market-based methodologies** (trading comps, precedent transactions) bracket the deal price, with the premium implied range ($168–$183) nearly matching the offer, suggesting the market was pricing in a takeout
- The deal is **6.9% dilutive to CVX EPS**, requiring approximately **$2.6B in annual synergies** to break even on an accretion basis confirming this is a long duration growth bet on Guyana production rather than a near term earnings story

---

## About

This project was built as a demonstration of investment banking analytical skills implemented in Python. It reflects the frameworks taught in IB training programs and used by advisory teams on large-cap M&A transactions ;applied to one of the most strategically significant energy deals of 2023.

---

## Disclaimer

This analysis is for educational and demonstrative purposes only. It does not constitute investment advice, a solicitation, or a recommendation to buy or sell any security. All data is sourced from public filings and market data providers.
