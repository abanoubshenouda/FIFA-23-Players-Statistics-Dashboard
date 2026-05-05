"""
chart_03_scatter.py — Week 3: Scatter Chart
Dr. Plotly pattern: px.scatter with color, opacity, hover_name.
"""

import pandas as pd
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from config import COLORS, load_data


def make_scatter_pace_overall(df: pd.DataFrame):
    """Pace vs Overall Rating, coloured by League."""
    fig = px.scatter(
        df,
        x="pace",
        y="overall",
        color="league_name",
        opacity=0.4,
        hover_name="short_name",
        color_discrete_sequence=COLORS,
        labels={"pace":"Pace Total","overall":"Overall Rating","league_name":"League"},
        title="Pace vs Overall Rating — Coloured by League (FIFA 23)",
    )
    fig.update_traces(marker=dict(size=8))
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1, x=1.0, y=1.0),
        margin=dict(t=70, r=180, b=70, l=70),
    )
    return fig


def make_scatter_age_value(df: pd.DataFrame):
    """Age vs Market Value — ST vs CB positions."""
    plot = df[df["player_positions"].isin(["ST","CB"])].copy()

    fig = px.scatter(
        plot,
        x="age",
        y="value_M",
        color="player_positions",
        opacity=0.45,
        hover_name="short_name",
        color_discrete_sequence=[COLORS[0], COLORS[1]],
        labels={"age":"Player Age (years)","value_M":"Market Value (€M)",
                "player_positions":"Position"},
        title="Age vs Market Value — ST vs CB (FIFA 23)",
    )
    fig.update_traces(marker=dict(size=8))
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1, x=1.0, y=1.0),
        margin=dict(t=70, r=180, b=70, l=70),
    )
    return fig


def make_scatter_custom(df: pd.DataFrame, x_col: str, y_col: str, color_col: str):
    """Interactive scatter for dashboard dropdowns."""
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        opacity=0.4,
        hover_name="short_name",
        color_discrete_sequence=COLORS,
        labels={x_col: x_col.replace("_"," ").title(),
                y_col: y_col.replace("_"," ").title(),
                color_col: color_col.replace("_"," ").title()},
        title=f"{x_col.replace('_',' ').title()} vs {y_col.replace('_',' ').title()} — FIFA 23",
    )
    fig.update_traces(marker=dict(size=8))
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1, x=1.0, y=1.0),
        margin=dict(t=70, r=180, b=70, l=70),
    )
    return fig


if __name__ == "__main__":
    df = load_data()
    make_scatter_pace_overall(df).show()
    make_scatter_age_value(df).show()
    print("✅ Scatter charts rendered.")
