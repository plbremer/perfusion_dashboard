import dash
from dash import dcc, html, dash_table, callback, ctx
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
import io
import pandas as pd

from config import UNIT_DICT

dash.register_page(__name__, path='/unit-manager')



layout = html.Div(
    children=[
        html.Br(),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(width=4),
                dbc.Col(
                    children=[
                        dash_table.DataTable(
                            id='datatable_units',
                            # columns=column_list,
                            columns=[
                                {
                                    'id':'parameter',
                                    'name':'Parameter'
                                },
                                {
                                    'id':'unit',
                                    'name':'Unit'
                                },
                            ],
                            data=[
                                {
                                    'parameter':temp_key,
                                    'unit':UNIT_DICT[temp_key]
                                } for temp_key in UNIT_DICT.keys()
                            ],
                            markdown_options={"link_target": "_blank"},
                            # page_current=0,
                            # page_size=50,
                            # page_action='native',
                            # sort_action='native',
                            # sort_mode='multi',
                            # filter_action='native',
                            style_cell={
                                'fontSize': 17,
                                'padding': '8px',
                                'textAlign': 'center'
                            },
                            style_header={
                                'font-family': 'arial',
                                'fontSize': 15,
                                'fontWeight': 'bold',
                                'textAlign': 'center'
                            },
                            style_data={
                                'textAlign': 'center',
                                'fontWeight': 'bold',
                                'font-family': 'Roboto',
                                'fontSize': 15,
                            },
                        )
                    ],
                    width=4
                ),
                dbc.Col(width=4)
            ]
        )


    ],
)