import dash
from dash import dcc, html, dash_table, callback, ctx
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
import io
import pandas as pd
import openpyxl

from config import DATAFRAME_DICT_BIOCHEMISTRY

dash.register_page(__name__, path='/dataset-manager-biochemistry')

def create_shorthand_string_biochemistry(temp_string):
    '''
    '''
    return temp_string.split(': ')[1]
    # return temp_string


def check_file(filename):
    if '.xlsx' not in filename:
        return ['Did you mean to upload a .xlsx?']
    else:
        return True

def get_sheet_names(bytes_object):
    try:
        workbook = openpyxl.load_workbook(bytes_object)
        sheet_names = workbook.sheetnames
        return sheet_names
    except Exception as e:
        print(f"Error: {e}")
        return None

def coerce_one_sheet(bytes_object,temp_sheet):
    temp_df=pd.read_excel(
        io=bytes_object,
        sheet_name=temp_sheet,
        header=None
    )
    temp_df=temp_df.dropna(how='all')
    temp_df=temp_df.T
    temp_df.columns=temp_df.iloc[0]
    temp_df=temp_df.drop([0,1],axis='index')
    temp_df['Time from perfusion onset (h)']=temp_df['Time from perfusion onset (h)'].astype(float).round(decimals=2)
    temp_df=temp_df.drop(['Date','Hour'],axis='columns')
    pattern = r'(\d+\.\d+|\d+)'
    for temp_df_col in temp_df.columns:
        temp_df[temp_df_col]=temp_df[temp_df_col].astype(str).str.extract(pattern, expand=False)
    temp_df=temp_df.reset_index(drop=True)
    # print(temp_df)
    # print(temp_df['pH',:])
    temp_df['pH']=temp_df['pH'].where(
        cond=(temp_df['pH'].astype(float)<20),
        other=(temp_df['pH'].astype(float)/1000).astype(str)
    )
    temp_df['pH, bile']=temp_df['pH, bile'].where(
        cond=(temp_df['pH, bile'].astype(float)<20),
        other=(temp_df['pH, bile'].astype(float)/1000).astype(str)
    )
    return temp_df


def pandas_from_xlsx(content_string):
    content_type, content_string = content_string.split(',')
    decoded=base64.b64decode(content_string)
    bytes_object=io.BytesIO(decoded)
    sheet_names=get_sheet_names(bytes_object)
    sheet_dict=dict()
    for temp_sheet in sheet_names:
        if 'liver' not in temp_sheet.lower():
            continue
        else:
            sheet_dict['sheet: '+temp_sheet]=coerce_one_sheet(bytes_object,temp_sheet)
    return sheet_dict

    # temp_dataframe=pd.read_csv(
        
    # )

layout = html.Div(
    children=[
        html.Br(),
        html.Br(),
        dcc.Store(id='dummy_store_biochemistry'),
        dbc.Row(
            children=[
                dbc.Col(width=4),
                dbc.Col(
                    children=[
                        dcc.Upload(
                            id='upload_dataset_biochemistry',
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
                dbc.Col(width=3),
                dbc.Col(
                    children=[
                        dbc.Spinner(
                            dash_table.DataTable(
                                id='datatable_dataset_biochemistry',
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
                                        'id':'dataset_timepoint_count',
                                        'name':'Number of Timepoints'
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
                                    'width': '40%'},
                                    {'if': {'column_id': 'dataset_shorthand'},
                                    'width': '20%'},
                                    {'if': {'column_id': 'dataset_row_count'},
                                    'width': '40%'},
                                ],
                                row_deletable=True
                            )
                        )
                    ],
                    width=6
                ),
                dbc.Col(width=3)
            ]
        )
    ],
)


@callback(
    [
        Output(component_id='dummy_store_biochemistry', component_property='data'),
        # Output(component_id='store_panda_numeric', component_property='data'),
        # Output(component_id='store_panda_nonnumeric', component_property='data'),
    ],
    [
        # Input(component_id="upload_dataset", component_property="contents"),
        Input(component_id="datatable_dataset_biochemistry", component_property="data_previous"),
    ],
    [
        State(component_id='dummy_store_biochemistry', component_property='data'),
        State(component_id='datatable_dataset_biochemistry', component_property='data'),
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
    global DATAFRAME_DICT_BIOCHEMISTRY

    if datatable_dataset_data_previous is None:
        raise PreventUpdate
    if len(datatable_dataset_data_previous) < len(datatable_dataset_data):
        raise PreventUpdate
    
    elif len(datatable_dataset_data_previous) > len(datatable_dataset_data):
        # print('previous is greater than current')
        # print(len(datatable_dataset_data))
        if len(datatable_dataset_data)==0:
            # print('in innermost')
            # print(DATAFRAME_DICT.keys()[0])
            # print(DATAFRAME_DICT)
            # del DATAFRAME_DICT[DATAFRAME_DICT.keys()[0]]
            DATAFRAME_DICT_BIOCHEMISTRY=dict()
        elif len(datatable_dataset_data)>0:

            current_datasets=set(
                [temp_dict['dataset_filename'] for temp_dict in datatable_dataset_data]
            )
            # print(current_datasets)
            # global DATAFRAME_DICT

            dict_keys_to_remove=list()
            for temp_key in DATAFRAME_DICT_BIOCHEMISTRY.keys():
                if temp_key not in current_datasets:
                    dict_keys_to_remove.append(temp_key)
                    
            for temp_key in dict_keys_to_remove:
                del DATAFRAME_DICT_BIOCHEMISTRY[temp_key]

    return [dummy_store_data]




@callback(
    [
        Output(component_id='datatable_dataset_biochemistry', component_property='data'),
        # Output(component_id='store_panda_numeric', component_property='data'),
        # Output(component_id='store_panda_nonnumeric', component_property='data'),
    ],
    [
        Input(component_id="upload_dataset_biochemistry", component_property="contents"),
        # Input(component_id="datatable_dataset", component_property="previous"),
        # Input(component_id='datatable_dataset', component_property='data'),
    ],
    [
        State(component_id="upload_dataset_biochemistry", component_property="filename"),
        # State(component_id='datatable_dataset', component_property='data')
    ],
    # prevent_initial_call=True,
)
def add_datasets(
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

    the behavior of this uploader is different compared to the behavior of previous uploader
    in the previous uploader, one csv corresponded to one "sample". in this version, one .xlsx
    defines the entire set of samples. 
    '''

    # if upload_dataset_contents==None:
    #     raise PreventUpdate
    
    # passes_checks=check_file(upload_dataset_filename.lower())
    # if passes_checks!=True:
    #     return [html.H6(passes_checks[0])]
    global DATAFRAME_DICT_BIOCHEMISTRY
    
    
    if upload_dataset_contents!=None:
        uploaded_pandas=pandas_from_xlsx(upload_dataset_contents)
        # uploaded_panda=panda_from_csv(upload_dataset_contents)
        for dataset in uploaded_pandas.keys():

            DATAFRAME_DICT_BIOCHEMISTRY[dataset]=uploaded_pandas[dataset]

    

    


    timepoint_count_list=list()
    shorthand_list=list()
    filename_list=list()

    if len(DATAFRAME_DICT_BIOCHEMISTRY.keys())>=1:
        for temp_key in DATAFRAME_DICT_BIOCHEMISTRY.keys():
            filename_list.append(temp_key)

            shorthand_list.append(
                create_shorthand_string_biochemistry(temp_key)
            )
            timepoint_count_list.append(
                len(DATAFRAME_DICT_BIOCHEMISTRY[temp_key].index)
            )

        output_list=[
            {
                'dataset_filename':filename_list[i],
                'dataset_shorthand':shorthand_list[i],
                'dataset_timepoint_count':timepoint_count_list[i]
            } for i in range(len(timepoint_count_list))
        ]
    elif len(DATAFRAME_DICT_BIOCHEMISTRY.keys())==0:
        output_list=[]

    return [output_list]




