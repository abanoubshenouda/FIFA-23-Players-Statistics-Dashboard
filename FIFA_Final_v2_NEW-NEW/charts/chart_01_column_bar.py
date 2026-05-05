"""
chart_01_column_bar.py — Week 1 & 2: Column Chart + Bar Chart
Dr. Plotly pattern: px.bar with minimal arguments, clean and simple.
"""

import pandas as pd
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from config import COLORS, BLUE, GREEN, load_data


def make_column_chart(df: pd.DataFrame):
    """Average Overall Rating by League — Column Chart (winner on left)."""
    agg = (
        df.groupby("league_name")["overall"]
        .mean().round(1)
        .sort_values(ascending=False)
        .reset_index()
    )

    # Rule 8: lightgreen for winner, lightblue for others
    color_map = {row["league_name"]: ("lightgreen" if i == 0 else "lightblue")
                 for i, row in agg.iterrows()}

    fig = px.bar(
        agg,
        x="league_name",
        y="overall",
        color="league_name",
        color_discrete_map=color_map,
        text="overall",
        title="Average Overall Rating by League — FIFA 23",
        labels={"league_name": "League", "overall": "Average Overall Rating"},
    )
    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside",
        textfont_color="black",
        marker_line_color="black",
        marker_line_width=0.8,
    )
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        font_color="black",
        xaxis=dict(gridcolor="lightgrey", tickangle=0, linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", rangemode="tozero", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1, x=1.0, y=1.0),
        showlegend=True,
        margin=dict(t=70, r=180, b=70, l=70),
    )
    return fig


def make_bar_chart(df: pd.DataFrame):
    """Top 10 Clubs by Overall Rating — Horizontal Bar Chart (winner on top)."""
    agg = (
        df.groupby("club_name")["overall"]
        .mean().round(1)
        .sort_values(ascending=False)
        .head(10).reset_index()
        .sort_values("overall", ascending=True)   # ascending → best on top
    )

    colors = ["lightblue"] * len(agg)
    colors[-1] = "lightgreen"

    fig = px.bar(
        agg,
        y="club_name",
        x="overall",
        orientation="h",
        color="club_name",
        color_discrete_sequence=colors,
        text="overall",
        title="Top 10 Clubs — Overall Rating Standings (FIFA 23)",
        labels={"club_name": "Club Name", "overall": "Average Overall Rating"},
    )
    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside",
        textfont_color="black",
        marker_line_color="black",
        marker_line_width=0.8,
        showlegend=False,
    )
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        font_color="black",
        xaxis=dict(gridcolor="lightgrey", rangemode="tozero", linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        margin=dict(t=70, r=80, b=70, l=200),
    )
    return fig


if __name__ == "__main__":
    df = load_data()
    make_column_chart(df).show()
    make_bar_chart(df).show()
    print("✅ Column & Bar charts rendered.")