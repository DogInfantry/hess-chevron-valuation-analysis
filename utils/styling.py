"""
IB Styling system and chart helper functions.
Produces Goldman Sachs / Morgan Stanley pitch-book-quality charts:
navy palette, clean spines, white backgrounds, sans-serif fonts,
value annotations on every chart.
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------

IB_COLORS = {
    'dark_navy':     '#0B1F3F',
    'navy':          '#003366',
    'blue':          '#1B4F72',
    'mid_blue':      '#2874A6',
    'steel_blue':    '#5B9BD5',
    'light_blue':    '#A9CCE3',
    'pale_blue':     '#D6EAF8',
    'dark_gray':     '#2C3E50',
    'gray':          '#7F8C8D',
    'light_gray':    '#BDC3C7',
    'accent_red':    '#C0392B',
    'accent_green':  '#27AE60',
    'accent_orange': '#E67E22',
}

# Ordered list of IB colour shades used for multi-series charts
_COLOR_CYCLE = [
    IB_COLORS['navy'],
    IB_COLORS['steel_blue'],
    IB_COLORS['mid_blue'],
    IB_COLORS['blue'],
    IB_COLORS['light_blue'],
    IB_COLORS['accent_orange'],
    IB_COLORS['accent_green'],
    IB_COLORS['accent_red'],
]

# ---------------------------------------------------------------------------
# Global style setup
# ---------------------------------------------------------------------------

def setup_ib_style():
    """Apply IB pitch-book rcParams to the current matplotlib session."""
    matplotlib.rcParams.update({
        # Resolution
        'figure.dpi':         100,
        'savefig.dpi':        150,
        # Font
        'font.family':        'sans-serif',
        'font.sans-serif':    ['Segoe UI', 'Calibri', 'Arial', 'DejaVu Sans'],
        # Spines
        'axes.spines.top':    False,
        'axes.spines.right':  False,
        # Grid
        'axes.grid':          True,
        'grid.color':         '#E8E8E8',
        'grid.linewidth':     0.5,
        'axes.axisbelow':     True,
        # Backgrounds
        'figure.facecolor':   'white',
        'axes.facecolor':     'white',
        # Title
        'axes.titleweight':   'bold',
        'axes.titlesize':     14,
        # Save
        'savefig.bbox':       'tight',
    })


# ---------------------------------------------------------------------------
# 1. Bar chart
# ---------------------------------------------------------------------------

def plot_bar_chart(labels, values, title, xlabel, ylabel,
                   highlight_idx=None, horizontal=False):
    """
    Simple bar chart with value annotations.

    Parameters
    ----------
    labels        : list of str
    values        : list of float
    title         : str
    xlabel        : str
    ylabel        : str
    highlight_idx : int or None  — bar index to colour accent_red
    horizontal    : bool         — if True draw horizontal bars
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    colors = [
        IB_COLORS['accent_red'] if i == highlight_idx else IB_COLORS['navy']
        for i in range(len(labels))
    ]

    if horizontal:
        bars = ax.barh(labels, values, color=colors)
        for bar, val in zip(bars, values):
            ax.text(
                bar.get_width() + max(values) * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f'{val:.1f}x',
                va='center', fontsize=10, color=IB_COLORS['dark_gray'],
            )
        ax.set_xlabel(ylabel)
        ax.set_ylabel(xlabel)
    else:
        bars = ax.bar(labels, values, color=colors, width=0.6)
        for bar, val in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(values) * 0.01,
                f'{val:.1f}x',
                ha='center', va='bottom', fontsize=10,
                color=IB_COLORS['dark_gray'],
            )
        ax.set_xlabel(xlabel, labelpad=8)
        ax.set_ylabel(ylabel, labelpad=8)

    ax.set_title(title, pad=14)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 2. Grouped bar chart
# ---------------------------------------------------------------------------

def plot_grouped_bar(labels, group_data: dict, title, ylabel):
    """
    Side-by-side grouped bar chart.

    Parameters
    ----------
    labels     : list of str  — x-axis categories
    group_data : dict         — {group_name: [values per label]}
    title      : str
    ylabel     : str
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    groups = list(group_data.keys())
    n_groups = len(groups)
    n_labels = len(labels)
    x = np.arange(n_labels)
    width = 0.8 / n_groups

    for gi, (group, vals) in enumerate(group_data.items()):
        offset = (gi - n_groups / 2 + 0.5) * width
        color = _COLOR_CYCLE[gi % len(_COLOR_CYCLE)]
        bars = ax.bar(x + offset, vals, width=width * 0.9,
                      label=group, color=color)
        for bar, val in zip(bars, vals):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + max(max(v) for v in group_data.values()) * 0.01,
                f'{val:.1f}',
                ha='center', va='bottom', fontsize=8,
                color=IB_COLORS['dark_gray'],
            )

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel(ylabel, labelpad=8)
    ax.set_title(title, pad=14)
    ax.legend(frameon=False)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 3. Area chart
# ---------------------------------------------------------------------------

def plot_area_chart(df, title, ylabel):
    """
    Stacked area chart from a DataFrame (columns = series, index = x-axis).

    Parameters
    ----------
    df    : pd.DataFrame
    title : str
    ylabel: str
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    colors = _COLOR_CYCLE[:len(df.columns)]
    ax.stackplot(df.index, df.T, labels=df.columns, colors=colors, alpha=0.85)

    ax.set_title(title, pad=14)
    ax.set_ylabel(ylabel, labelpad=8)
    ax.legend(loc='upper left', frameon=False)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 4. Oil price chart
# ---------------------------------------------------------------------------

def plot_oil_price_chart(wti_series, brent_series, events: dict, title):
    """
    Dual-line oil price chart with annotated events.

    Parameters
    ----------
    wti_series   : pd.Series (datetime index, float values)
    brent_series : pd.Series (datetime index, float values)
    events       : dict  {'YYYY-MM-DD': 'Label', ...}
    title        : str
    """
    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(wti_series.index, wti_series.values,
            color=IB_COLORS['navy'], linewidth=1.8, label='WTI Crude')
    ax.plot(brent_series.index, brent_series.values,
            color=IB_COLORS['steel_blue'], linewidth=1.8,
            linestyle='--', label='Brent Crude')

    # Determine y range for annotations
    all_vals = list(wti_series.values) + list(brent_series.values)
    y_range = max(all_vals) - min(all_vals)

    for i, (date_str, label) in enumerate(events.items()):
        event_date = pd.to_datetime(date_str)
        # Find closest WTI value
        idx = wti_series.index.get_indexer([event_date], method='nearest')[0]
        y_val = float(wti_series.iloc[idx])
        y_offset = y_range * 0.25 * (1 if i % 2 == 0 else -1)

        ax.annotate(
            label,
            xy=(event_date, y_val),
            xytext=(event_date, y_val + y_offset),
            fontsize=8,
            ha='center',
            color=IB_COLORS['dark_gray'],
            arrowprops=dict(arrowstyle='->', color=IB_COLORS['gray'],
                            lw=1.0),
            bbox=dict(boxstyle='round,pad=0.3', fc='white',
                      ec=IB_COLORS['light_gray'], alpha=0.9),
        )

    ax.set_title(title, pad=14)
    ax.set_ylabel('Price ($/bbl)', labelpad=8)
    ax.legend(frameon=False)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 5. Comps table styler
# ---------------------------------------------------------------------------

def format_comps_table(df) -> 'pd.io.formats.style.Styler':
    """
    Apply IB pitch-book styling to a comparables DataFrame.

    Returns a pandas Styler with:
    - Alternating white / pale_blue rows
    - Bold header
    - Automatic number formatting ($, x, %)
    """
    def _row_colors(row):
        bg = IB_COLORS['pale_blue'] if row.name % 2 == 1 else 'white'
        return [f'background-color: {bg}' for _ in row]

    def _fmt_cell(val):
        if isinstance(val, float):
            if abs(val) > 100:
                return f'${val:,.0f}'
            elif abs(val) < 20:
                return f'{val:.1f}x'
            else:
                return f'{val:.1f}%'
        return val

    styler = (
        df.style
        .apply(_row_colors, axis=1)
        .format(_fmt_cell)
        .set_table_styles([
            {'selector': 'th',
             'props': [('background-color', IB_COLORS['navy']),
                       ('color', 'white'),
                       ('font-weight', 'bold'),
                       ('text-align', 'center')]},
            {'selector': 'td',
             'props': [('text-align', 'right'),
                       ('padding', '4px 10px')]},
        ])
    )
    return styler


# ---------------------------------------------------------------------------
# 6. Football field
# ---------------------------------------------------------------------------

def plot_football_field(valuations: dict, offer_price: float, title: str):
    """
    Horizontal bar football-field valuation chart.

    Parameters
    ----------
    valuations  : dict  {'Method': (low, mid, high), ...}
    offer_price : float
    title       : str
    """
    fig, ax = plt.subplots(figsize=(14, 8))

    methods = list(valuations.keys())
    for i, (method, (lo, mid, hi)) in enumerate(valuations.items()):
        ax.barh(i, hi - lo, left=lo, height=0.5,
                color=IB_COLORS['navy'], alpha=0.8)
        ax.plot(mid, i, 'D', color='white', markersize=8, zorder=5)
        ax.text(lo - 2, i, f'${lo:.0f}', ha='right', va='center', fontsize=10)
        ax.text(hi + 2, i, f'${hi:.0f}', ha='left',  va='center', fontsize=10)

    ax.axvline(offer_price,
               color=IB_COLORS['accent_red'],
               linestyle='--', linewidth=2,
               label=f'Offer: ${offer_price:.0f}')

    ax.set_yticks(range(len(methods)))
    ax.set_yticklabels(methods)
    ax.set_xlabel('Implied Share Price ($)')
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.legend(loc='lower right')
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 7. Sensitivity heatmap
# ---------------------------------------------------------------------------

def plot_sensitivity_heatmap(row_values, col_values, data_matrix,
                              row_label, col_label, title,
                              highlight_row_idx, highlight_col_idx,
                              fmt='$.0f'):
    """
    Seaborn heatmap with RdYlGn colourmap and a red rectangle on the base case.

    Parameters
    ----------
    row_values        : list of numbers (y-axis labels)
    col_values        : list of numbers (x-axis labels)
    data_matrix       : 2-D array-like (rows × cols)
    row_label         : str
    col_label         : str
    title             : str
    highlight_row_idx : int  — base-case row
    highlight_col_idx : int  — base-case column
    fmt               : str  — e.g. '$.0f' or '.1%'
    """
    data_matrix = np.array(data_matrix, dtype=float)

    # Build annotation strings
    def _apply_fmt(val, fmt_str):
        if fmt_str.startswith('$'):
            inner = fmt_str[1:]
            return f'${val:{inner}}'
        return f'{val:{fmt_str}}'

    annot = np.array([[_apply_fmt(v, fmt) for v in row]
                      for row in data_matrix])

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        data_matrix,
        annot=annot,
        fmt='',
        cmap='RdYlGn',
        xticklabels=[f'{v}' for v in col_values],
        yticklabels=[f'{v}' for v in row_values],
        ax=ax,
        linewidths=0.5,
        linecolor=IB_COLORS['light_gray'],
    )

    # Highlight base-case cell with a red rectangle
    rect = mpatches.Rectangle(
        (highlight_col_idx, highlight_row_idx),
        1, 1,
        linewidth=3,
        edgecolor=IB_COLORS['accent_red'],
        facecolor='none',
    )
    ax.add_patch(rect)

    ax.set_xlabel(col_label, labelpad=8)
    ax.set_ylabel(row_label, labelpad=8)
    ax.set_title(title, pad=14)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 8. Waterfall chart
# ---------------------------------------------------------------------------

def plot_waterfall(labels, values, title):
    """
    Waterfall / bridge chart.

    The first value is the starting total (e.g. Revenue), subsequent values
    are changes (negative = cost / deduction), and the last value is the
    final total (e.g. UFCF). Intermediate bars show deltas; first/last bars
    show absolute totals.

    Parameters
    ----------
    labels : list of str
    values : list of float  (first = start total, last = end total, rest = deltas)
    title  : str
    """
    fig, ax = plt.subplots(figsize=(14, 7))

    n = len(values)
    running = 0.0
    bottoms = []
    bar_colors = []

    for i, (label, val) in enumerate(zip(labels, values)):
        is_total = (i == 0) or (i == n - 1)
        if is_total:
            bottoms.append(0)
            bar_colors.append(IB_COLORS['navy'])
            running = val if i == 0 else running
        else:
            bottoms.append(running if val >= 0 else running + val)
            bar_colors.append(
                IB_COLORS['accent_green'] if val >= 0 else IB_COLORS['accent_red']
            )
            running += val

    # Draw bars
    bar_heights = []
    for i, (val, is_total) in enumerate(
            zip(values, [j == 0 or j == n - 1 for j in range(n)])):
        height = abs(val)
        bar_heights.append(height)
        ax.bar(i, height, bottom=bottoms[i], color=bar_colors[i],
               width=0.6, zorder=3)

        # Value label
        label_y = bottoms[i] + height / 2
        formatted = f'${val / 1000:.1f}B' if abs(val) >= 1000 else f'${val:.0f}M'
        ax.text(i, label_y, formatted, ha='center', va='center',
                fontsize=9, color='white', fontweight='bold', zorder=4)

    # Connector lines
    running2 = 0.0
    for i in range(n - 1):
        is_total = (i == 0) or (i == n - 1)
        top = bottoms[i] + bar_heights[i]
        next_bottom = bottoms[i + 1]
        ax.plot([i + 0.3, i + 0.7], [top, top],
                color=IB_COLORS['gray'], linewidth=0.8, linestyle='-')

    ax.set_xticks(range(n))
    ax.set_xticklabels(labels, rotation=15, ha='right')
    ax.set_ylabel('$ (Millions)', labelpad=8)
    ax.set_title(title, pad=14)
    ax.grid(axis='x', visible=False)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 9. Tornado chart
# ---------------------------------------------------------------------------

def plot_tornado(labels, low_values, high_values, base_value, title):
    """
    Tornado sensitivity chart — widest bars at top.

    Parameters
    ----------
    labels      : list of str
    low_values  : list of float  — downside values
    high_values : list of float  — upside values
    base_value  : float          — vertical line position
    title       : str
    """
    ranges = [abs(h - l) for h, l in zip(high_values, low_values)]
    order = np.argsort(ranges)[::-1]

    sorted_labels = [labels[i] for i in order]
    sorted_low    = [low_values[i] for i in order]
    sorted_high   = [high_values[i] for i in order]

    fig, ax = plt.subplots(figsize=(12, 7))
    y_pos = np.arange(len(sorted_labels))

    for yi, (lo, hi) in enumerate(zip(sorted_low, sorted_high)):
        # Downside bar (left of base)
        ax.barh(yi, lo - base_value, left=base_value,
                height=0.5, color=IB_COLORS['accent_red'], alpha=0.85)
        # Upside bar (right of base)
        ax.barh(yi, hi - base_value, left=base_value,
                height=0.5, color=IB_COLORS['accent_green'], alpha=0.85)
        # End labels
        ax.text(lo - abs(base_value) * 0.01, yi, f'${lo:.0f}',
                ha='right', va='center', fontsize=9,
                color=IB_COLORS['dark_gray'])
        ax.text(hi + abs(base_value) * 0.01, yi, f'${hi:.0f}',
                ha='left', va='center', fontsize=9,
                color=IB_COLORS['dark_gray'])

    ax.axvline(base_value, color=IB_COLORS['dark_navy'],
               linestyle='--', linewidth=1.5, label=f'Base: ${base_value:.0f}')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(sorted_labels)
    ax.set_xlabel('Implied Share Price ($)')
    ax.set_title(title, pad=14)
    ax.legend(frameon=False)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 10. Monte Carlo histogram
# ---------------------------------------------------------------------------

def plot_monte_carlo_hist(simulations, offer_price, title):
    """
    80-bin histogram of simulation results with percentile and offer lines.

    Parameters
    ----------
    simulations : array-like of float
    offer_price : float
    title       : str
    """
    sims = np.array(simulations)
    p10  = np.percentile(sims, 10)
    p50  = np.percentile(sims, 50)
    p90  = np.percentile(sims, 90)
    pct_above = (sims > offer_price).mean() * 100

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.hist(sims, bins=80, color=IB_COLORS['navy'], alpha=0.8, edgecolor='white')

    y_max = ax.get_ylim()[1]

    for val, label, ls in [
        (p10, f'P10: ${p10:.0f}', ':'),
        (p50, f'P50: ${p50:.0f}', '--'),
        (p90, f'P90: ${p90:.0f}', '-.'),
    ]:
        ax.axvline(val, color=IB_COLORS['steel_blue'], linestyle=ls,
                   linewidth=1.8, label=label)

    ax.axvline(offer_price, color=IB_COLORS['accent_red'],
               linestyle='--', linewidth=2.2,
               label=f'Offer: ${offer_price:.0f}')

    # Callout box
    ax.text(
        0.98, 0.95,
        f'{pct_above:.1f}% above offer',
        transform=ax.transAxes,
        ha='right', va='top', fontsize=12, fontweight='bold',
        color=IB_COLORS['accent_green'],
        bbox=dict(boxstyle='round,pad=0.5', fc='white',
                  ec=IB_COLORS['accent_green'], alpha=0.9),
    )

    ax.set_xlabel('Implied Share Price ($)', labelpad=8)
    ax.set_ylabel('Frequency', labelpad=8)
    ax.set_title(title, pad=14)
    ax.legend(frameon=False)
    plt.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 11. Comps scatter / bubble chart
# ---------------------------------------------------------------------------

def plot_comps_scatter(peer_data_df, hess_point, x_col, y_col, size_col, title):
    """
    Bubble scatter chart for comparable-company analysis.

    Parameters
    ----------
    peer_data_df : pd.DataFrame  — must contain x_col, y_col, size_col, 'Name'
    hess_point   : tuple         — (x_val, y_val, size_val, 'Label')
    x_col        : str           — e.g. 'EV/EBITDA'
    y_col        : str           — e.g. 'EV/DACF'
    size_col     : str           — bubble size column
    title        : str
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    # Peer bubbles
    sizes = (peer_data_df[size_col] / peer_data_df[size_col].max()) * 800 + 100
    ax.scatter(
        peer_data_df[x_col], peer_data_df[y_col],
        s=sizes, c=IB_COLORS['steel_blue'], alpha=0.7,
        edgecolors=IB_COLORS['navy'], linewidths=0.8, zorder=3,
    )

    for _, row in peer_data_df.iterrows():
        ax.annotate(
            row['Name'],
            xy=(row[x_col], row[y_col]),
            xytext=(5, 5), textcoords='offset points',
            fontsize=9, color=IB_COLORS['dark_gray'],
        )

    # Hess star marker
    hx, hy, hs, hlabel = hess_point
    hsize = (hs / peer_data_df[size_col].max()) * 800 + 100
    ax.scatter(hx, hy, s=hsize * 1.5, marker='*',
               c=IB_COLORS['accent_red'], edgecolors=IB_COLORS['dark_navy'],
               linewidths=0.8, zorder=5, label=hlabel)
    ax.annotate(
        hlabel, xy=(hx, hy),
        xytext=(8, 8), textcoords='offset points',
        fontsize=10, fontweight='bold', color=IB_COLORS['accent_red'],
    )

    # Regression line (peers only)
    x_fit = peer_data_df[x_col].values
    y_fit = peer_data_df[y_col].values
    if len(x_fit) > 1:
        coeffs = np.polyfit(x_fit, y_fit, 1)
        poly   = np.poly1d(coeffs)
        x_line = np.linspace(x_fit.min() - 0.5, x_fit.max() + 0.5, 200)
        ax.plot(x_line, poly(x_line),
                color=IB_COLORS['gray'], linestyle='--',
                linewidth=1.2, alpha=0.8, label='Regression')

    # Axis ranges suitable for E&P (3x–12x EV/EBITDA)
    x_min = max(3, peer_data_df[x_col].min() - 1)
    x_max = min(12, peer_data_df[x_col].max() + 1)
    ax.set_xlim(x_min, x_max)

    ax.set_xlabel(x_col, labelpad=8)
    ax.set_ylabel(y_col, labelpad=8)
    ax.set_title(title, pad=14)
    ax.legend(frameon=False)
    plt.tight_layout()
    return fig
