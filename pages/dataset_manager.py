import dash
from dash import dcc, html, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/content/a537f01f-de6f-4093-b216-89fef5cfba1b/dataset-manager')

def create_shorthand_string(temp_string):
    shorthand_list=temp_string.split(' ')[0:2]
    return ' '.join(shorthand_list)


layout = html.Div(
    children=[
        html.Br(),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(width=4),
                dbc.Col(
                    children=[
                        dcc.Upload(
                            id='upload_dataset',
                            children=html.Div([
                                'Upload Dataset',
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            },
                        ),
                    ],
                    width=4
                ),
                dbc.Col(width=4)
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(width=4),
                dbc.Col(
                    children=[
                        dash_table.DataTable(
                            id='datatable_dataset',
                            # columns=column_list,
                            columns=[{'id':'hi','name':'hi'}],
                            # data=data,
                            markdown_options={"link_target": "_blank"},
                            page_current=0,
                            page_size=50,
                            page_action='native',
                            sort_action='native',
                            sort_mode='multi',
                            filter_action='native',
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