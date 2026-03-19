"""
Data fetching utilities with fallback support.

All yfinance calls are wrapped in try/except because yfinance scrapes Yahoo Finance
and can break without warning. If live data is unavailable, the module falls back
to cached data in config/fallback_data.py so the notebook remains functional.
"""

import os
import sys
import warnings
import pandas as pd

# Suppress noisy yfinance / urllib warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*auto_adjust.*")

try:
    import yfinance as yf
    _YF_AVAILABLE = True
except ImportError:
    _YF_AVAILABLE = False
    print("[data_fetch] WARNING: yfinance not installed — live data unavailable.")

try:
    from fredapi import Fred
    _FRED_AVAILABLE = True
except ImportError:
    _FRED_AVAILABLE = False
    print("[data_fetch] WARNING: fredapi not installed — FRED data unavailable.")


# ---------------------------------------------------------------------------
# Validate tickers
# ---------------------------------------------------------------------------

def validate_tickers(tickers: list) -> tuple:
    """
    Quick validation: tries yf.Ticker(t).info.get('shortName') for each ticker.

    Returns
    -------
    (valid_tickers, failed_tickers)
    """
    if not _YF_AVAILABLE:
        print("[validate_tickers] yfinance unavailable — returning all tickers as unvalidated.")
        return list(tickers), []

    valid = []
    failed = []
    for t in tickers:
        try:
            name = yf.Ticker(t).info.get("shortName")
            if name:
                valid.append(t)
            else:
                failed.append(t)
        except Exception as e:
            failed.append(t)

    return valid, failed


# ---------------------------------------------------------------------------
# Peer comparable companies
# ---------------------------------------------------------------------------

def fetch_peer_comps(tickers: list) -> pd.DataFrame:
    """
    Fetch key trading multiples for a list of E&P / integrated oil tickers.

    Extracts: ticker, shortName, marketCap, enterpriseValue, enterpriseToEbitda,
    enterpriseToRevenue, trailingPE, forwardPE, sector.

    Falls back to config.fallback_data.FALLBACK_PEER_DATA when fewer than 5
    tickers return data successfully.
    """
    _FIELDS = [
        "shortName", "marketCap", "enterpriseValue",
        "enterpriseToEbitda", "enterpriseToRevenue",
        "trailingPE", "forwardPE", "sector",
    ]

    if not _YF_AVAILABLE:
        print("[fetch_peer_comps] yfinance unavailable — loading fallback data.")
        return _load_fallback_peers()

    rows = []
    skipped = []

    for t in tickers:
        try:
            info = yf.Ticker(t).info
            row = {"ticker": t}
            for field in _FIELDS:
                row[field] = info.get(field)
            # Only include if we got at least the company name
            if row.get("shortName"):
                rows.append(row)
            else:
                skipped.append(t)
        except Exception as e:
            skipped.append(t)

    fetched = len(rows)
    total = len(tickers)
    skip_str = f" (skipped: {', '.join(skipped)})" if skipped else ""
    print(f"[fetch_peer_comps] Fetched {fetched}/{total} peers{skip_str}")

    if fetched < 5:
        print("[fetch_peer_comps] Fewer than 5 peers fetched — loading fallback data.")
        return _load_fallback_peers()

    df = pd.DataFrame(rows)
    df = df.set_index("ticker") if "ticker" in df.columns else df
    return df


def _load_fallback_peers() -> pd.DataFrame:
    """Load FALLBACK_PEER_DATA from config and return as DataFrame."""
    try:
        from config import fallback_data
        data = fallback_data.FALLBACK_PEER_DATA
        if not data:
            print("[fetch_peer_comps] Fallback cache is empty.")
            return pd.DataFrame()
        df = pd.DataFrame.from_dict(data, orient="index")
        df.index.name = "ticker"
        print(f"[fetch_peer_comps] Loaded {len(df)} rows from fallback cache.")
        return df
    except Exception as e:
        print(f"[fetch_peer_comps] Could not load fallback data: {e}")
        return pd.DataFrame()


# ---------------------------------------------------------------------------
# Commodity prices & macro series
# ---------------------------------------------------------------------------

_COMMODITY_MAP = {
    "WTI":          "CL=F",
    "Brent":        "BZ=F",
    "NatGas":       "NG=F",
    "Treasury_10Y": "^TNX",
    "XLE":          "XLE",
    "XOP":          "XOP",
    "SP500":        "^GSPC",
}


def fetch_commodity_prices(start: str = "2020-01-01") -> dict:
    """
    Download price history for WTI, Brent, NatGas, 10Y yield, XLE, XOP, S&P 500.

    Parameters
    ----------
    start : str
        Start date in 'YYYY-MM-DD' format (default '2020-01-01').

    Returns
    -------
    dict of {descriptive_name: pd.DataFrame}
        Keys: 'WTI', 'Brent', 'NatGas', 'Treasury_10Y', 'XLE', 'XOP', 'SP500'
        Only keys for which data was successfully downloaded are included.
    """
    if not _YF_AVAILABLE:
        print("[fetch_commodity_prices] yfinance unavailable — returning empty dict.")
        return {}

    result = {}
    for name, symbol in _COMMODITY_MAP.items():
        try:
            df = yf.download(symbol, start=start, progress=False, auto_adjust=True)
            if df is not None and not df.empty:
                result[name] = df
            else:
                print(f"[fetch_commodity_prices] No data for {name} ({symbol})")
        except Exception as e:
            print(f"[fetch_commodity_prices] Failed {name} ({symbol}): {e}")

    fetched_names = list(result.keys())
    print(f"[fetch_commodity_prices] Fetched: {', '.join(fetched_names) if fetched_names else 'none'}")
    return result


# ---------------------------------------------------------------------------
# FRED macroeconomic data
# ---------------------------------------------------------------------------

_FRED_SERIES = {
    "BAMLH0A0HYM2": "HY_OAS",          # BofA HY OAS spread
    "DHHNGSP":      "HH_NatGas",        # Henry Hub natural gas spot
    "DFF":          "FedFunds",         # Effective federal funds rate
    "T10Y2Y":       "Yield_Curve_10Y2Y",# 10Y–2Y Treasury spread
}


def fetch_fred_data(api_key: str) -> dict:
    """
    Pull macroeconomic series from FRED.

    Parameters
    ----------
    api_key : str or None
        FRED API key.  If None or unavailable, returns empty dict.

    Returns
    -------
    dict of {series_code: pd.Series}
        Keys are raw FRED codes (e.g. 'BAMLH0A0HYM2').
        Returns empty dict on total failure.
    """
    if not _FRED_AVAILABLE:
        print("[fetch_fred_data] fredapi not installed — returning empty dict.")
        return {}

    if not api_key:
        print("[fetch_fred_data] WARNING: No FRED API key provided — returning empty dict.")
        return {}

    result = {}
    try:
        fred = Fred(api_key=api_key)
    except Exception as e:
        print(f"[fetch_fred_data] Failed to initialise Fred client: {e}")
        return {}

    for code in _FRED_SERIES:
        try:
            series = fred.get_series(code)
            result[code] = series
        except Exception as e:
            print(f"[fetch_fred_data] Failed to fetch {code}: {e}")

    if result:
        print(f"[fetch_fred_data] Fetched series: {', '.join(result.keys())}")
    else:
        print("[fetch_fred_data] No FRED series fetched.")

    return result


# ---------------------------------------------------------------------------
# Save fallback cache
# ---------------------------------------------------------------------------

def save_fallback_cache(peer_df: pd.DataFrame) -> None:
    """
    Persist peer_df as a Python dict literal into config/fallback_data.py
    so it can be imported as FALLBACK_PEER_DATA on subsequent runs.

    Only call this after a successful full (or near-full) pull.
    """
    if peer_df is None or peer_df.empty:
        print("[save_fallback_cache] Empty DataFrame — nothing to save.")
        return

    # Build the dict representation with ticker as key
    data = peer_df.copy()
    if data.index.name == "ticker":
        records = data.to_dict(orient="index")
    else:
        records = data.to_dict(orient="index")

    # Serialise: replace NaN / None cleanly for Python literal
    cleaned = {}
    for ticker, fields in records.items():
        cleaned[ticker] = {
            k: (None if (v != v or v is None) else v)   # NaN check: v != v
            for k, v in fields.items()
        }

    # Format as Python source
    lines = [
        '"""',
        "Fallback peer data cache.",
        "Populated from last successful yfinance pull.",
        "Used when yfinance is unavailable.",
        '"""',
        "",
        "FALLBACK_PEER_DATA = {",
    ]
    for ticker, fields in cleaned.items():
        lines.append(f"    {ticker!r}: {{")
        for k, v in fields.items():
            lines.append(f"        {k!r}: {v!r},")
        lines.append("    },")
    lines.append("}")
    lines.append("")

    # Resolve config directory relative to this file's location
    this_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(this_dir, "..", "config")
    out_path = os.path.normpath(os.path.join(config_dir, "fallback_data.py"))

    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))

    print(f"[save_fallback_cache] Saved {len(cleaned)} tickers to {out_path}")
