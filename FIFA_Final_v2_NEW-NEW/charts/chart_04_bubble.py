"""
chart_04_bubble.py — Week 4: Bubble Chart
Dr. Plotly pattern: px.scatter with size='vote_count', size_max=40, opacity=0.45.
"""

import pandas as pd
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from config import COLORS, load_data


def make_bubble_club(df: pd.DataFrame):
    """Club Avg Age vs Avg Overall, bubble size = total market value."""
    agg = (
        df.groupby("club_name")
        .agg(avg_age=("age","mean"), avg_overall=("overall","mean"),
             total_value=("value_M","sum"), count=("short_name","count"),
             league=("league_name","first"))
        .reset_index()
    )
    agg = agg[agg["count"] >= 4].round(1)

    fig = px.scatter(
        agg,
        x="avg_age",
        y="avg_overall",
        size="total_value",
        size_max=40,
        color="league",
        opacity=0.45,
        hover_name="club_name",
        color_discrete_sequence=COLORS,
        labels={"avg_age":"Average Age (years)","avg_overall":"Average Overall Rating",
                "total_value":"Total Value (€M)","league":"League"},
        title="Club Scouting: Avg Age vs Overall — Bubble Size = Market Value (€M)",
    )
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1, x=1.0, y=1.0),
        margin=dict(t=80, r=200, b=70, l=70),
    )
    return fig


def make_bubble_skills(df: pd.DataFrame):
    """Pace vs Shooting, bubble size = overall rating, colour = league."""
    fig = px.scatter(
        df,
        x="pace",
        y="shooting",
        size="overall",
        size_max=20,
        color="league_name",
        opacity=0.45,
        hover_name="short_name",
        color_discrete_sequence=COLORS,
        labels={"pace":"Pace Total","shooting":"Shooting Total",
                "overall":"Overall Rating","league_name":"League"},
        title="Pace vs Shooting — Bubble Size = Overall Rating  |  Colour = League",
    )
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1, x=1.0, y=1.0),
        margin=dict(t=70, r=200, b=70, l=70),
    )
    return fig


if __name__ == "__main__":
    df = load_data()
    make_bubble_club(df).show()
    make_bubble_skills(df).show()
    print("✅ Bubble charts rendered.")
