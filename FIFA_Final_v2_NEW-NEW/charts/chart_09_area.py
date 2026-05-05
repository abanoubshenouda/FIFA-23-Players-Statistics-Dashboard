"""
chart_09_area.py — Week 9: Area Chart
Dr. Plotly pattern (exact):
  Single:  px.area(x, y)
  Stacked: px.area(x, y, color='type')
  CRITICAL: plt.ylim(0, None) → yaxis rangemode='tozero'
"""

import pandas as pd
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from config import COLORS, BLUE, ORANGE, load_data


def _pos_group(pos):
    p = str(pos).split(",")[0].strip()
    if p == "GK":                           return "Goalkeeper"
    if p in ["CB","LB","RB","LWB","RWB"]:  return "Defender"
    if p in ["CDM","CM","CAM","LM","RM"]:   return "Midfielder"
    return "Forward"


def make_area_single(df: pd.DataFrame):
    """Total players per FIFA Edition — Single Area Chart."""
    by_ver = (
        df.groupby("fifa_version").size()
        .reset_index(name="player_count")
        .sort_values("fifa_version")
    )
    versions = sorted(by_ver["fifa_version"].unique())

    # Dr. pattern: px.area(x, y)
    fig = px.area(
        by_ver,
        x="fifa_version",
        y="player_count",
        color_discrete_sequence=[BLUE],
        labels={"fifa_version":"FIFA Edition","player_count":"Number of Players"},
        title="Total Players per FIFA Edition<br><sup>Area Chart</sup>",
    )
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", linecolor="black",
                   tickvals=versions, ticktext=[str(v) for v in versions]),
        yaxis=dict(gridcolor="lightgrey", rangemode="tozero", linecolor="black"),  # Dr.: plt.ylim(0, None)
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        margin=dict(t=70, r=80, b=70, l=70),
    )
    return fig


def make_area_stacked_positions(df: pd.DataFrame):
    """Player count by Position Group per Edition — Stacked Area Chart."""
    d = df.copy()
    d["pos_group"] = d["player_positions"].apply(_pos_group)

    agg = (
        d.groupby(["fifa_version","pos_group"]).size()
        .reset_index(name="count")
    )
    versions = sorted(agg["fifa_version"].unique())
    pos_order = ["Goalkeeper","Defender","Midfielder","Forward"]

    # Ensure all combos present
    from itertools import product
    full = pd.DataFrame(list(product(versions, pos_order)), columns=["fifa_version","pos_group"])
    agg = full.merge(agg, on=["fifa_version","pos_group"], how="left").fillna(0)
    agg["count"] = agg["count"].astype(int)

    # Dr. pattern: px.area(x, y, color='type')
    fig = px.area(
        agg,
        x="fifa_version",
        y="count",
        color="pos_group",
        category_orders={"pos_group": pos_order},
        color_discrete_sequence=COLORS[:4],
        labels={"fifa_version":"FIFA Edition","count":"Number of Players",
                "pos_group":"Position Group"},
        title="Player Count by Position Group per FIFA Edition<br><sup>Stacked Area Chart</sup>",
    )
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", linecolor="black",
                   tickvals=versions, ticktext=[str(v) for v in versions]),
        yaxis=dict(gridcolor="lightgrey", rangemode="tozero", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1, x=1.0, y=1.0,
                    title="Position"),
        margin=dict(t=70, r=190, b=70, l=70),
    )
    return fig


def make_area_stacked_value(df: pd.DataFrame):
    """Total Market Value (€M) by League per Edition — Stacked Area Chart."""
    agg = (
        df.groupby(["fifa_version","league_name"])["value_M"]
        .sum().round(1).reset_index()
    )
    leagues  = sorted(agg["league_name"].unique())
    versions = sorted(agg["fifa_version"].unique())

    # Ensure all combos present
    from itertools import product
    full = pd.DataFrame(list(product(versions, leagues)),
                        columns=["fifa_version","league_name"])
    agg = full.merge(agg, on=["fifa_version","league_name"], how="left").fillna(0)

    # Dr. pattern: px.area(x, y, color='type')
    fig = px.area(
        agg,
        x="fifa_version",
        y="value_M",
        color="league_name",
        category_orders={"league_name": leagues},
        color_discrete_sequence=COLORS,
        labels={"fifa_version":"FIFA Edition","value_M":"Total Market Value (€M)",
                "league_name":"League"},
        title="Total Market Value (€M) by League per FIFA Edition<br><sup>Stacked Area Chart</sup>",
    )
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", linecolor="black",
                   tickvals=versions, ticktext=[str(v) for v in versions]),
        yaxis=dict(gridcolor="lightgrey", rangemode="tozero", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1, x=1.0, y=1.0,
                    title="League"),
        margin=dict(t=70, r=190, b=70, l=70),
    )
    return fig


if __name__ == "__main__":
    df = load_data()
    make_area_single(df).show()
    make_area_stacked_positions(df).show()
    make_area_stacked_value(df).show()
    print("✅ Area charts rendered.")
