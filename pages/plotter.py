import dash
from dash import dcc, html, dash_table, callback, ctx
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
import io
import pandas as pd
import itertools
import numpy as np
from pprint import pprint

from config import UNIT_DICT,DATAFRAME_DICT,UNIT_DICT_BIOCHEMISTRY,DATAFRAME_DICT_BIOCHEMISTRY

dash.register_page(__name__, path='/plotter')

def create_shorthand_string(temp_string):
    shorthand_list=temp_string.split(' ')[0:2]
    return ' '.join(shorthand_list)

def create_shorthand_string_biochemistry(temp_string):
    '''
    '''
    return temp_string.split(': ')[1]
    # return temp_string


layout = html.Div(
    children=[
        html.Br(),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(
                    width=0
                ),
                dbc.Col(
                    html.H2("Metra Data"),
                    style={'textAlign': 'center'},
                    width=5
                ),
                dbc.Col(
                    width=0
                ),
                dbc.Col(
                    html.H2("Biochemistry Data"),
                    style={'textAlign': 'center'},
                    width=5
                ),
                dbc.Col(
                    width=0
                ),
            ]
        ),
        html.Br(),
        
        dbc.Row(
            children=[
                dbc.Col(
                    width=0
                ),
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dbc.Row(
                                        html.H3('Choose What Data Get Plottted')
                                    ),
                                    html.Br(),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(width=1),
                                            dbc.Col(
                                                children=[
                                                    dbc.Button('Clear Checkboxes', id='button_clear_checkboxes')
                                                ],
                                                width=2
                                            ),
                                            dbc.Col(width=2),
                                            dbc.Col(
                                                children=[
                                                    dbc.Button('Clear Traces', id='button_clear_traces')  
                                                ],
                                                width=2
                                            ),
                                            dbc.Col(width=2),
                                            dbc.Col(
                                                children=[
                                                    dbc.Button('Clear All', id='button_clear_all')  
                                                ],
                                                width=2
                                            ),
                                            dbc.Col(width=1)
                                        ]
                                    ),
                                    html.Br(),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(
                                                dcc.Checklist(
                                                    id='checklist_dataset',
                                                    options=[]
                                                ),
                                                width=6
                                            ),
                                            dbc.Col(
                                                dcc.Checklist(
                                                    id='checklist_parameters',
                                                    options=[]
                                                ),
                                                width=6
                                            )
                                        ]
                                    ),
                                    html.Br(),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(width=5),
                                            dbc.Col(
                                                children=[
                                                    dbc.Button('Add Trace', id='button_add_trace')
                                                ],
                                                width=3
                                            ),
                                            dbc.Col(width=3)
                                        ]
                                    ),
                                    html.Br(),
                                    dbc.Row(
                                        children=[
                                            dash_table.DataTable(
                                                id='datatable_traces',
                                                # columns=column_list,
                                                columns=[
                                                    {
                                                        'id':'dataset_filename',
                                                        'name':'Dataset Filename'
                                                    },
                                                    {
                                                        'id':'dataset_shorthand',
                                                        'name':'Dataset Shorthand'
                                                    },
                                                    {
                                                        'id':'dataset_parameter',
                                                        'name':'Dataset Parameter'
                                                    },
                                                ],
                                                data=[],
                                                markdown_options={"link_target": "_blank"},
                                                style_cell={
                                                    'fontSize': 17,
                                                    'padding': '8px',
                                                    'textAlign': 'left',
                                                    'textOverflow': 'ellipsis',
                                                    'maxWidth':0
                                                },
                                                style_header={
                                                    'font-family': 'arial',
                                                    'fontSize': 15,
                                                    'fontWeight': 'bold',
                                                    'textAlign': 'center'
                                                },
                                                style_data={
                                                    'textAlign': 'left',
                                                    'fontWeight': 'bold',
                                                    'font-family': 'Roboto',
                                                    'fontSize': 15,
                                                },
                                                row_deletable=True
                                            )
                                        ]
                                    )
                                ]
                            )
                        ),
                    ],
                    width=5
                ),
                dbc.Col(
                    width=0
                ),
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    dbc.Row(
                                        html.H3('Choose What Data Get Plottted')
                                    ),
                                    html.Br(),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(width=1),
                                            dbc.Col(
                                                children=[
                                                    dbc.Button('Clear Checkboxes', id='button_clear_checkboxes_biochemistry')
                                                ],
                                                width=2
                                            ),
                                            dbc.Col(width=2),
                                            dbc.Col(
                                                children=[
                                                    dbc.Button('Clear Traces', id='button_clear_traces_biochemistry')  
                                                ],
                                                width=2
                                            ),
                                            dbc.Col(width=2),
                                            dbc.Col(
                                                children=[
                                                    dbc.Button('Clear All', id='button_clear_all_biochemistry')  
                                                ],
                                                width=2
                                            ),
                                            dbc.Col(width=1)
                                        ]
                                    ),
                                    html.Br(),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(
                                                dcc.Checklist(
                                                    id='checklist_dataset_biochemistry',
                                                    options=[]
                                                ),
                                                width=6
                                            ),
                                            dbc.Col(
                                                dcc.Checklist(
                                                    id='checklist_parameters_biochemistry',
                                                    options=[]
                                                ),
                                                width=6
                                            )
                                        ]
                                    ),
                                    html.Br(),
                                    dbc.Row(
                                        children=[
                                            dbc.Col(width=5),
                                            dbc.Col(
                                                children=[
                                                    dbc.Button('Add Trace', id='button_add_trace_biochemistry')
                                                ],
                                                width=3
                                            ),
                                            dbc.Col(width=3)
                                        ]
                                    ),
                                    html.Br(),
                                    dbc.Row(
                                        children=[
                                            dash_table.DataTable(
                                                id='datatable_traces_biochemistry',
                                                # columns=column_list,
                                                columns=[
                                                    {
                                                        'id':'dataset_filename',
                                                        'name':'Dataset Filename'
                                                    },
                                                    {
                                                        'id':'dataset_shorthand',
                                                        'name':'Dataset Shorthand'
                                                    },
                                                    {
                                                        'id':'dataset_parameter',
                                                        'name':'Dataset Parameter'
                                                    },
                                                ],
                                                data=[],
                                                markdown_options={"link_target": "_blank"},
                                                style_cell={
                                                    'fontSize': 17,
                                                    'padding': '8px',
                                                    'textAlign': 'left',
                                                    'textOverflow': 'ellipsis',
                                                    'maxWidth':0
                                                },
                                                style_header={
                                                    'font-family': 'arial',
                                                    'fontSize': 15,
                                                    'fontWeight': 'bold',
                                                    'textAlign': 'center'
                                                },
                                                style_data={
                                                    'textAlign': 'left',
                                                    'fontWeight': 'bold',
                                                    'font-family': 'Roboto',
                                                    'fontSize': 15,
                                                },
                                                row_deletable=True
                                            )
                                        ]
                                    )
                                ]
                            )
                        ),
                    ],
                    width=5
                ),
                dbc.Col(
                    width=1
                )        
            ]
        ),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(
                    width=0
                ),
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                children=[                               
                                    html.H3('Choose Scatter Details'),
                                    html.Br(),
                                    html.H6('Time Subsampling'),
                                    dbc.RadioItems(
                                        id="radioitems_timesampling",
                                        className="btn-group",
                                        inputClassName="btn-check",
                                        labelClassName="btn btn-outline-primary",
                                        labelCheckedClassName="active",
                                        options=[
                                            {"label": "Every Second", "value": 1},
                                            {"label": "Every Minute", "value": 60},
                                            {"label": "Every Five Minutes", "value": 300},
                                            {"label": "Every Half-hour", "value": 1800},
                                            {"label": "Every Hour", "value": 3600},
                                        ],
                                        value=60,
                                    ),
                                    html.Br(),
                                    html.H6('Interpolation'),
                                    dbc.RadioItems(
                                        id="radioitems_interpolation",
                                        className="btn-group",
                                        inputClassName="btn-check",
                                        labelClassName="btn btn-outline-primary",
                                        labelCheckedClassName="active",
                                        options=[
                                            {"label": "No Interpolation", "value": 'no_interpolation'},
                                            {"label": "Interpolation", "value": 'interpolation'},
                                        ],
                                        value='no_interpolation',
                                    ),
                                    html.Br(),
                                    html.H6('Negatives to Zero'),
                                    dbc.RadioItems(
                                        id="radioitems_negatives_to_zero",
                                        className="btn-group",
                                        inputClassName="btn-check",
                                        labelClassName="btn btn-outline-primary",
                                        labelCheckedClassName="active",
                                        options=[
                                            {"label": "Negatives to Zero", "value": 'change_values'},
                                            {"label": "Do not change values", "value": 'dont_change_values'},
                                        ],
                                        value='dont_change_values',
                                    ),
                                ]
                            )
                        )
                    ],
                    width=5
                ),
                dbc.Col(
                    width=0
                ),
                dbc.Col(
                    children=[
                        dbc.Card(
                            dbc.CardBody(
                                children=[                               
                                    html.H3('Choose Scatter Details'),
                                    html.Br(),
                                    # html.H6('Time Subsampling'),
                                    # dbc.RadioItems(
                                    #     id="radioitems_timesampling",
                                    #     className="btn-group",
                                    #     inputClassName="btn-check",
                                    #     labelClassName="btn btn-outline-primary",
                                    #     labelCheckedClassName="active",
                                    #     options=[
                                    #         {"label": "Every Second", "value": 1},
                                    #         {"label": "Every Minute", "value": 60},
                                    #         {"label": "Every Five Minutes", "value": 300},
                                    #         {"label": "Every Half-hour", "value": 1800},
                                    #         {"label": "Every Hour", "value": 3600},
                                    #     ],
                                    #     value=60,
                                    # ),
                                    html.Br(),
                                    html.H6('Interpolation'),
                                    dbc.RadioItems(
                                        id="radioitems_interpolation_biochemistry",
                                        className="btn-group",
                                        inputClassName="btn-check",
                                        labelClassName="btn btn-outline-primary",
                                        labelCheckedClassName="active",
                                        options=[
                                            {"label": "No Interpolation", "value": 'no_interpolation'},
                                            {"label": "Interpolation", "value": 'interpolation'},
                                        ],
                                        value='no_interpolation',
                                    ),
                                    html.Br(),
                                    html.H6('Negatives to Zero'),
                                    dbc.RadioItems(
                                        id="radioitems_negatives_to_zero_biochemistry",
                                        className="btn-group",
                                        inputClassName="btn-check",
                                        labelClassName="btn btn-outline-primary",
                                        labelCheckedClassName="active",
                                        options=[
                                            {"label": "Negatives to Zero", "value": 'change_values'},
                                            {"label": "Do not change values", "value": 'dont_change_values'},
                                        ],
                                        value='dont_change_values',
                                    ),
                                ]
                            )
                        )
                    ],
                    width=5
                ),
                dbc.Col(
                    width=1
                )        
            ]
        ),
        html.Br(),
        dbc.Row(
            children=[
                # dbc.Col(
                #     width=0
                # ),
                dbc.Col(
                    children=[
                        dbc.Row(
                            children=[
                                dbc.Col(width=5),
                                dbc.Col(
                                    children=[
                                        dbc.Button('Render Plot', id='button_render_plot')  
                                    ],
                                    width=2
                                ),
                                dbc.Col(width=5),
                                
                            ]
                        ),
                        dbc.Row(
                            dcc.Graph(
                                id='main_plot',
                                style={'height':'80vh'}
                            )
                        )
                    ],
                    width=6
                ),
                # dbc.Col(
                #     width=0
                # ),
                dbc.Col(
                    children=[
                        dbc.Row(
                            children=[
                                dbc.Col(width=5),
                                dbc.Col(
                                    children=[
                                        dbc.Button('Render Plot', id='button_render_plot_biochemistry')  
                                    ],
                                    width=2
                                ),
                                dbc.Col(width=5),
                            ]
                        ),
                        dbc.Row(
                            dcc.Graph(
                                id='main_plot_biochemistry',
                                style={'height':'80vh'}
                            )
                        )
                    ],
                    width=6
                ),
                # dbc.Col(
                #     width=0
                # )        
            ]
        ),
    ],
)


def generate_yaxis_options():
    global DATAFRAME_DICT
    if len(DATAFRAME_DICT.keys())>0:
        yaxis_options=list()
        total_column_set=set()
        for temp_dataset in DATAFRAME_DICT.values():
            total_column_set=total_column_set.union(set(temp_dataset.columns.tolist()))
        for temp_column in total_column_set:
            if temp_column in UNIT_DICT.keys():
                yaxis_options.append(
                    {
                        'label': temp_column,
                        'value': temp_column
                    }
                )
        yaxis_options=sorted(yaxis_options,key=lambda x:x['label'])
    else:
        yaxis_options=list()
    return yaxis_options


@callback(
    [
        Output(component_id='checklist_dataset', component_property='options'),
        Output(component_id='checklist_parameters', component_property='options')
    ],
    [
        Input(component_id='url', component_property="pathname")
    ]
)
def update_trace_selection_options(
    # store_dataset_keys_and_columns_data,
    url_pathname
):

    global DATAFRAME_DICT

    if len(DATAFRAME_DICT.keys())==0:
        return [list(),list()]

    output_dict={
        'dataset_filename':[],
        'dataset_shorthand':[],
        'dataset_parameter':[]
    }

    for temp_key in DATAFRAME_DICT.keys():
        output_dict['dataset_filename'].append(
            temp_key
        )
        output_dict['dataset_shorthand'].append(
            create_shorthand_string(temp_key)
        )

    output_dict['dataset_parameter']=generate_yaxis_options()

    #this is a little silly and non-minimal but whatever
    checklist_dataset_options=[]
    for i in range(len(output_dict['dataset_filename'])):
        checklist_dataset_options.append(
            {
                'label': output_dict['dataset_shorthand'][i],
                'value': output_dict['dataset_filename'][i]
            }
        )


    return [checklist_dataset_options,output_dict['dataset_parameter']]


@callback(
    [
        Output(component_id="checklist_dataset", component_property="value"),
        Output(component_id="checklist_parameters", component_property="value"),
    ],
    [
        Input(component_id='button_clear_checkboxes', component_property="n_clicks"),
        Input(component_id='button_clear_all', component_property="n_clicks"),
    ],
    prevent_initial_call=True,
)
def clear_checkboxes(
        button_clear_checkboxes_n_clicks,
        button_clear_all_n_clicks
):
    return [[],[]]


@callback(
    [
        Output(component_id='datatable_traces', component_property='data'),
    ],
    [
        Input(component_id="button_add_trace", component_property="n_clicks"),
        Input(component_id="button_clear_traces", component_property="n_clicks"),
        Input(component_id='button_clear_all', component_property="n_clicks"),
    ],
    [
        State(component_id="datatable_traces", component_property="data"),
        State(component_id="checklist_dataset", component_property="value"),
        State(component_id="checklist_parameters", component_property="value"),
    ],
    prevent_initial_call=True,
)
def add_traces_to_datatable(
    button_add_trace_n_clicks,
    button_clear_traces_n_clicks,
    button_clear_all_n_clicks,
    datatable_traces_data,
    checklist_dataset_value,
    checklist_parameters_value,
):

    if ctx.triggered_id=='button_clear_traces' or ctx.triggered_id=='button_clear_all':
        return [[]]

    new_traces=list()
    for temp_dataset in checklist_dataset_value:
        for temp_parameter in checklist_parameters_value:

            new_traces.append(
                {
                    'dataset_filename':temp_dataset,
                    'dataset_shorthand':create_shorthand_string(temp_dataset),
                    'dataset_parameter':temp_parameter
                }
            )

    output_traces=datatable_traces_data+new_traces

    temp_panda=pd.DataFrame.from_records(output_traces)
    temp_panda.drop_duplicates(inplace=True)
    output_traces=temp_panda.to_dict(orient='records')
    return [output_traces]

def determine_y_axis_string_value(datatable_traces_data):
    global UNIT_DICT
    y_axis_terms=set()
    for temp_row in datatable_traces_data:
        try:
            y_axis_terms=y_axis_terms.union(
               {UNIT_DICT[temp_row['dataset_parameter']]}
            )
        except KeyError:
            y_axis_terms=y_axis_terms.union(
                {'Parameter Column Does Not Match Unit Dict Parameters'}
            )
    return ', '.join(y_axis_terms)
                                                

@callback(
    [
        Output(component_id='main_plot', component_property='figure'),
    ],
    [
        Input(component_id="button_render_plot", component_property="n_clicks"),
        Input(component_id='button_clear_all', component_property="n_clicks"),
    ],
    [
        State(component_id="datatable_traces", component_property="data"),


        State(component_id="radioitems_timesampling", component_property="value"),
        State(component_id="radioitems_interpolation", component_property="value"),
        State(component_id="radioitems_negatives_to_zero", component_property="value")
    ],
    prevent_initial_call=True,
)
def add_traces_to_scatter(
    button_render_plot_n_clicks,
    button_clear_all_n_clicks,

    datatable_traces_data,

    radioitems_timesampling_value,
    radioitems_interpolation_value,
    radioitems_negatives_to_zero_value
):
    if ctx.triggered_id=='button_clear_all':
        return [{}]
    
    
    global DATAFRAME_DICT
    global UNIT_DICT    

    if len(datatable_traces_data)==0:
        raise PreventUpdate

    traces_list=list()

    for temp_row in datatable_traces_data:
        temp_shorthand_string=temp_row['dataset_shorthand']+': '+temp_row['dataset_parameter']
        
        traces_list.append(
            np.array(
                [
                    DATAFRAME_DICT[temp_row['dataset_filename']].index[::radioitems_timesampling_value],
                    DATAFRAME_DICT[temp_row['dataset_filename']][temp_row['dataset_parameter']][::radioitems_timesampling_value],
                    [temp_shorthand_string for i in range(0,len(DATAFRAME_DICT[temp_row['dataset_filename']].index),radioitems_timesampling_value)]
                ]
            ).T
        )

    traces=np.vstack(traces_list)

    #adjust the x axis to something reasonable
    if radioitems_timesampling_value>59 and radioitems_timesampling_value<301:
        traces[:,0]=traces[:,0].astype(int)/60
    elif radioitems_timesampling_value>=301:
        traces[:,0]=traces[:,0].astype(int)/3600
    #     concat_list.append(
    #         DATAFRAME_DICT[temp_row['dataset_filename']][temp_row['parameter']]
    #     )

    if radioitems_negatives_to_zero_value=='change_values':
        traces[:,1]=np.where(
            traces[:,1].astype(float)<0,
            0,
            traces[:,1].astype(float)
        )


    downsampling_mask=np.zeros(len(traces),dtype=int)
    downsampling_mask[:100000]=1
    np.random.shuffle(downsampling_mask)
    downsampling_mask=downsampling_mask.astype(bool)
    traces=traces[downsampling_mask]

    if radioitems_interpolation_value=='no_interpolation':
        temp_figure=px.scatter(
            x=traces[:,0].astype(float),
            y=traces[:,1].astype(float),
            color=traces[:,2],
            opacity=0.5
        )
    elif radioitems_interpolation_value=='interpolation':
        temp_figure=px.line(
            x=traces[:,0].astype(float),
            y=traces[:,1].astype(float),
            color=traces[:,2]
            # opacity=0.01*slider_opacity_percent_value
        )

    if radioitems_timesampling_value<=59 :
        temp_figure.update_layout(
            xaxis_title="Seconds"
        )
    elif radioitems_timesampling_value>59 and radioitems_timesampling_value<301:
        temp_figure.update_layout(
            xaxis_title="Minutes"
        )
    elif radioitems_timesampling_value>=301:
        temp_figure.update_layout(
            xaxis_title="Hours"
        )

    y_axis_string_value=determine_y_axis_string_value(datatable_traces_data)
    temp_figure.update_layout(
        yaxis_title=y_axis_string_value
    )

    temp_figure.update_traces(marker=dict(size=5))

    temp_figure.update_layout(
        font=dict(
            size=14
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return [temp_figure]








############################################################
############################################################
############################################################
########################################biochemistry analogs
############################################################
############################################################
############################################################
def generate_yaxis_options_biochemistry():
    global DATAFRAME_DICT_BIOCHEMISTRY
    if len(DATAFRAME_DICT_BIOCHEMISTRY.keys())>0:
        yaxis_options=list()
        total_column_set=set()
        for temp_dataset in DATAFRAME_DICT_BIOCHEMISTRY.values():
            total_column_set=total_column_set.union(set(temp_dataset.columns.tolist()))
        for temp_column in total_column_set:
            if temp_column in UNIT_DICT_BIOCHEMISTRY.keys():
                yaxis_options.append(
                    {
                        'label': temp_column,
                        'value': temp_column
                    }
                )
        yaxis_options=sorted(yaxis_options,key=lambda x:x['label'])
    else:
        yaxis_options=list()
    return yaxis_options



@callback(
    [
        Output(component_id='checklist_dataset_biochemistry', component_property='options'),
        Output(component_id='checklist_parameters_biochemistry', component_property='options')
    ],
    [
        Input(component_id='url', component_property="pathname")
    ]
)
def update_trace_selection_options_biochemistry(
    # store_dataset_keys_and_columns_data,
    url_pathname
):

    global DATAFRAME_DICT_BIOCHEMISTRY

    if len(DATAFRAME_DICT_BIOCHEMISTRY.keys())==0:
        return [list(),list()]

    output_dict={
        'dataset_filename':[],
        'dataset_shorthand':[],
        'dataset_parameter':[]
    }

    for temp_key in DATAFRAME_DICT_BIOCHEMISTRY.keys():
        output_dict['dataset_filename'].append(
            temp_key
        )
        output_dict['dataset_shorthand'].append(
            create_shorthand_string_biochemistry(temp_key)
        )

    output_dict['dataset_parameter']=generate_yaxis_options_biochemistry()

    #this is a little silly and non-minimal but whatever
    checklist_dataset_options=[]
    for i in range(len(output_dict['dataset_filename'])):
        checklist_dataset_options.append(
            {
                'label': output_dict['dataset_shorthand'][i],
                'value': output_dict['dataset_filename'][i]
            }
        )
    # pprint(output_dict)

    return [checklist_dataset_options,output_dict['dataset_parameter']]





@callback(
    [
        Output(component_id="checklist_dataset_biochemistry", component_property="value"),
        Output(component_id="checklist_parameters_biochemistry", component_property="value"),
    ],
    [
        Input(component_id='button_clear_checkboxes_biochemistry', component_property="n_clicks"),
        Input(component_id='button_clear_all_biochemistry', component_property="n_clicks"),
    ],
    prevent_initial_call=True,
)
def clear_checkboxes_biochemistry(
        button_clear_checkboxes_n_clicks,
        button_clear_all_n_clicks
):
    return [[],[]]



@callback(
    [
        Output(component_id='datatable_traces_biochemistry', component_property='data'),
    ],
    [
        Input(component_id="button_add_trace_biochemistry", component_property="n_clicks"),
        Input(component_id="button_clear_traces_biochemistry", component_property="n_clicks"),
        Input(component_id='button_clear_all_biochemistry', component_property="n_clicks"),
    ],
    [
        State(component_id="datatable_traces_biochemistry", component_property="data"),
        State(component_id="checklist_dataset_biochemistry", component_property="value"),
        State(component_id="checklist_parameters_biochemistry", component_property="value"),
    ],
    prevent_initial_call=True,
)
def add_traces_to_datatable_biochemistry(
    button_add_trace_n_clicks,
    button_clear_traces_n_clicks,
    button_clear_all_n_clicks,
    datatable_traces_data,
    checklist_dataset_value,
    checklist_parameters_value,
):

    if ctx.triggered_id=='button_clear_traces_biochemistry' or ctx.triggered_id=='button_clear_all_biochemistry':
        return [[]]

    new_traces=list()
    for temp_dataset in checklist_dataset_value:
        for temp_parameter in checklist_parameters_value:

            new_traces.append(
                {
                    'dataset_filename':temp_dataset,
                    'dataset_shorthand':create_shorthand_string_biochemistry(temp_dataset),
                    'dataset_parameter':temp_parameter
                }
            )

    output_traces=datatable_traces_data+new_traces

    temp_panda=pd.DataFrame.from_records(output_traces)
    temp_panda.drop_duplicates(inplace=True)
    output_traces=temp_panda.to_dict(orient='records')
    return [output_traces]

def determine_y_axis_string_value_biochemistry(datatable_traces_data):
    global UNIT_DICT_BIOCHEMISTRY
    pprint(UNIT_DICT_BIOCHEMISTRY)
    print(datatable_traces_data)
    y_axis_terms=set()
    for temp_row in datatable_traces_data:
        try:
            y_axis_terms=y_axis_terms.union(
               {UNIT_DICT_BIOCHEMISTRY[temp_row['dataset_parameter']]}
            )
        except KeyError:
            y_axis_terms=y_axis_terms.union(
                {'Parameter Column Does Not Match Unit Dict Parameters'}
            )
    return ', '.join(y_axis_terms)
                      




@callback(
    [
        Output(component_id='main_plot_biochemistry', component_property='figure'),
    ],
    [
        Input(component_id="button_render_plot_biochemistry", component_property="n_clicks"),
        Input(component_id='button_clear_all_biochemistry', component_property="n_clicks"),
    ],
    [
        State(component_id="datatable_traces_biochemistry", component_property="data"),
        State(component_id="radioitems_interpolation_biochemistry", component_property="value"),
        State(component_id="radioitems_negatives_to_zero_biochemistry", component_property="value")
    ],
    prevent_initial_call=True,
)
def add_traces_to_scatter(
    button_render_plot_n_clicks,
    button_clear_all_n_clicks,

    datatable_traces_data,
    radioitems_interpolation_value,
    radioitems_negatives_to_zero_value
):
    if ctx.triggered_id=='button_clear_all_biochemistry':
        return [{}]
    
    
    global DATAFRAME_DICT_BIOCHEMISTRY
    global UNIT_DICT_BIOCHEMISTRY   

    if len(datatable_traces_data)==0:
        raise PreventUpdate

    traces_list=list()

    print('---')
    #pprint(datatable_traces_data)
    pprint(DATAFRAME_DICT_BIOCHEMISTRY['sheet: Liver 8'].columns)

    for temp_row in datatable_traces_data:
        temp_shorthand_string=temp_row['dataset_shorthand']+': '+temp_row['dataset_parameter']
        
        traces_list.append(
            np.array(
                [
                    DATAFRAME_DICT_BIOCHEMISTRY[temp_row['dataset_filename']]['Time from perfusion onset (h)'],
                    DATAFRAME_DICT_BIOCHEMISTRY[temp_row['dataset_filename']][temp_row['dataset_parameter']],
                    [temp_shorthand_string for i in range(0,len(DATAFRAME_DICT_BIOCHEMISTRY[temp_row['dataset_filename']].index))]
                ]
            ).T
        )

    traces=np.vstack(traces_list)

    #adjust the x axis to something reasonable
    # if radioitems_timesampling_value>59 and radioitems_timesampling_value<301:
    #     traces[:,0]=traces[:,0].astype(int)/60
    # elif radioitems_timesampling_value>=301:
    #     traces[:,0]=traces[:,0].astype(int)/3600
    #     concat_list.append(
    #         DATAFRAME_DICT_BIOCHEMISTRY[temp_row['dataset_filename']][temp_row['parameter']]
    #     )

    if radioitems_negatives_to_zero_value=='change_values':
        traces[:,1]=np.where(
            traces[:,1].astype(float)<0,
            0,
            traces[:,1].astype(float)
        )


    downsampling_mask=np.zeros(len(traces),dtype=int)
    downsampling_mask[:100000]=1
    np.random.shuffle(downsampling_mask)
    downsampling_mask=downsampling_mask.astype(bool)
    traces=traces[downsampling_mask]

    pprint(traces)

    if radioitems_interpolation_value=='no_interpolation':
        temp_figure=px.scatter(
            x=traces[:,0].astype(float),
            y=traces[:,1].astype(float),
            color=traces[:,2],
            opacity=0.5
        )
    elif radioitems_interpolation_value=='interpolation':
        temp_figure=px.line(
            x=traces[:,0].astype(float),
            y=traces[:,1].astype(float),
            color=traces[:,2]
            # connectgaps=True
            # opacity=0.01*slider_opacity_percent_value
        )
        temp_figure.update_traces(connectgaps=True)

    # if radioitems_timesampling_value<=59 :
    #     temp_figure.update_layout(
    #         xaxis_title="Seconds"
    #     )
    # elif radioitems_timesampling_value>59 and radioitems_timesampling_value<301:
    #     temp_figure.update_layout(
    #         xaxis_title="Minutes"
    #     )
    # elif radioitems_timesampling_value>=301:
    temp_figure.update_layout(
        xaxis_title="Hours"
    )

    y_axis_string_value=determine_y_axis_string_value_biochemistry(datatable_traces_data)
    temp_figure.update_layout(
        yaxis_title=y_axis_string_value
    )

    temp_figure.update_traces(marker=dict(size=5))

    temp_figure.update_layout(
        font=dict(
            size=14
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return [temp_figure]
