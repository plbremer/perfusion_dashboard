import dash
from dash import dcc, html, dash_table, callback, ctx
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
import io
import pandas as pd

from config import DATAFRAME_DICT

dash.register_page(__name__, path='/dataset-manager')



def create_shorthand_string(temp_string):
    shorthand_list=temp_string.split(' ')[0:2]
    return ' '.join(shorthand_list)


def check_file(filename):
    if '.csv' not in filename:
        return ['Did you mean to upload a .csv?']
    else:
        return True

def panda_from_csv(content_string):
    
    content_type, content_string = content_string.split(',')
    decoded=base64.b64decode(content_string)
    temp_dataframe=pd.read_csv(
        io.BytesIO(decoded)
    )
    return temp_dataframe


layout = html.Div(
    children=[
        html.Br(),
        html.Br(),
        dcc.Store(id='dummy_store'),
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
                dbc.Col(width=1),
                dbc.Col(
                    children=[
                        dbc.Spinner(
                            dash_table.DataTable(
                                id='datatable_dataset',
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
                                        'id':'dataset_row_count',
                                        'name':'Number of Rows'
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
                                style_cell_conditional=[
                                    {'if': {'column_id': 'dataset_filename'},
                                    'width': '60%'},
                                    {'if': {'column_id': 'dataset_shorthand'},
                                    'width': '20%'},
                                    {'if': {'column_id': 'dataset_row_count'},
                                    'width': '20%'},
                                ],
                                row_deletable=True
                            )
                        )
                    ],
                    width=10
                ),
                dbc.Col(width=1)
            ]
        )


    ],
)




# dcc.Store(id='dummy_store')
@callback(
    [
        Output(component_id='dummy_store', component_property='data'),
        # Output(component_id='store_panda_numeric', component_property='data'),
        # Output(component_id='store_panda_nonnumeric', component_property='data'),
    ],
    [
        
        # Input(component_id="upload_dataset", component_property="contents"),
        Input(component_id="datatable_dataset", component_property="data_previous"),
        
    ],
    [
        State(component_id='dummy_store', component_property='data'),
        Input(component_id='datatable_dataset', component_property='data'),
        # State(component_id='datatable_dataset', component_property='data')
    ],
    # prevent_initial_call=True,
)
def remove_dataset(
    # upload_dataset_contents,
    datatable_dataset_data_previous,
    dummy_store_data,
    datatable_dataset_data
    # upload_dataset_filename,
    # datatable_dataset_data
    
):
    '''
    dummy store is a way to remove datasets from the global based on updates to 
    datatable data

    check if addition or removal with lenght previous and legnth store
    '''
    global DATAFRAME_DICT

    # print('we are here')
    # print(len(datatable_dataset_data_previous))
    # print(len(datatable_dataset_data))
    # print('----')

    # print(DATAFRAME_DICT)

    if datatable_dataset_data_previous is None:
        raise PreventUpdate
    if len(datatable_dataset_data_previous) < len(datatable_dataset_data):
        raise PreventUpdate
    # elif len(datatable_dataset_data)==0:
    #     # global DATAFRAME_DICT
    #     DATAFRAME_DICT=dict()

    
    
    elif len(datatable_dataset_data_previous) > len(datatable_dataset_data):
        # print('previous is greater than current')
        # print(len(datatable_dataset_data))
        if len(datatable_dataset_data)==0:
            # print('in innermost')
            # print(DATAFRAME_DICT.keys()[0])
            # print(DATAFRAME_DICT)
            # del DATAFRAME_DICT[DATAFRAME_DICT.keys()[0]]
            DATAFRAME_DICT=dict()
        elif len(datatable_dataset_data)>0:

            current_datasets=set(
                [temp_dict['dataset_filename'] for temp_dict in datatable_dataset_data]
            )
            # print(current_datasets)
            # global DATAFRAME_DICT

            dict_keys_to_remove=list()
            for temp_key in DATAFRAME_DICT.keys():
                if temp_key not in current_datasets:
                    dict_keys_to_remove.append(temp_key)
                    
            for temp_key in dict_keys_to_remove:
                del DATAFRAME_DICT[temp_key]

    return [dummy_store_data]




@callback(
    [
        Output(component_id='datatable_dataset', component_property='data'),
        # Output(component_id='store_panda_numeric', component_property='data'),
        # Output(component_id='store_panda_nonnumeric', component_property='data'),
    ],
    [
        Input(component_id="upload_dataset", component_property="contents"),
        # Input(component_id="datatable_dataset", component_property="previous"),
        # Input(component_id='datatable_dataset', component_property='data'),
    ],
    [
        State(component_id="upload_dataset", component_property="filename"),
        # State(component_id='datatable_dataset', component_property='data')
    ],
    # prevent_initial_call=True,
)
def add_dataset(
    upload_dataset_contents,
    # datatable_dataset_data_previous
    # datatable_dataset_data,
    upload_dataset_filename,
    # datatable_dataset_data
):
    '''
    add the dataset to the global variable
    get the dataset description from the global variable
    send the data to the datatable


    comparing the length of previous to the current data length informs us about 
    if this was called because of an add
    '''

    # if upload_dataset_contents==None:
    #     raise PreventUpdate
    
    # passes_checks=check_file(upload_dataset_filename.lower())
    # if passes_checks!=True:
    #     return [html.H6(passes_checks[0])]
    global DATAFRAME_DICT
    
    
    if upload_dataset_contents!=None:
        uploaded_panda=panda_from_csv(upload_dataset_contents)
        DATAFRAME_DICT[upload_dataset_filename]=uploaded_panda.copy()

    

    


    row_count_list=list()
    shorthand_list=list()
    filename_list=list()

    if len(DATAFRAME_DICT.keys())>=1:
        for temp_key in DATAFRAME_DICT.keys():
            filename_list.append(temp_key)

            shorthand_list.append(
                create_shorthand_string(temp_key)
            )
            row_count_list.append(
                len(DATAFRAME_DICT[temp_key].index)
            )

        output_list=[
            {
                'dataset_filename':filename_list[i],
                'dataset_shorthand':shorthand_list[i],
                'dataset_row_count':row_count_list[i]
            } for i in range(len(row_count_list))
        ]
    elif len(DATAFRAME_DICT.keys())==0:
        output_list=[]

    return [output_list]






# @callback(
#     [
#         Output(component_id='datatable_dataset', component_property='data'),
#         # Output(component_id='store_panda_numeric', component_property='data'),
#         # Output(component_id='store_panda_nonnumeric', component_property='data'),
#     ],
#     [
#         Input(component_id="upload_dataset", component_property="contents"),
#     ],
#     [
#         State(component_id="upload_dataset", component_property="filename"),
#         State(component_id='datatable_dataset', component_property='data')
#     ],
#     # prevent_initial_call=True,
# )
# def remove_dataset(
#     upload_dataset_contents,
#     upload_dataset_filename,
#     datatable_dataset_data
# ):
#     '''
#     add the dataset to the global variable
#     get the dataset description from the global variable
#     send the data to the datatable
#     '''

#     # if upload_dataset_contents==None:
#     #     raise PreventUpdate
    
#     # passes_checks=check_file(upload_dataset_filename.lower())
#     # if passes_checks!=True:
#     #     return [html.H6(passes_checks[0])]
#     global DATAFRAME_DICT
    
    
#     if upload_dataset_contents!=None:
#         uploaded_panda=panda_from_csv(upload_dataset_contents)
#         DATAFRAME_DICT[upload_dataset_filename]=uploaded_panda.copy()

#     row_count_list=list()
#     shorthand_list=list()
#     filename_list=list()

#     if len(DATAFRAME_DICT.keys())>=1:
#         for temp_key in DATAFRAME_DICT.keys():
#             filename_list.append(temp_key)

#             shorthand_list.append(
#                 create_shorthand_string(temp_key)
#             )
#             row_count_list.append(
#                 len(DATAFRAME_DICT[temp_key].index)
#             )

#         output_list=[
#             {
#                 'dataset_filename':filename_list[i],
#                 'dataset_shorthand':shorthand_list[i],
#                 'dataset_row_count':row_count_list[i]
#             } for i in range(len(row_count_list))
#         ]
#     elif len(DATAFRAME_DICT.keys())==0:
#         output_list=[]

#     return [output_list]