"""
app.py — FIFA 23 Players Statistics Dashboard
Project 8: Data Visualization Final Project
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "charts"))

import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback_context
import dash_bootstrap_components as dbc

from charts.config import load_data
from charts.chart_01_column_bar        import make_column_chart, make_bar_chart
from charts.chart_02_stacked_clustered import (make_stacked_column, make_stacked_bar,
                                               make_clustered_column, make_clustered_bar)
from charts.chart_03_scatter           import make_scatter_pace_overall, make_scatter_age_value, make_scatter_custom
from charts.chart_04_bubble            import make_bubble_club, make_bubble_skills
from charts.chart_05_histogram         import make_histogram_overall, make_histogram_age, make_histogram_value, make_histogram_metric
from charts.chart_06_box               import make_box_overall_by_position, make_box_value_by_league, make_box_skills_notched, make_box_metric_by_position
from charts.chart_07_violin            import make_violin_overall_by_league, make_violin_age_by_league, make_violin_skills, make_violin_metric_by_league
from charts.chart_08_line              import make_line_overall_by_edition, make_line_normalised_trends, make_line_moving_average
from charts.chart_09_area              import make_area_single, make_area_stacked_positions, make_area_stacked_value

# ── Data ──────────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "male_players_cleaned.csv")
DF = load_data(DATA_PATH)

ALL_LEAGUES   = sorted(DF["league_name"].dropna().astype(str).unique())
ALL_POSITIONS = sorted(DF["player_positions"].dropna().unique())
ALL_VERSIONS  = sorted(DF["fifa_version"].dropna().unique())

# ── Colors ────────────────────────────────────────────────────────────────────
DARK_BG  = "#0D0D0D"
PANEL_BG = "#1A1A2E"
CARD_BG  = "#141414"
ACCENT   = "#00D4FF"
GOLD     = "#FFD700"
TEXT     = "#EAEAEA"
SUBTLE   = "#9B9B9B"

EMPTY_FIG = go.Figure().update_layout(
    paper_bgcolor="white", plot_bgcolor="white",
    annotations=[dict(text="No data — adjust filters", x=0.5, y=0.5,
                      xref="paper", yref="paper", showarrow=False,
                      font=dict(size=14, color="grey"))]
)


# ── Helpers ───────────────────────────────────────────────────────────────────
def _filter(lgs, pos, ovr, ver):
    lgs = lgs or ALL_LEAGUES
    pos = pos or ALL_POSITIONS
    ver = ver or ALL_VERSIONS
    return DF[
        DF["league_name"].isin(lgs) &
        DF["player_positions"].isin(pos) &
        DF["overall"].between(*ovr) &
        DF["fifa_version"].isin(ver)
    ]


def _btn(bid, label, color):
    return html.Button(label, id=bid, style={
        "fontSize":"10px","padding":"2px 7px","border":"none",
        "borderRadius":"3px","cursor":"pointer","marginLeft":"5px",
        "background":color,"color":"white","fontFamily":"Roboto,sans-serif",
    })


def _filter_row(label, id_all, id_none):
    return html.Div([
        html.Span(label, style={"color":ACCENT,"fontSize":"12px","fontWeight":"bold"}),
        _btn(id_all,  "All",  "#2196F3"),
        _btn(id_none, "None", "#FF5722"),
    ], style={"display":"flex","alignItems":"center","marginBottom":"4px"})


def section_card(title, *children):
    return html.Div([
        html.H4(title, style={"color":ACCENT,"fontSize":"12px","letterSpacing":"1.5px",
                               "textTransform":"uppercase","borderLeft":f"4px solid {GOLD}",
                               "paddingLeft":"10px","marginBottom":"14px"}),
        *children,
    ], style={"background":CARD_BG,"borderRadius":"10px","padding":"20px",
               "border":"1px solid #2A2A3A","marginBottom":"20px"})


# ── Sidebar ───────────────────────────────────────────────────────────────────
sidebar = html.Div([
    html.Div([
        html.H2("FIFA 23", style={"color":GOLD,"fontFamily":"Rajdhani,sans-serif",
                                   "textAlign":"center","margin":0,"fontSize":"28px"}),
        html.P("Players Analytics Dashboard",
               style={"color":SUBTLE,"textAlign":"center","fontSize":"11px",
                      "letterSpacing":"1px","marginTop":"4px"}),
    ], style={"marginBottom":"22px"}),

    _filter_row("🏆 League",   "btn-lg-all",  "btn-lg-none"),
    dcc.Dropdown(id="dd-league",
        options=[{"label":l,"value":l} for l in ALL_LEAGUES],
        value=ALL_LEAGUES, multi=True, clearable=False,
        style={"marginBottom":"14px","fontSize":"12px"}),

    _filter_row("🎯 Position", "btn-pos-all", "btn-pos-none"),
    dcc.Dropdown(id="dd-position",
        options=[{"label":p,"value":p} for p in ALL_POSITIONS],
        value=ALL_POSITIONS, multi=True, clearable=False,
        style={"marginBottom":"14px","fontSize":"12px"}),

    html.Label("⭐ Overall Range",
               style={"color":ACCENT,"fontSize":"12px","fontWeight":"bold"}),
    dcc.RangeSlider(id="slider-overall",
        min=int(DF.overall.min()), max=int(DF.overall.max()),
        value=[int(DF.overall.min()), int(DF.overall.max())],
        marks={50:"50",65:"65",80:"80",95:"95"},
        tooltip={"placement":"bottom","always_visible":False},
        className="mb-3"),

    _filter_row("📅 Edition",  "btn-ver-all", "btn-ver-none"),
    dcc.Checklist(id="cl-version",
        options=[{"label":f"  FIFA {v}","value":v} for v in ALL_VERSIONS],
        value=ALL_VERSIONS, inline=False,
        style={"color":TEXT,"fontSize":"12px","marginTop":"4px"},
        inputStyle={"marginRight":"6px","accentColor":ACCENT}),

    html.Hr(style={"borderColor":"#2A2A3A","margin":"18px 0 10px"}),
    html.Button("↺  Reset All Filters", id="btn-reset", style={
        "width":"100%","padding":"8px","fontSize":"12px","fontWeight":"bold",
        "background":"#2A2A3A","color":GOLD,
        "border":f"1px solid {GOLD}","borderRadius":"6px",
        "cursor":"pointer","fontFamily":"Roboto,sans-serif",
    }),
], style={
    "width":"240px","minHeight":"100vh","background":PANEL_BG,
    "padding":"24px 16px","position":"fixed","top":0,"left":0,
    "overflowY":"auto","borderRight":"1px solid #2A2A3A",
    "fontFamily":"Roboto,sans-serif",
})

# ── Dropdown options ──────────────────────────────────────────────────────────
dd_style = {"fontSize":"12px","marginBottom":"8px"}
dist_opts  = [("Overall","overall"),("Age","age"),("Value €M","value_M"),
              ("Pace","pace"),("Shooting","shooting"),("Passing","passing"),
              ("Dribbling","dribbling"),("Defending","defending"),("Physic","physic")]
skill_opts = [("Overall","overall"),("Pace","pace"),("Shooting","shooting"),
              ("Passing","passing"),("Dribbling","dribbling"),
              ("Defending","defending"),("Physic","physic")]
scatter_opts = dist_opts[:]

# ── Main layout ───────────────────────────────────────────────────────────────
main = html.Div([
    html.Div([
        html.H1("⚽ FIFA 23 Players Statistics Dashboard",
                style={"color":TEXT,"fontFamily":"Rajdhani,sans-serif",
                       "fontSize":"26px","margin":0}),
        html.P("Interactive scouting analytics  •  All 9 chart types  •  Dr. guidelines applied",
               style={"color":SUBTLE,"fontSize":"12px","margin":"4px 0 0"}),
    ], style={"borderBottom":"1px solid #2A2A3A","paddingBottom":"16px","marginBottom":"22px"}),

    # Week 1
    section_card("Week 1 — Column & Bar Charts",
        dbc.Row([dbc.Col(dcc.Graph(id="fig-col"),md=6),
                 dbc.Col(dcc.Graph(id="fig-bar"),md=6)])),

    # Week 2
    section_card("Week 2 — Stacked & Clustered Charts",
        html.Div([
            html.Label("Chart Type:", style={"color":SUBTLE,"fontSize":"12px"}),
            dcc.RadioItems(id="radio-w2",
                options=[{"label":" Stacked Column","value":"sc"},
                         {"label":" Stacked Bar",   "value":"sb"},
                         {"label":" Clustered Column","value":"cc"},
                         {"label":" Clustered Bar",  "value":"cb"}],
                value="sc", inline=True,
                style={"color":TEXT,"fontSize":"12px"},
                inputStyle={"marginRight":"5px","marginLeft":"12px","accentColor":ACCENT}),
        ], style={"marginBottom":"12px"}),
        dcc.Graph(id="fig-w2")),

    # Week 3
    section_card("Week 3 — Scatter Charts",
        dbc.Row([
            dbc.Col([html.Label("X-Axis:",style={"color":SUBTLE,"fontSize":"11px"}),
                     dcc.Dropdown(id="dd-sx",options=[{"label":l,"value":v} for l,v in scatter_opts],
                                  value="age",clearable=False,style=dd_style)],md=4),
            dbc.Col([html.Label("Y-Axis:",style={"color":SUBTLE,"fontSize":"11px"}),
                     dcc.Dropdown(id="dd-sy",options=[{"label":l,"value":v} for l,v in scatter_opts],
                                  value="overall",clearable=False,style=dd_style)],md=4),
            dbc.Col([html.Label("Color By:",style={"color":SUBTLE,"fontSize":"11px"}),
                     dcc.Dropdown(id="dd-sc",clearable=False,style=dd_style,
                         options=[{"label":"League","value":"league_name"},
                                  {"label":"Position","value":"player_positions"}],
                         value="league_name")],md=4),
        ], style={"marginBottom":"12px"}),
        dbc.Row([dbc.Col(dcc.Graph(id="fig-sc1"),md=6),
                 dbc.Col(dcc.Graph(id="fig-sc2"),md=6)])),

    # Week 4
    section_card("Week 4 — Bubble Charts",
        dbc.Row([dbc.Col(dcc.Graph(id="fig-bub1"),md=6),
                 dbc.Col(dcc.Graph(id="fig-bub2"),md=6)])),

    # Week 5
    section_card("Week 5 — Histogram",
        dbc.Row([dbc.Col([html.Label("Metric:",style={"color":SUBTLE,"fontSize":"12px"}),
                          dcc.Dropdown(id="dd-hist",
                              options=[{"label":l,"value":v} for l,v in dist_opts],
                              value="overall",clearable=False,style=dd_style)],md=4)],
                style={"marginBottom":"10px"}),
        dcc.Graph(id="fig-hist")),

    # Week 6
    section_card("Week 6 — Box Charts",
        dbc.Row([dbc.Col([html.Label("Metric:",style={"color":SUBTLE,"fontSize":"12px"}),
                          dcc.Dropdown(id="dd-box",
                              options=[{"label":l,"value":v} for l,v in skill_opts],
                              value="overall",clearable=False,style=dd_style)],md=4)],
                style={"marginBottom":"10px"}),
        dbc.Row([dbc.Col(dcc.Graph(id="fig-box1"),md=6),
                 dbc.Col(dcc.Graph(id="fig-box2"),md=6)])),

    # Week 7
    section_card("Week 7 — Violin Charts",
        dbc.Row([dbc.Col([html.Label("Metric:",style={"color":SUBTLE,"fontSize":"12px"}),
                          dcc.Dropdown(id="dd-vio",
                              options=[{"label":l,"value":v} for l,v in skill_opts],
                              value="overall",clearable=False,style=dd_style)],md=4)],
                style={"marginBottom":"10px"}),
        dbc.Row([dbc.Col(dcc.Graph(id="fig-vio1"),md=6),
                 dbc.Col(dcc.Graph(id="fig-vio2"),md=6)])),

    # Week 8
    section_card("Week 8 — Line Charts",
        dbc.Row([dbc.Col(dcc.Graph(id="fig-line1"),md=6),
                 dbc.Col(dcc.Graph(id="fig-line2"),md=6)]),
        dcc.Graph(id="fig-line3")),

    # Week 9
    section_card("Week 9 — Area Charts",
        dbc.Row([dbc.Col(dcc.Graph(id="fig-area1"),md=6),
                 dbc.Col(dcc.Graph(id="fig-area2"),md=6)]),
        dcc.Graph(id="fig-area3")),

    html.Div("FIFA 23 Complete Player Dataset  •  Plotly Dash  •  Data Visualization Project",
             style={"color":SUBTLE,"fontSize":"11px","textAlign":"center","padding":"20px 0"}),
], style={"marginLeft":"260px","padding":"28px",
           "background":DARK_BG,"minHeight":"100vh","fontFamily":"Roboto,sans-serif"})

# ── App ───────────────────────────────────────────────────────────────────────
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
           suppress_callback_exceptions=True)
app.title = "FIFA 23 | Players Dashboard"
app.layout = html.Div([sidebar, main], style={"background":DARK_BG})

INPUTS = [Input("dd-league","value"), Input("dd-position","value"),
          Input("slider-overall","value"), Input("cl-version","value")]


# ── Select All / None / Reset ─────────────────────────────────────────────────
@app.callback(Output("dd-league","value"),
              Input("btn-lg-all","n_clicks"), Input("btn-lg-none","n_clicks"),
              Input("btn-reset","n_clicks"), prevent_initial_call=True)
def toggle_leagues(*_):
    t = callback_context.triggered[0]["prop_id"].split(".")[0]
    return ALL_LEAGUES if t in ("btn-lg-all","btn-reset") else []

@app.callback(Output("dd-position","value"),
              Input("btn-pos-all","n_clicks"), Input("btn-pos-none","n_clicks"),
              Input("btn-reset","n_clicks"), prevent_initial_call=True)
def toggle_positions(*_):
    t = callback_context.triggered[0]["prop_id"].split(".")[0]
    return ALL_POSITIONS if t in ("btn-pos-all","btn-reset") else []

@app.callback(Output("cl-version","value"),
              Input("btn-ver-all","n_clicks"), Input("btn-ver-none","n_clicks"),
              Input("btn-reset","n_clicks"), prevent_initial_call=True)
def toggle_versions(*_):
    t = callback_context.triggered[0]["prop_id"].split(".")[0]
    return ALL_VERSIONS if t in ("btn-ver-all","btn-reset") else []


# ── Chart Callbacks ───────────────────────────────────────────────────────────
@app.callback(Output("fig-col","figure"), Output("fig-bar","figure"), *INPUTS)
def cb_w1(lgs,pos,ovr,ver):
    d = _filter(lgs,pos,ovr,ver)
    if d.empty: return EMPTY_FIG, EMPTY_FIG
    return make_column_chart(d), make_bar_chart(d)

@app.callback(Output("fig-w2","figure"), Input("radio-w2","value"), *INPUTS)
def cb_w2(ct,lgs,pos,ovr,ver):
    d = _filter(lgs,pos,ovr,ver)
    if d.empty: return EMPTY_FIG
    return {"sc":make_stacked_column,"sb":make_stacked_bar,
            "cc":make_clustered_column,"cb":make_clustered_bar}[ct](d)

@app.callback(Output("fig-sc1","figure"), Output("fig-sc2","figure"),
              Input("dd-sx","value"), Input("dd-sy","value"), Input("dd-sc","value"), *INPUTS)
def cb_w3(x,y,c,lgs,pos,ovr,ver):
    d = _filter(lgs,pos,ovr,ver)
    if d.empty: return EMPTY_FIG, EMPTY_FIG
    return make_scatter_custom(d,x,y,c), make_scatter_age_value(d)

@app.callback(Output("fig-bub1","figure"), Output("fig-bub2","figure"), *INPUTS)
def cb_w4(lgs,pos,ovr,ver):
    d = _filter(lgs,pos,ovr,ver)
    if d.empty: return EMPTY_FIG, EMPTY_FIG
    return make_bubble_club(d), make_bubble_skills(d)

@app.callback(Output("fig-hist","figure"), Input("dd-hist","value"), *INPUTS)
def cb_w5(metric,lgs,pos,ovr,ver):
    d = _filter(lgs,pos,ovr,ver)
    if d.empty: return EMPTY_FIG
    return make_histogram_metric(d, metric)

@app.callback(Output("fig-box1","figure"), Output("fig-box2","figure"),
              Input("dd-box","value"), *INPUTS)
def cb_w6(metric,lgs,pos,ovr,ver):
    d = _filter(lgs,pos,ovr,ver)
    if d.empty: return EMPTY_FIG, EMPTY_FIG
    return make_box_metric_by_position(d,metric), make_box_value_by_league(d)

@app.callback(Output("fig-vio1","figure"), Output("fig-vio2","figure"),
              Input("dd-vio","value"), *INPUTS)
def cb_w7(metric,lgs,pos,ovr,ver):
    d = _filter(lgs,pos,ovr,ver)
    if d.empty: return EMPTY_FIG, EMPTY_FIG
    return make_violin_metric_by_league(d,metric), make_violin_skills(d)

@app.callback(Output("fig-line1","figure"), Output("fig-line2","figure"),
              Output("fig-line3","figure"), *INPUTS)
def cb_w8(lgs,pos,ovr,ver):
    d = _filter(lgs,pos,ovr,ver)
    if d.empty: return EMPTY_FIG, EMPTY_FIG, EMPTY_FIG
    return (make_line_overall_by_edition(d),
            make_line_normalised_trends(d),
            make_line_moving_average(d))

@app.callback(Output("fig-area1","figure"), Output("fig-area2","figure"),
              Output("fig-area3","figure"), *INPUTS)
def cb_w9(lgs,pos,ovr,ver):
    d = _filter(lgs,pos,ovr,ver)
    if d.empty: return EMPTY_FIG, EMPTY_FIG, EMPTY_FIG
    return (make_area_single(d),
            make_area_stacked_positions(d),
            make_area_stacked_value(d))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
