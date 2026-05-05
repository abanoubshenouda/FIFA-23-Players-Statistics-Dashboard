"""
chart_07_violin.py — Week 7: Violin Chart
Dr. Plotly pattern (exact):
  px.violin(x, y, color, category_orders, color_discrete_sequence=COLORS,
            box=True, points='outliers')
  fig.update_traces(spanmode='hard')
  fig.update_layout(showlegend=False)
"""

import pandas as pd
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from config import COLORS, load_data

# Week 7 notebook uses PURPLE-first palette
W7_COLORS = [
    '#9C27B0', '#FF5722', '#4CAF50', '#2196F3',
    '#FF9800', '#00BCD4', '#E91E63', '#607D8B',
    '#8BC34A', '#FF5252',
]


def make_violin_overall_by_league(df: pd.DataFrame):
    """Overall Rating distribution by League — Violin Chart."""
    leagues = sorted(df["league_name"].dropna().unique())

    fig = px.violin(
        df,
        x="league_name",
        y="overall",
        color="league_name",
        category_orders={"league_name": leagues},
        color_discrete_sequence=W7_COLORS,
        box=True,
        points="outliers",
        labels={"league_name":"League","overall":"Overall Rating (0–100)"},
        title="Overall Rating Distribution by League<br><sup>Violin Chart</sup>",
    )
    fig.update_traces(spanmode="hard")
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


def make_violin_age_by_league(df: pd.DataFrame):
    """Player Age distribution by League — Violin Chart."""
    leagues = sorted(df["league_name"].dropna().unique())

    fig = px.violin(
        df,
        x="league_name",
        y="age",
        color="league_name",
        category_orders={"league_name": leagues},
        color_discrete_sequence=W7_COLORS,
        box=True,
        points="outliers",
        labels={"league_name":"League","age":"Age (years)"},
        title="Player Age Distribution by League<br><sup>Violin Chart</sup>",
    )
    fig.update_traces(spanmode="hard")
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


def make_violin_skills(df: pd.DataFrame):
    """All skill attributes — Violin Chart."""
    skills = ["pace","shooting","passing","dribbling","defending","physic"]
    melt = df[skills].melt(var_name="Skill", value_name="Score")
    melt["Skill"] = melt["Skill"].str.title()

    fig = px.violin(
        melt,
        x="Skill",
        y="Score",
        color="Skill",
        category_orders={"Skill": [s.title() for s in skills]},
        color_discrete_sequence=W7_COLORS,
        box=True,
        points="outliers",
        labels={"Skill":"Skill Attribute","Score":"Score (0–100)"},
        title="All Skill Attributes Distribution<br><sup>Violin Chart (FIFA 23)</sup>",
    )
    fig.update_traces(spanmode="hard")
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


def make_violin_metric_by_league(df: pd.DataFrame, metric: str):
    """Dashboard: violin for any selected metric by league."""
    leagues = sorted(df["league_name"].dropna().unique())
    label = metric.replace("_"," ").title()

    fig = px.violin(
        df,
        x="league_name",
        y=metric,
        color="league_name",
        category_orders={"league_name": leagues},
        color_discrete_sequence=W7_COLORS,
        box=True,
        points="outliers",
        labels={"league_name":"League", metric: label},
        title=f"{label} Distribution by League<br><sup>Violin Chart</sup>",
    )
    fig.update_traces(spanmode="hard")
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
    make_violin_overall_by_league(df).show()
    make_violin_age_by_league(df).show()
    make_violin_skills(df).show()
    print("✅ Violin charts rendered.")
