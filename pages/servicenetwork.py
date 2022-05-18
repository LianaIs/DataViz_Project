import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from dash import callback, Input, Output

from utils import Header, make_dash_table
import pandas as pd
import pathlib

import folium
import json

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

# df_expenses = pd.read_csv(DATA_PATH.joinpath("df_expenses.csv"))
# df_minimums = pd.read_csv(DATA_PATH.joinpath("df_minimums.csv"))

df_melted = pd.read_csv(DATA_PATH.joinpath("df_melted.csv"))

df_pca = pd.read_csv(DATA_PATH.joinpath("df_pca.csv"))
days = df_pca['Y-M'].unique()
banks = df_pca['Banks name'].unique()


def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 4
            html.Div(
                [
                html.H6(
                                        ["Used indicators"], className="subtitle padded"
                                    ),
                html.Div([
                                                  dcc.Dropdown(
                                                                    id="dropdown",
                                                                    options=[{"label": x, "value": x} for x in days],
                                                                    value=days[0],
                                                                    clearable=False,
                                                                    style={"width": "80%"}
                                                                ),
#                                                   dcc.Dropdown(
                                            
#                                                                 list(df_pca['Y-M'].unique()), '2013_12' , id = 'Q',
#                                                                 ),
                                                  html.Div(id='dd-output-container')
                                                 ], className = 'six columns'),
                html.Div([
                                                  dcc.Dropdown(
                                                                    id="dropdown2",
                                                                    options=[{"label": x, "value": x} for x in banks],
                                                                    value=banks[0],
                                                                    clearable=False,
                                                                    style={"width": "80%"}
                                                                ),
#                                                   dcc.Dropdown(
                                            
#                                                                 list(df_pca['Y-M'].unique()), '2013_12' , id = 'Q',
#                                                                 ),
                                                  html.Div(id='dd-output-container1')
                                                 ], className = 'six columns'),
                html.H6(
                                        "# of beanches map",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-3",

                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                    
                    
        ],
        className="page",
    )


@callback(Output("graph-3", "figure"), [Input("dropdown", "value"), Input("dropdown2", "value")])
def update_bar_chart(day, bank):
    mask = (df_melted['Y-M'] == day) & (df_melted['Banks name'] == bank)
    m = folium.Map(location=[40.2, 44.6],zoom_start=8)
    for lat, lon, bank, value, variable in zip(df_melted[mask]['Lat'], df_melted[mask]['Lon'], df_melted[mask]['Banks name'], df_melted[mask]['value'], df_melted[mask]['variable']):
        folium.CircleMarker(
            [lat, lon],
            radius=value,
             popup = ('#: ' + str(value)
                     ),
            color='b',
            key_on = bank,
            threshold_scale=[0,1,2,3],
            fill_color='red',
            fill=True,
            fill_opacity=0.7
            ).add_to(m)
    return m


