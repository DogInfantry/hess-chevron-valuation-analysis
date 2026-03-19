"""
Hardcoded financial data for Chevron / Hess acquisition analysis.

All monetary values in millions of dollars (USD) unless explicitly noted.
Sources: Hess Corporation 10-K filings (FY2022, FY2023), Chevron 10-K (FY2023),
         public deal announcements, Damodaran datasets.

HES is delisted from Yahoo Finance; all Hess data is hardcoded here.
"""

# ---------------------------------------------------------------------------
# Hess Corporation — Income Statement & Balance Sheet Data
# ---------------------------------------------------------------------------
# Revenue FY2023 ~$10.5B, FY2022 ~$11.3B  (per Hess 10-K)
# Net Income both years ~$2.1B
# All figures in $M

HESS_FINANCIALS = {
    "FY2023": {
        "revenue": 10482,           # $M  — sales & other operating revenues
        "production_costs": 4521,   # $M  — production, transportation, operating
        "exploration_expense": 487, # $M  — exploration expense
        "dda": 2012,                # $M  — DD&A (depreciation, depletion, amortisation)
        "ga": 298,                  # $M  — G&A expense
        # EBITDA = Revenue - Production Costs - Exploration - G&A
        "ebitda": 10482 - 4521 - 487 - 298,   # = 5176
        # EBIT  = EBITDA - DD&A
        "ebit":  10482 - 4521 - 487 - 298 - 2012,  # = 3164
        "net_income": 2103,         # $M
        "total_debt": 8268,         # $M  — long-term debt + current portion
        "cash": 1715,               # $M  — cash & cash equivalents
        "shares_outstanding_M": 306.2,
        "capex": 3620,              # $M  — capital expenditures
        "production_kboepd": 391,   # thousand barrels of oil equivalent per day
    },
    "FY2022": {
        "revenue": 11314,
        "production_costs": 4480,
        "exploration_expense": 510,
        "dda": 1945,
        "ga": 285,
        "ebitda": 11314 - 4480 - 510 - 285,   # = 6039
        "ebit":  11314 - 4480 - 510 - 285 - 1945,  # = 4094
        "net_income": 2095,
        "total_debt": 8351,
        "cash": 1880,
        "shares_outstanding_M": 306.2,
        "capex": 2996,
        "production_kboepd": 356,
    },
}

# ---------------------------------------------------------------------------
# Hess unaffected share price (last close before deal announcement 2023-10-23)
# ---------------------------------------------------------------------------
HESS_UNAFFECTED_PRICE = 155.39  # USD per share

# ---------------------------------------------------------------------------
# Deal Terms — Chevron / Hess (announced 2023-10-23)
# ---------------------------------------------------------------------------
DEAL_TERMS = {
    "announcement_date": "2023-10-23",
    "exchange_ratio": 1.025,          # HES shares per CVX share received
    "implied_price": 171.0,           # approx implied value per HES share at announcement
    "equity_value_M": 53000,          # $M
    "enterprise_value_M": 60000,      # $M  (equity + net debt)
    "premium_1day_pct": 10.0,         # % premium to HES unaffected price
    "close_date": "2024-10-01",
    "structure": "All-stock",
    "acquirer": "Chevron Corporation",
    "target": "Hess Corporation",
}

# ---------------------------------------------------------------------------
# Chevron Corporation — Key Financial Data (FY2023)
# ---------------------------------------------------------------------------
CVX_FINANCIALS = {
    "eps_fy2023": 13.17,              # USD per diluted share
    "shares_outstanding_M": 1930,     # millions of shares
    "net_income_M": 25400,            # $M  (approximate)
    "projected_eps_growth": 0.03,     # 3 % annual growth assumption
}

# ---------------------------------------------------------------------------
# Precedent M&A Transactions — Oil & Gas (E&P)
# ---------------------------------------------------------------------------
# ev_billions: enterprise value in $ billions
# ev_ebitda:   EV / EBITDA multiple (x)
# premium_1day: 1-day premium to unaffected price (%); None for private targets

PRECEDENT_TRANSACTIONS = [
    {
        "acquirer": "ExxonMobil",
        "target": "Pioneer Natural Resources",
        "date": "Oct 2023",
        "ev_billions": 64.5,
        "ev_ebitda": 6.2,
        "premium_1day": 18.0,
    },
    {
        "acquirer": "Chevron",
        "target": "Hess Corporation",
        "date": "Oct 2023",
        "ev_billions": 60.0,
        "ev_ebitda": 8.4,
        "premium_1day": 10.0,
    },
    {
        "acquirer": "ConocoPhillips",
        "target": "Marathon Oil",
        "date": "May 2024",
        "ev_billions": 22.5,
        "ev_ebitda": 5.8,
        "premium_1day": 15.0,
    },
    {
        "acquirer": "Diamondback Energy",
        "target": "Endeavor Energy",
        "date": "Feb 2024",
        "ev_billions": 26.0,
        "ev_ebitda": 7.1,
        "premium_1day": None,   # private target
    },
    {
        "acquirer": "Occidental Petroleum",
        "target": "CrownRock",
        "date": "Dec 2023",
        "ev_billions": 12.0,
        "ev_ebitda": 5.5,
        "premium_1day": None,   # private target
    },
    {
        "acquirer": "Chesapeake Energy",
        "target": "Southwestern Energy",
        "date": "Jan 2024",
        "ev_billions": 7.4,
        "ev_ebitda": 5.2,
        "premium_1day": 12.0,
    },
    {
        "acquirer": "Chevron",
        "target": "PDC Energy",
        "date": "May 2023",
        "ev_billions": 7.6,
        "ev_ebitda": 4.8,
        "premium_1day": 11.0,
    },
    {
        "acquirer": "APA Corp",
        "target": "Callon Petroleum",
        "date": "Jan 2024",
        "ev_billions": 4.5,
        "ev_ebitda": 4.1,
        "premium_1day": 8.0,
    },
    {
        "acquirer": "Civitas Resources",
        "target": "Tap Rock + Hibernia",
        "date": "Jun 2023",
        "ev_billions": 4.7,
        "ev_ebitda": 4.5,
        "premium_1day": None,   # private target
    },
    {
        "acquirer": "Devon Energy",
        "target": "Validus Energy",
        "date": "Jul 2023",
        "ev_billions": 1.8,
        "ev_ebitda": 4.0,
        "premium_1day": None,   # private target
    },
    {
        "acquirer": "ConocoPhillips",
        "target": "Concho Resources",
        "date": "Oct 2020",
        "ev_billions": 13.3,
        "ev_ebitda": 5.9,
        "premium_1day": 15.0,
    },
]

# ---------------------------------------------------------------------------
# Peer Universe (E&P / Integrated)
# ---------------------------------------------------------------------------
PEER_TICKERS = ["CVX", "XOM", "COP", "EOG", "DVN", "FANG", "OXY", "APA", "CTRA", "EQT"]

# ---------------------------------------------------------------------------
# Hess Production History (KBOEPD)
# ---------------------------------------------------------------------------
HESS_PRODUCTION_HISTORY = {
    2019: 273,
    2020: 321,
    2021: 315,
    2022: 356,
    2023: 391,
}

# ---------------------------------------------------------------------------
# Damodaran / CAPM Parameters (E&P sector)
# ---------------------------------------------------------------------------
DAMODARAN_EP = {
    "unlevered_beta": 1.10,
    "equity_risk_premium": 0.055,   # 5.5 % ERP
    "debt_to_equity": 0.35,
    "cost_of_debt": 0.045,          # 4.5 % — Hess blended cost of debt
}

# ---------------------------------------------------------------------------
# Synergy Scenarios ($M)
# ---------------------------------------------------------------------------
SYNERGY_SCENARIOS = [0, 500, 1000, 1500]  # $M annual run-rate synergies

# ---------------------------------------------------------------------------
# Peer 2023 Production (KBOEPD — approximate)
# ---------------------------------------------------------------------------
PEER_PRODUCTION_KBOEPD = {
    "CVX": 3100,
    "XOM": 3700,
    "COP": 1700,
    "EOG": 950,
    "DVN": 660,
    "FANG": 460,
    "OXY": 1200,
    "APA": 420,
    "CTRA": 640,
    "EQT": 520,
}
