import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
from dash import callback, Input, Output

from utils import Header, make_dash_table

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()


df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))

df = pd.read_csv(DATA_PATH.joinpath("Competitors_Data_smp.csv"))
cols = ['LoanPortfolio(net)','TotalAssets', 'TotalLiabilities', 'TotalCapital',       
       'Liabilitiestocustomers(incl.securities)','Bonds Attracted','Netinterestincome','Net non-interest',
        'Profit/(loss)aftertax','NPL (%)_r', 'ROA\n(Annualized)', 'ROE\n(Annualized)','Cost of credit risk_r']

table = df[cols].describe().loc[['mean', 'min', 'max','std']].reset_index().pivot_table(columns = 'index', values = cols)
table = table.round(decimals=0)
table = table.reset_index().T.reset_index().T
# table = table.style.format("{:,.0f}")

df_pca = pd.read_csv(DATA_PATH.joinpath("df_pca.csv"))

days = df_pca['Y-M'].unique()

banks = df_pca['Banks name'].unique()

def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Methodology"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                     In this dashboard, for the purpose of comparison of Armenian banks, integral indices have been\
                                     constructed by the following three methods: sum of variables standardized by the min-max method,\
                                     method of calculating the z-score, standardization using the IQR. As a result of\
                                     the analysis, it became clear that each of the mentioned methods has certain limitations, which can\
                                     be overcomed in the case of the indexes obtained through PCA which will be used here.",
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Used indicators"], className="subtitle padded"
                                    ),
                                    html.Table(make_dash_table(table)),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Filters to apply",
                                        className="subtitle padded",
                                    ),
                                    html.Div([
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
                                        
                                     ], className = 'row'),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Hypothetical growth",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-2",
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                            
                            html.Div(
                                [
                                    html.H6(
                                        "Overall index performance",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-1",

                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                            
#                             html.Div(
#                                 [
#                                     html.H6(
#                                         "Risk Potential", className="subtitle padded"
#                                     ),
# #                                     html.Img(
# #                                         src=app.get_asset_url("risk_reward.png"),
# #                                         className="risk-reward",
# #                                     ),
#                                 ],
#                                 className="six columns",
#                             ),
                        ],
                        className="row ",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )

@callback(Output("graph-1", "figure"), Input("dropdown", "value"))
def update_bar_chart(day):
    mask = df_pca['Y-M'] == day
    fig = px.bar(df_pca[mask], x="Banks name", y="Index", barmode="group")
    fig.update_layout(plot_bgcolor="white")
    return fig

@callback(Output("graph-2", "figure"), Input("dropdown2", "value"))
def update_bar_chart1(bank):
    mask = df_pca['Banks name'] == bank
    fig = px.line(df_pca[mask], x='level_0', y='Index')
    fig.update_layout(plot_bgcolor="white")
    return fig  
    