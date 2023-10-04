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

from config import UNIT_DICT,DATAFRAME_DICT

# print(DATAFRAME_DICT.keys())

dash.register_page(__name__, path='/plotter')

def create_shorthand_string(temp_string):
    shorthand_list=temp_string.split(' ')[0:2]
    return ' '.join(shorthand_list)



layout = html.Div(
    children=[
        html.Br(),
        html.Br(),
        dbc.Row(
            children=[
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
                                            dbc.Col(width=3),
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
                                            dbc.Col(width=3)
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
                                                # page_current=0,
                                                # page_size=50,
                                                # page_action='native',
                                                # sort_action='native',
                                                # sort_mode='multi',
                                                # filter_action='native',
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
                        html.Br(),
                        # html.Br(),
                        # html.Br(),
                        # dbc.Card(
                        #     dbc.CardBody(
                        #         children=[
                                    
                        #         ]
                        #     )
                        # ),


                        # dbc.Row(
                        #     children=[
                        #         dbc.Col(width=2),
                        #         dbc.Col(
                        #             children=[
                        #                 html.H6('Time Subsampler'),
                        #                 dcc.Slider(
                        #                     id='slider_time_subsampler',
                        #                     # min=0,
                        #                     # max=60,
                        #                     # step=1,
                        #                     # step=None,
                        #                     marks={
                        #                         # 1: 'Every Second',
                        #                         # 60: 'Every Minute',
                        #                         # 300: 'Every Five Minutes',
                        #                         # 1800: 'Every half-hour',
                        #                         # 3600: 'Every hour'
                        #                         1: 'Every Second',
                        #                         2: 'Every Minute',
                        #                         3: 'Every Five Minutes',
                        #                         4: 'Every half-hour',
                        #                         5: 'Every hour'

                        #                     },
                        #                     vertical=True
                        #                     # value=0
                        #                 )
                        #             ]
                        #         ),
                        #         dbc.Col(width=2)
                        #     ]
                        # ),
                        dbc.Row(
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
                                                    # {"label": "Every Five Minutes", "value": 300},
                                                    # {"label": "Every Half-hour", "value": 1800},
                                                    # {"label": "Every Hour", "value": 3600},
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
                                                    # {"label": "Every Five Minutes", "value": 300},
                                                    # {"label": "Every Half-hour", "value": 1800},
                                                    # {"label": "Every Hour", "value": 3600},
                                                ],
                                                value='dont_change_values',
                                            ),
                                            html.Br(),
                                            html.H6('Dot Size'),
                                            dcc.Slider(
                                                id='slider_dot_size',
                                                min=1,
                                                max=30,
                                                step=2,
                                                # step=None,
                                                # marks={
                                                #     # 1: 'Every Second',
                                                #     # 60: 'Every Minute',
                                                #     # 300: 'Every Five Minutes',
                                                #     # 1800: 'Every half-hour',
                                                #     # 3600: 'Every hour'
                                                #     1: 'Every Second',
                                                #     2: 'Every Minute',
                                                #     3: 'Every Five Minutes',
                                                #     4: 'Every half-hour',
                                                #     5: 'Every hour'

                                                # },
                                                # vertical=True
                                                value=5
                                            ),
                                            html.Br(),
                                            html.H6('Opacity Percent'),
                                            dcc.Slider(
                                                id='slider_opacity_percent',
                                                min=1,
                                                max=100,
                                                step=10,
                                                # step=None,
                                                # marks={
                                                #     # 1: 'Every Second',
                                                #     # 60: 'Every Minute',
                                                #     # 300: 'Every Five Minutes',
                                                #     # 1800: 'Every half-hour',
                                                #     # 3600: 'Every hour'
                                                #     1: 'Every Second',
                                                #     2: 'Every Minute',
                                                #     3: 'Every Five Minutes',
                                                #     4: 'Every half-hour',
                                                #     5: 'Every hour'

                                                # },
                                                # vertical=True
                                                value=50
                                            ),
                                            html.Br(),
                                            html.H6('Max Points Shown on Figure (1 to 1e6)'),
                                            html.H6('(Recommended not Adjusting)'),
                                            dbc.Input(id="downsampling_limit",type="number",min=1,max=1e6,step=1,value=1e5),

                                        ]

                                    )
                                )
                            ]
                        ),
                        # dbc.Row(
                        #     children=[
                        #         dbc.Card(
                        #             dbc.CardBody(
                        #                 children=[
                                            
                        #                 ]
                        #             )
                        #         )
                        #     ]
                        # ),
                        # dbc.Row(
                        #     children=[
                        #         dbc.Card(
                        #             dbc.CardBody(
                        #                 children=[
                                            
                        #                 ]
                        #             )
                        #         )
                        #     ]
                        # ),

                        # dbc.Row(
                        #     children=[
                        #         dbc.Col(width=2),
                        #         dbc.Col(
                        #             children=[
                                        
                        #             ]
                        #         ),
                        #         dbc.Col(width=2)
                        #     ]
                        # # ),
                        # dbc.Row(
                        #     children=[
                        #         dbc.Col(width=2),
                        #         dbc.Col(
                        #             children=[
                                        
                        #             ]
                        #         ),
                        #         dbc.Col(width=2)
                        #     ]
                        # ),
                        # dbc.Row(
                        #     children=[
                        #         dbc.Col(width=2),
                        #         dbc.Col(
                        #             children=[
                                        
                        #             ]
                        #         ),
                        #         dbc.Col(width=2)
                        #     ]
                        # ),
                        # dbc.Row(
                        #     children=[

                        #     ]
                        # ),



                    ],
                    width=4
                ),
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
                    width=8
                ),
                # dbc.Col(width=4)
            ]
        )
    ],
)





def generate_yaxis_options():
    global DATAFRAME_DICT
    # print(DATAFRAME_DICT.keys())
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
    # elif len(DATAFRAME_DICT.keys())==0 or :
    else:
        yaxis_options=list()

    return yaxis_options



@callback(
    [
        Output(component_id='checklist_dataset', component_property='options'),
        Output(component_id='checklist_parameters', component_property='options'),
        # Output(component_id='store_panda_nonnumeric', component_property='data'),
    ],
    [
        # Input(component_id='store_dataset_keys_and_columns', component_property="data"),
        Input(component_id='url', component_property="pathname")
    ],
    # [
    #     State(component_id="datatable_traces", component_property="data"),
    #     State(component_id="checklist_dataset", component_property="value"),
    #     State(component_id="checklist_parameters", component_property="value"),
    #     # State(component_id='datatable_dataset', component_property='data')
    # ],
    # prevent_initial_call=True,
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








# @callback(
#     [
#         Output(component_id='checklist_dataset', component_property='options'),
#         Output(component_id='checklist_parameters', component_property='options'),
#         # Output(component_id='store_panda_nonnumeric', component_property='data'),
#     ],
#     [
#         Input(component_id='store_dataset_keys_and_columns', component_property="data"),
#         Input(component_id='url', component_property="pathname")
#     ],
#     # [
#     #     State(component_id="datatable_traces", component_property="data"),
#     #     State(component_id="checklist_dataset", component_property="value"),
#     #     State(component_id="checklist_parameters", component_property="value"),
#     #     # State(component_id='datatable_dataset', component_property='data')
#     # ],
#     # prevent_initial_call=True,
# )
# def update_trace_selection_options(
#     store_dataset_keys_and_columns_data,
#     url_pathname
# ):

#     # print(store_dataset_keys_and_columns_data.keys())
#     if len(store_dataset_keys_and_columns_data['dataset_filename'])==0:
#         return [ list(), list()]

#     # print('are we updating the options?')


#     checklist_dataset_options=[]
#     for i in range(len(store_dataset_keys_and_columns_data['dataset_filename'])):
#         checklist_dataset_options.append(
#             {
#                 'label': store_dataset_keys_and_columns_data['dataset_shorthand'][i],
#                 'value': store_dataset_keys_and_columns_data['dataset_filename'][i]
#             }
#         )

#     # print(checklist_dataset_options)
#     # print(store_dataset_keys_and_columns_data['dataset_parameter'])
#     # print('-------------------')

#     return [checklist_dataset_options,store_dataset_keys_and_columns_data['dataset_parameter']]
    


@callback(
    [
        Output(component_id="checklist_dataset", component_property="value"),
        Output(component_id="checklist_parameters", component_property="value"),
        # Output(component_id='store_panda_nonnumeric', component_property='data'),
    ],
    [
        Input(component_id='button_clear_checkboxes', component_property="n_clicks"),
        # Input(component_id='url', component_property="pathname")
    ],
    # [
    # #     State(component_id="datatable_traces", component_property="data"),
    #     State(component_id='checklist_dataset', component_property='options'),
    #     State(component_id='checklist_parameters', component_property='options'),
    # #     # State(component_id='datatable_dataset', component_property='data')
    # ],
    prevent_initial_call=True,
)
def clear_checkboxes(
        button_clear_checkboxes_n_clicks,
        # checklist_dataset_options,
        # checklist_parameters_options,
):
    # print('in the cleaning function')
    return [[],[]]








@callback(
    [
        Output(component_id='datatable_traces', component_property='data'),
        # Output(component_id='store_panda_numeric', component_property='data'),
        # Output(component_id='store_panda_nonnumeric', component_property='data'),
    ],
    [
        Input(component_id="button_add_trace", component_property="n_clicks"),
        Input(component_id="button_clear_traces", component_property="n_clicks")
    ],
    [
        State(component_id="datatable_traces", component_property="data"),
        State(component_id="checklist_dataset", component_property="value"),
        State(component_id="checklist_parameters", component_property="value"),
        # State(component_id='datatable_dataset', component_property='data')
    ],
    prevent_initial_call=True,
)
def add_traces_to_datatable(
    button_add_trace_n_clicks,
    button_clear_traces_n_clicks,
    datatable_traces_data,
    checklist_dataset_value,
    checklist_parameters_value,
):

    # print(checklist_dataset_value)
    # print(checklist_parameters_value)

    # print(ctx.triggered_id)

    if ctx.triggered_id=='button_clear_traces':
        #raise PreventUpdate
        # return {
        #     'dataset_filename':[],
        #     'dataset_shorthand':[],
        #     'dataset_parameter':[]
        # }
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
    # print(output_traces)

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
        # Output(component_id='store_panda_numeric', component_property='data'),
        # Output(component_id='store_panda_nonnumeric', component_property='data'),
    ],
    [
        Input(component_id="button_render_plot", component_property="n_clicks"),
    ],
    [
        State(component_id="datatable_traces", component_property="data"),


        State(component_id="radioitems_timesampling", component_property="value"),
        State(component_id="radioitems_interpolation", component_property="value"),
        State(component_id="radioitems_negatives_to_zero", component_property="value"),
        State(component_id="slider_dot_size", component_property="value"),
        State(component_id="slider_opacity_percent", component_property="value"),
        State(component_id="downsampling_limit", component_property="value"),

        # State(component_id="checklist_dataset", component_property="value"),
        # State(component_id="checklist_parameters", component_property="value"),
        # State(component_id='datatable_dataset', component_property='data')
    ],
    prevent_initial_call=True,
)
def add_traces_to_scatter(
    button_render_plot_n_clicks,
    datatable_traces_data,

    radioitems_timesampling_value,
    radioitems_interpolation_value,
    radioitems_negatives_to_zero_value,
    slider_dot_size_value,
    slider_opacity_percent_value,
    downsampling_limit_value
):
    global DATAFRAME_DICT
    global UNIT_DICT    

    if len(datatable_traces_data)==0:
        raise PreventUpdate

    # concat_list=list()
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

    # print(traces)
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
    downsampling_mask[:downsampling_limit_value]=1
    np.random.shuffle(downsampling_mask)
    downsampling_mask=downsampling_mask.astype(bool)
    traces=traces[downsampling_mask]


    # output_numpy=pd.concat(concat_list,axis='index',ignore_index=True).

    if radioitems_interpolation_value=='no_interpolation':
        temp_figure=px.scatter(
            x=traces[:,0].astype(float),
            y=traces[:,1].astype(float),
            color=traces[:,2],
            opacity=0.01*slider_opacity_percent_value
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

    temp_figure.update_traces(marker=dict(size=slider_dot_size_value))
    # temp_figure=px.scatter(
    #         x=outputted_xy[:,0][downsampling_mask],
    #         y=outputted_xy[:,1][downsampling_mask],
    #         color=string_name_array[downsampling_mask],
    #         opacity=0.01*opacity_percent_value
    #     )

    temp_figure.update_layout(
        font=dict(
            size=14
        )
    )


    return [temp_figure]
                                                    






