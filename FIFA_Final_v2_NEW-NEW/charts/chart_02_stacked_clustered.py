"""
chart_02_stacked_clustered.py — Week 2: Stacked & Clustered Charts
Dr. Plotly pattern: px.bar with barmode='stack' or barmode='group', text_auto=True.
"""

import pandas as pd
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from config import COLORS, BLUE, ORANGE, GREEN, load_data


def _pos_group(pos):
    p = str(pos).split(",")[0].strip()
    if p == "GK":                           return "Goalkeeper"
    if p in ["CB","LB","RB","LWB","RWB"]:  return "Defender"
    if p in ["CDM","CM","CAM","LM","RM"]:   return "Midfielder"
    return "Forward"


# ── Stacked Column ─────────────────────────────────────────────────────────────
def make_stacked_column(df: pd.DataFrame):
    """Squad composition by position group per league — Stacked Column."""
    d = df.copy()
    d["pos_group"] = d["player_positions"].apply(_pos_group)
    agg = d.groupby(["league_name","pos_group"]).size().reset_index(name="count")

    # winner on left: order by total count descending
    order = (agg.groupby("league_name")["count"].sum()
               .sort_values(ascending=False).index.tolist())

    fig = px.bar(
        agg,
        x="league_name", y="count",
        color="pos_group",
        barmode="stack",
        text_auto=True,
        category_orders={"league_name": order,
                         "pos_group": ["Goalkeeper","Defender","Midfielder","Forward"]},
        color_discrete_sequence=[COLORS[0], COLORS[1], COLORS[2], GREEN],
        title="Squad Composition by Position Group per League — Stacked Column",
        labels={"league_name":"League","count":"Number of Players","pos_group":"Position"},
    )
    fig.update_traces(textfont_color="white", marker_line_color="black", marker_line_width=0.5)
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", tickangle=0, linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", rangemode="tozero", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1, x=1.0, y=1.0),
        margin=dict(t=70, r=190, b=70, l=70),
    )
    return fig


# ── Stacked Bar ────────────────────────────────────────────────────────────────
def make_stacked_bar(df: pd.DataFrame):
    """Same data, horizontal orientation."""
    d = df.copy()
    d["pos_group"] = d["player_positions"].apply(_pos_group)
    agg = d.groupby(["league_name","pos_group"]).size().reset_index(name="count")

    order = (agg.groupby("league_name")["count"].sum()
               .sort_values(ascending=True).index.tolist())   # ascending → best on top

    fig = px.bar(
        agg,
        y="league_name", x="count",
        color="pos_group",
        barmode="stack",
        orientation="h",
        text_auto=True,
        category_orders={"league_name": order,
                         "pos_group": ["Goalkeeper","Defender","Midfielder","Forward"]},
        color_discrete_sequence=[COLORS[0], COLORS[1], COLORS[2], GREEN],
        title="Squad Composition by Position Group per League — Stacked Bar",
        labels={"league_name":"League","count":"Number of Players","pos_group":"Position"},
    )
    fig.update_traces(textfont_color="white", marker_line_color="black", marker_line_width=0.5)
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", rangemode="tozero", linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1, x=1.0, y=1.0),
        margin=dict(t=70, r=190, b=70, l=130),
    )
    return fig


# ── Clustered Column ───────────────────────────────────────────────────────────
def make_clustered_column(df: pd.DataFrame):
    """Pace vs Shooting side-by-side per league — Clustered Column."""
    agg = (
        df.groupby("league_name")[["pace","shooting"]]
        .mean().round(1).reset_index()
        .sort_values("pace", ascending=False)    # winner on left
    )
    agg_long = agg.melt(id_vars="league_name", value_vars=["pace","shooting"],
                        var_name="Skill", value_name="Score")
    agg_long["Skill"] = agg_long["Skill"].str.title()

    fig = px.bar(
        agg_long,
        x="league_name", y="Score",
        color="Skill",
        barmode="group",
        text_auto=".1f",
        color_discrete_sequence=[BLUE, COLORS[1]],
        title="Pace vs Shooting — Side-by-Side by League (Clustered Column)",
        labels={"league_name":"League","Score":"Average Skill Score","Skill":"Skill"},
    )
    fig.update_traces(textposition="outside", textfont_color="black",
                      marker_line_color="black", marker_line_width=0.8)
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", tickangle=0, linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", rangemode="tozero", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1, x=1.0, y=1.0),
        margin=dict(t=70, r=180, b=70, l=70),
    )
    return fig


# ── Clustered Bar ──────────────────────────────────────────────────────────────
def make_clustered_bar(df: pd.DataFrame):
    """Same data, horizontal orientation."""
    agg = (
        df.groupby("league_name")[["pace","shooting"]]
        .mean().round(1).reset_index()
        .sort_values("pace", ascending=True)     # ascending → best on top
    )
    agg_long = agg.melt(id_vars="league_name", value_vars=["pace","shooting"],
                        var_name="Skill", value_name="Score")
    agg_long["Skill"] = agg_long["Skill"].str.title()

    fig = px.bar(
        agg_long,
        y="league_name", x="Score",
        color="Skill",
        barmode="group",
        orientation="h",
        text_auto=".1f",
        color_discrete_sequence=[BLUE, COLORS[1]],
        title="Pace vs Shooting — Side-by-Side by League (Clustered Bar)",
        labels={"league_name":"League","Score":"Average Skill Score","Skill":"Skill"},
    )
    fig.update_traces(textposition="outside", textfont_color="black",
                      marker_line_color="black", marker_line_width=0.8)
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", rangemode="tozero", linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1, x=1.0, y=1.0),
        margin=dict(t=70, r=180, b=70, l=140),
    )
    return fig


if __name__ == "__main__":
    df = load_data()
    make_stacked_column(df).show()
    make_stacked_bar(df).show()
    make_clustered_column(df).show()
    make_clustered_bar(df).show()
    print("✅ Stacked & Clustered charts rendered.")
