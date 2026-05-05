"""
config.py — Shared configuration for all FIFA chart modules.
Follows the exact color palette and style from Dr. notebooks.
"""

import pandas as pd

# ── Dr. Notebook Color Palette ─────────────────────────────────────────────────
BLUE   = '#2196F3'
ORANGE = '#FF5722'
GREEN  = '#4CAF50'
PURPLE = '#9C27B0'

COLORS = [
    '#2196F3', '#FF5722', '#4CAF50', '#9C27B0',
    '#FF9800', '#00BCD4', '#E91E63', '#607D8B',
    '#8BC34A', '#FF5252',
]

# ── Dr. Guidelines — White-background layout shared by all charts ──────────────
LAYOUT_BASE = dict(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color="black", family="Arial, sans-serif", size=12),
    title_font=dict(color="black", size=14),
)

AXIS_BASE = dict(
    gridcolor="lightgrey",
    gridwidth=1,
    showgrid=True,
    title_font=dict(color="black"),
    tickfont=dict(color="black"),
    linecolor="black",
    linewidth=1,
)

BORDER_SHAPE = dict(
    type="rect", xref="paper", yref="paper",
    x0=0, y0=0, x1=1, y1=1,
    line=dict(color="black", width=2),
)

LEGEND_BASE = dict(
    bgcolor="white",
    bordercolor="black",
    borderwidth=1,
    font=dict(color="black"),
    x=1.0, y=1.0,
)


def load_data(path: str = "../data/male_players_cleaned.csv") -> pd.DataFrame:
    """Load and prepare the FIFA players dataset."""
    df = pd.read_csv(path)
    df["value_M"] = (df["value_eur"] / 1e6).round(2)
    df["wage_K"]  = (df["wage_eur"]  / 1e3).round(1)
    skill_cols = ["pace", "shooting", "passing", "dribbling", "defending", "physic"]
    df["avg_skill"] = df[skill_cols].mean(axis=1).round(1)
    return df
