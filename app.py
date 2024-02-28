import dash
from dash import html, dcc,callback
import dash_bootstrap_components as dbc


local_stylesheet = {
    "href": "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap",
    "rel": "stylesheet"
}

#intentionally using a global


app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, local_stylesheet ])

#custom ordering of navbar
my_page_link_list=[
    # dbc.NavLink('Home', href='/content/a537f01f-de6f-4093-b216-89fef5cfba1b',style = {'color': 'white','font-weight':'bold'},className='navlink-parker'),
    # dbc.NavLink('Dataset Manager', href='/content/a537f01f-de6f-4093-b216-89fef5cfba1b/dataset-manager',style = {'color': 'white','font-weight':'bold'},className='navlink-parker'),
    # dbc.NavLink('Dataset Manager Biochem.', href='/content/a537f01f-de6f-4093-b216-89fef5cfba1b/dataset-manager-biochemistry',style = {'color': 'white','font-weight':'bold'},className='navlink-parker'),
    # dbc.NavLink('Unit Manager', href='/content/a537f01f-de6f-4093-b216-89fef5cfba1b/unit-manager',style = {'color': 'white','font-weight':'bold'},className='navlink-parker'),
    # dbc.NavLink('Unit Manager Biochem.', href='/content/a537f01f-de6f-4093-b216-89fef5cfba1b/unit-manager-biochemistry',style = {'color': 'white','font-weight':'bold'},className='navlink-parker'),
    # dbc.NavLink('Plotter', href='/content/a537f01f-de6f-4093-b216-89fef5cfba1b/plotter',style = {'color': 'white','font-weight':'bold'},className='navlink-parker'),
    dbc.NavLink('Home', href='/',style = {'color': 'white','font-weight':'bold'},className='navlink-parker'),
    dbc.NavLink('Dataset Manager', href='/dataset-manager',style = {'color': 'white','font-weight':'bold'},className='navlink-parker'),
    dbc.NavLink('Dataset Manager Biochem.', href='/dataset-manager-biochemistry',style = {'color': 'white','font-weight':'bold'},className='navlink-parker'),
    dbc.NavLink('Unit Manager', href='/unit-manager',style = {'color': 'white','font-weight':'bold'},className='navlink-parker'),
    dbc.NavLink('Unit Manager Biochem.', href='/unit-manager-biochemistry',style = {'color': 'white','font-weight':'bold'},className='navlink-parker'),
    dbc.NavLink('Plotter', href='/plotter',style = {'color': 'white','font-weight':'bold'},className='navlink-parker'),
]

app.layout = html.Div(
    [
        dcc.Store(id='store_dataset_keys_and_columns',data={'dataset_filename':[],'dataset_shorthand':[],'dataset_parameter':[]}),
        dcc.Location('url'),
        dbc.NavbarSimple(
            children=[]+my_page_link_list,
            brand='Perfusion Dashboard',
            color='#1A3E68',
            brand_style = {'color': '#FFCD00'},
        ),
        dash.page_container
    ]
)


if __name__ == "__main__":
    #app.run(debug=False, host='0.0.0.0')
    app.run(debug=True, host='0.0.0.0', port=8050)