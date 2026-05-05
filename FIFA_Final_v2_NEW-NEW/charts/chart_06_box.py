"""
chart_06_box.py — Week 6: Box Chart
Dr. Plotly pattern (exact):
  px.box(x, y, color, category_orders, color_discrete_sequence=COLORS,
         points='outliers')
  fig.update_layout(showlegend=False)
"""

import pandas as pd
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from config import COLORS, load_data


def make_box_overall_by_position(df: pd.DataFrame):
    """Overall Rating distribution by player position."""
    positions = sorted(df["player_positions"].dropna().unique())

    fig = px.box(
        df,
        x="player_positions",
        y="overall",
        color="player_positions",
        category_orders={"player_positions": positions},
        color_discrete_sequence=COLORS,
        points="outliers",
        labels={"player_positions":"Player Position","overall":"Overall Rating (0–100)"},
        title="Overall Rating Distribution by Player Position<br><sup>Box Chart</sup>",
    )
    fig.update_layout(
        showlegend=False,
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", tickangle=0, linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", rangemode="tozero", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        margin=dict(t=70, r=80, b=70, l=70),
    )
    return fig


def make_box_value_by_league(df: pd.DataFrame):
    """Market Value distribution by league."""
    leagues = sorted(df["league_name"].dropna().unique())
    plot = df[df["value_M"] > 0]

    fig = px.box(
        plot,
        x="league_name",
        y="value_M",
        color="league_name",
        category_orders={"league_name": leagues},
        color_discrete_sequence=COLORS,
        points="outliers",
        labels={"league_name":"League","value_M":"Market Value (€M)"},
        title="Market Value Distribution by League (€M)<br><sup>Box Chart</sup>",
    )
    fig.update_layout(
        showlegend=False,
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", tickangle=0, linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", rangemode="tozero", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        margin=dict(t=70, r=80, b=70, l=70),
    )
    return fig


def make_box_skills_notched(df: pd.DataFrame):
    """All skill attributes — Notched Box Chart."""
    skills = ["pace","shooting","passing","dribbling","defending","physic"]
    melt = df[skills].melt(var_name="Skill", value_name="Score")
    melt["Skill"] = melt["Skill"].str.title()

    fig = px.box(
        melt,
        x="Skill",
        y="Score",
        color="Skill",
        category_orders={"Skill": [s.title() for s in skills]},
        color_discrete_sequence=COLORS,
        points="outliers",
        notched=True,
        labels={"Skill":"Skill Attribute","Score":"Score (0–100)"},
        title="All Skill Attributes Distribution<br><sup>Notched Box Chart (FIFA 23)</sup>",
    )
    fig.update_layout(
        showlegend=False,
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", tickangle=0, linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", rangemode="tozero", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        margin=dict(t=70, r=80, b=70, l=70),
    )
    return fig


def make_box_metric_by_position(df: pd.DataFrame, metric: str):
    """Dashboard: box chart for any selected metric by position."""
    positions = sorted(df["player_positions"].dropna().unique())
    label = metric.replace("_"," ").title()

    fig = px.box(
        df,
        x="player_positions",
        y=metric,
        color="player_positions",
        category_orders={"player_positions": positions},
        color_discrete_sequence=COLORS,
        points="outliers",
        labels={"player_positions":"Player Position", metric: label},
        title=f"{label} Distribution by Player Position<br><sup>Box Chart</sup>",
    )
    fig.update_layout(
        showlegend=False,
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", tickangle=0, linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", rangemode="tozero", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        margin=dict(t=70, r=80, b=70, l=70),
    )
    return fig


if __name__ == "__main__":
    df = load_data()
    make_box_overall_by_position(df).show()
    make_box_value_by_league(df).show()
    make_box_skills_notched(df).show()
    print("✅ Box charts rendered.")
