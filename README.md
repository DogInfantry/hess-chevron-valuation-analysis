<div align="center">

# 🛢️ Chevron × Hess — $53B M&A Valuation Analysis

**Full investment banking-style valuation and deal analysis of Chevron's acquisition of Hess Corporation — six methodologies, Monte Carlo simulation, LBO, and accretion/dilution modeling, built entirely in Python.**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Data](https://img.shields.io/badge/Live_Data-yfinance_%7C_FRED-0077B5?style=for-the-badge)]()

> Replicates the analytical framework of a bulge-bracket M&A pitch book — applied to one of the most strategically significant energy deals of 2023.
> Announced October 2023 · All-stock deal · $171/share offer.

[📊 Methodologies](#-valuation-methodologies) · [🔍 Key Findings](#-key-findings) · [📈 Visualizations](#-visualizations) · [📄 Reports](#-downloadable-reports) · [🚀 Quick Start](#-quick-start)

</div>

---

## ⚡ Deal at a Glance

| Parameter | Detail |
|-----------|--------|
| **Deal** | Chevron Corporation acquires Hess Corporation |
| **Announced** | October 2023 |
| **Deal Value** | $53 billion (all-stock) |
| **Offer Price** | $171 per share |
| **Strategic Rationale** | Guyana deepwater reserves (Stabroek Block) + Bakken consolidation |
| **Accretion / Dilution** | 6.9% dilutive to CVX EPS at deal close |
| **Synergy Breakeven** | ~$2.6B in annual synergies required |
| **Analysis Scope** | 49-cell notebook · 8 sections · 15+ IB-grade charts |

---

## 🔍 Key Findings

> **Verdict: A long-duration growth bet on Guyana, not a near-term earnings story.**

- Chevron’s **$171/share offer** implies a modest ~10% premium to Hess’s unaffected price — within historical upstream M&A range but well below precedent mega-deal premiums
- **Cash-flow methodologies (DCF, LBO)** value Hess significantly *below* the offer price — quantifying the **“Guyana premium”** embedded for undeveloped offshore reserves in the Stabroek Block
- **Market-based methodologies** (trading comps, precedent transactions) bracket the deal price; the implied premium range ($168–$183) nearly matches the offer, suggesting the market was already pricing in a takeout
- The deal is **6.9% dilutive to CVX EPS** at close, requiring ~**$2.6B in annual synergies** to break even on an accretion basis — confirming this is a reserve acquisition, not a margin play

---

## 📊 Valuation Methodologies

Six independent methodologies implemented end-to-end in Python:

| # | Methodology | Key Output |
|---|-------------|------------|
| 1 | **Trading Comparable Companies** | EV/EBITDA, EV/Production, P/E across E&P peers (COP, DVN, MRO, APA, OVV) |
| 2 | **Precedent Transactions** | Historical upstream M&A multiples with control premium analysis |
| 3 | **DCF with Monte Carlo** | 5-year UFCF projection, WACC discounting, 10,000-path probabilistic output |
| 4 | **Leveraged Buyout (LBO)** | Sponsor return framework implying floor valuation |
| 5 | **Accretion / Dilution & Synergy Analysis** | Pro forma CVX EPS impact + breakeven synergy threshold |
| 6 | **Premium Analysis** | Implied premium vs. unaffected price: 1-day, 1-week, 52-week benchmarks |

All six outputs are aggregated into a **Football Field chart** showing the full valuation range vs. the $171 deal price.

---

## 📈 Visualizations

15+ professional-grade charts styled after IB deliverables:

| Chart | What It Reveals |
|-------|-----------------|
| **Football Field Valuation** | Full range across all 6 methods vs. deal price — where the Guyana premium sits |
| **DCF Sensitivity Heatmap** | WACC vs. terminal growth rate — how sensitive implied price is to macro assumptions |
| **Monte Carlo Distribution** | 10,000-path probability distribution of DCF outputs under parameter uncertainty |
| **UFCF Waterfall Bridge** | EBITDA-to-FCF conversion showing capex and working capital drag |
| **Tornado Chart** | Ranked single-variable sensitivity — which DCF input drives valuation most |
| **Trading Comps Scatter** | EV/EBITDA vs. EV/Production for peer E&P universe |
| **Precedent Transactions** | Historical deal multiples with Hess deal highlighted |
| **Accretion / Dilution** | CVX EPS impact across synergy scenarios — where breakeven lies |
| **WTI Oil Price Chart** | Crude annotated with deal milestones and macro events |
| **Sector Performance** | Hess vs. CVX vs. XLE since deal announcement |

---

## 📄 Downloadable Reports

Three full-length research documents included in the repository:

| Report | Description |
|--------|-------------|
| [`Chevron_Hess_$53B_Deal_Analysis.pdf`](./Chevron_Hess_$53B_Deal_Analysis.pdf) | Full deal analysis — valuation, synergies, strategic rationale |
| [`Chevron_Hess_Mega_Deal_White_Paper.pdf`](./Chevron_Hess_Mega_Deal_White_Paper.pdf) | Executive white paper — deal thesis and market context |
| [`Chev_Hess.pdf`](./Chev_Hess.pdf) | Supplementary analysis |

---

## 🗂️ Repository Structure

```
hess-chevron-valuation-analysis/
│
├── 📓 hess_chevron_analysis.ipynb     # Main notebook — 49 cells, 8 sections
├── 📁 config/
│   ├── constants.py                   # Hardcoded financials, deal terms, precedent comps
│   └── fallback_data.py               # Cached peer data for offline execution
├── 📁 utils/
│   ├── styling.py                     # IB-grade chart functions (11 chart types)
│   └── data_fetch.py                  # yfinance / FRED wrappers with fallback logic
├── 📁 docs/                           # Supporting documentation
├── 📄 Chevron_Hess_$53B_Deal_Analysis.pdf
├── 📄 Chevron_Hess_Mega_Deal_White_Paper.pdf
├── 📄 Chev_Hess.pdf
├── requirements.txt
└── .env.example                       # FRED API key template
```

---

## 🗃️ Data Sources

| Source | API Key | Provides |
|--------|---------|----------|
| [Yahoo Finance (yfinance)](https://pypi.org/project/yfinance/) | ❌ Not required | Peer trading data, WTI crude, XLE sector ETF |
| [FRED](https://fred.stlouisfed.org/) | ✅ Free key | IG credit spreads, Henry Hub gas, Fed Funds rate |
| SEC EDGAR (10-K filings) | ❌ Not required | Hess historical financials FY2020–FY2022 |
| [Damodaran Online](https://pages.stern.nyu.edu/~adamodar/) | ❌ Not required | Beta estimates, ERP, cost of capital inputs |

> **FRED API key is free** — get one at [fred.stlouisfed.org](https://fred.stlouisfed.org/docs/api/api_key.html). The notebook runs fully without it using cached fallback data.

---

## 🚀 Quick Start

```bash
git clone https://github.com/DogInfantry/hess-chevron-valuation-analysis.git
cd hess-chevron-valuation-analysis
pip install -r requirements.txt
cp .env.example .env          # Add your FRED API key (optional)
jupyter notebook hess_chevron_analysis.ipynb
```

---

## 🛠️ Technology Stack

```
Modeling      │ pandas · numpy · scipy
Visualization │ matplotlib · seaborn
Live Data     │ yfinance · fredapi
Environment   │ python-dotenv
Runtime       │ Python 3.8+ · Jupyter Notebook
```

---

## ⚠️ Disclaimer

This analysis is for educational and demonstrative purposes only. It does not constitute investment advice, a solicitation, or a recommendation to buy or sell any security. All data is sourced from public filings and market data providers.

---

<div align="center">

**Deal Announced:** October 2023 &nbsp;·&nbsp; **Deal Value:** $53B &nbsp;·&nbsp; **Status:** ✅ Complete

*Built to IB pitch book standards · Python-native · No paid data required*

</div>
