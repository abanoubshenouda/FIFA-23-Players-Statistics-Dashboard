"""
chart_08_line.py — Week 8: Line Chart
Dr. Plotly patterns (exact):
  Single line:   px.line(x, y, color_discrete_sequence=[BLUE])
                 fig.update_traces(line_width=2)
  Multi-line:    px.line(x, y, color, color_discrete_sequence=COLORS, markers=True)
                 fig.update_traces(line_width=2.5, marker_size=6)
  Moving avg:    go.Figure() + go.Scatter(line=dict(color, width), opacity=0.35)
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from config import COLORS, BLUE, ORANGE, GREEN, PURPLE, load_data


def make_line_overall_by_edition(df: pd.DataFrame):
    """Avg Overall Rating per FIFA Edition per League — Multi-line."""
    agg = (
        df.groupby(["fifa_version","league_name"])["overall"]
        .mean().round(2).reset_index()
    )

    fig = px.line(
        agg,
        x="fifa_version",
        y="overall",
        color="league_name",
        markers=True,
        color_discrete_sequence=COLORS,
        labels={"fifa_version":"FIFA Edition","overall":"Average Overall Rating",
                "league_name":"League"},
        title="Average Overall Rating per FIFA Edition by League<br><sup>Multiple Line Chart</sup>",
    )
    fig.update_traces(line_width=2.5, marker_size=6)
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", linecolor="black",
                   tickvals=sorted(df["fifa_version"].unique()),
                   ticktext=[str(v) for v in sorted(df["fifa_version"].unique())]),
        yaxis=dict(gridcolor="lightgrey", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1, x=1.0, y=1.0,
                    title="League"),
        margin=dict(t=70, r=190, b=70, l=70),
    )
    return fig


def make_line_normalised_trends(df: pd.DataFrame):
    """Avg Overall vs Avg Market Value — Normalised (0-1) per edition."""
    agg = (
        df.groupby("fifa_version")
        .agg(avg_overall=("overall","mean"), avg_value=("value_M","mean"))
        .reset_index().sort_values("fifa_version")
    )
    for col in ["avg_overall","avg_value"]:
        mn, mx = agg[col].min(), agg[col].max()
        agg[col+"_norm"] = ((agg[col]-mn)/(mx-mn)).round(3) if mx != mn else 0.5

    agg_long = agg[["fifa_version","avg_overall_norm","avg_value_norm"]].melt(
        id_vars="fifa_version",
        value_vars=["avg_overall_norm","avg_value_norm"],
        var_name="Metric", value_name="Value"
    )
    agg_long["Metric"] = agg_long["Metric"].map({
        "avg_overall_norm": "Avg Overall Rating",
        "avg_value_norm":   "Avg Market Value",
    })

    fig = px.line(
        agg_long,
        x="fifa_version",
        y="Value",
        color="Metric",
        markers=True,
        color_discrete_sequence=[BLUE, ORANGE],
        labels={"fifa_version":"FIFA Edition","Value":"Normalised Value (0–1)","Metric":""},
        title="Average Overall vs Market Value (Normalised) per FIFA Edition<br><sup>Multiple Line Chart</sup>",
    )
    fig.update_traces(line_width=2)
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", linecolor="black",
                   tickvals=sorted(df["fifa_version"].unique()),
                   ticktext=[str(v) for v in sorted(df["fifa_version"].unique())]),
        yaxis=dict(gridcolor="lightgrey", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1, x=1.0, y=1.0),
        margin=dict(t=70, r=190, b=70, l=70),
    )
    return fig


def make_line_moving_average(df: pd.DataFrame):
    """Avg Overall per edition + Moving Average overlay — Dr. go.Figure pattern."""
    by_ver = (
        df.groupby("fifa_version")["overall"]
        .mean().round(2).reset_index(name="avg_overall")
        .sort_values("fifa_version")
    )
    # Dr. pattern: rolling(window=5/10, center=True, min_periods=1).mean()
    by_ver["MA_2"]  = by_ver["avg_overall"].rolling(window=2,  center=True, min_periods=1).mean()
    by_ver["MA_3"]  = by_ver["avg_overall"].rolling(window=3,  center=True, min_periods=1).mean()

    versions = sorted(by_ver["fifa_version"].unique())

    # Dr. exact go.Figure pattern
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=by_ver["fifa_version"], y=by_ver["avg_overall"],
        name="Yearly Average",
        line=dict(color=PURPLE, width=1),
        opacity=0.35,
    ))
    fig.add_trace(go.Scatter(
        x=by_ver["fifa_version"], y=by_ver["MA_2"],
        name="2-Edition MA",
        line=dict(color=PURPLE, width=2.5),
    ))
    fig.add_trace(go.Scatter(
        x=by_ver["fifa_version"], y=by_ver["MA_3"],
        name="3-Edition MA",
        line=dict(color=ORANGE, width=3),
    ))

    fig.update_layout(
        title="Average Overall Rating per FIFA Edition<br><sup>Line + Moving Average Overlay</sup>",
        xaxis_title="FIFA Edition",
        yaxis_title="Average Overall Rating",
        paper_bgcolor="white", plot_bgcolor="white", font_color="black",
        xaxis=dict(gridcolor="lightgrey", linecolor="black",
                   tickvals=versions, ticktext=[str(v) for v in versions]),
        yaxis=dict(gridcolor="lightgrey", linecolor="black"),
        shapes=[dict(type="rect", xref="paper", yref="paper",
                     x0=0, y0=0, x1=1, y1=1, line=dict(color="black", width=2))],
        legend=dict(bgcolor="white", bordercolor="black", borderwidth=1,
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=80, r=80, b=70, l=70),
    )
    return fig


if __name__ == "__main__":
    df = load_data()
    make_line_overall_by_edition(df).show()
    make_line_normalised_trends(df).show()
    make_line_moving_average(df).show()
    print("✅ Line charts rendered.")
