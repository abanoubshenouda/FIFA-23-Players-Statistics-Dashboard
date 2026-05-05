"""
chart_05_histogram.py — Week 5: Histogram
Dr. Plotly pattern (exact):
  px.histogram(x, color, barmode='overlay', nbins=25, opacity=0.45,
               histnorm='density', color_discrete_sequence=COLORS)
  fig.update_traces(marker_line_width=0)
"""

import pandas as pd
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from config import COLORS, BLUE, GREEN, load_data


def make_histogram_overall(df: pd.DataFrame):
    """Overall Rating distribution by League — Normalised Density Histogram."""
    fig = px.histogram(
        df,
        x="overall",
        color="league_name",
        barmode="overlay",
        nbins=25,
        opacity=0.45,
        histnorm="density",
        color_discrete_sequence=COLORS,
        labels={"overall":"Overall Rating (0–100)", "league_name":"League"},
        title="Overall Rating Distribution by League<br><sup>Normalised Density Histogram</sup>",
    )
    fig.update_traces(marker_line_width=0)
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", rangemode="tozero", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1, x=1.0, y=1.0,
                    title="League"),
        margin=dict(t=80, r=190, b=70, l=70),
    )
    return fig


def make_histogram_age(df: pd.DataFrame):
    """Age distribution — Single histogram + KDE."""
    fig = px.histogram(
        df,
        x="age",
        nbins=25,
        opacity=0.65,
        histnorm="density",
        color_discrete_sequence=[BLUE],
        labels={"age":"Age (years)"},
        title="Distribution of Player Age — FIFA 23<br><sup>25-bin Histogram</sup>",
    )
    fig.update_traces(marker_line_width=0)
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", rangemode="tozero", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        margin=dict(t=80, r=160, b=70, l=70),
    )
    return fig


def make_histogram_value(df: pd.DataFrame):
    """Market Value (€M) distribution by League — Right-skewed."""
    plot = df[df["value_M"] > 0].copy()

    fig = px.histogram(
        plot,
        x="value_M",
        color="league_name",
        barmode="overlay",
        nbins=25,
        opacity=0.45,
        histnorm="density",
        color_discrete_sequence=COLORS,
        labels={"value_M":"Market Value (€M)", "league_name":"League"},
        title="Market Value Distribution by League (€M)<br><sup>Right-Skewed Density Histogram</sup>",
    )
    fig.update_traces(marker_line_width=0)
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", rangemode="tozero", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1, x=1.0, y=1.0,
                    title="League"),
        margin=dict(t=80, r=190, b=70, l=70),
    )
    return fig


def make_histogram_metric(df: pd.DataFrame, metric: str):
    """Dashboard: histogram for any selected metric."""
    label = metric.replace("_"," ").title()
    fig = px.histogram(
        df,
        x=metric,
        color="league_name",
        barmode="overlay",
        nbins=25,
        opacity=0.45,
        histnorm="density",
        color_discrete_sequence=COLORS,
        labels={metric: label, "league_name":"League"},
        title=f"Distribution of {label} — FIFA Players<br><sup>Normalised Density Histogram</sup>",
    )
    fig.update_traces(marker_line_width=0)
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", linecolor="black"),
        yaxis=dict(gridcolor="lightgrey", rangemode="tozero", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1, x=1.0, y=1.0,
                    title="League"),
        margin=dict(t=80, r=190, b=70, l=70),
    )
    return fig


if __name__ == "__main__":
    df = load_data()
    make_histogram_age(df).show()
    make_histogram_overall(df).show()
    make_histogram_value(df).show()
    print("✅ Histogram charts rendered.")
