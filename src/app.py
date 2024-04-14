from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from src.data import all_origin, all_dest
import src.callbacks


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


# Global widgets

global_widgets = [
    html.H1('FlightFinder'),
    html.H5('Which airline has the smallest delays for your route?'),
    html.Br(),
    html.Label('Years'),
    dcc.RangeSlider(
        id='year_range',
        min=2020,
        max=2023,
        value=[2020, 2023],  # A list since it's a range slideer
        step=1,  # The step between values
        marks={i: str(i) for i in range(2020, 2024)},  # The marks on the slider
        tooltip={'always_visible': True, 'placement': 'bottom'}  # Show the current values
    ),
    html.Br(),
    html.Label('Origin'),
    dcc.Dropdown(
        id='origin_dropdown',
        options=all_origin,
        value='Seattle, WA',
        multi=False,
        style={'color': "black"}
       
    ),
    html.Br(),
    html.Label('Destination'),
    dcc.Dropdown(
        id='dest_dropdown',
        options=all_dest,
        value='Los Angeles, CA',
        multi=False,
        style={'color': "black"}
    ),
    # html.Div(style={'flexGrow': '1'}),  # Spacer Div
    html.Div(id='app-info', children=[
        html.P("This Dash app was developed by Team 22 to provide insights into delay times of flights."),
        html.P(["Check out the source code on ", html.A("GitHub", href="https://github.com/UBC-MDS/DSCI-532_2024_22_flightfinder", target="_blank")]),
        html.P("Last updated: April 13, 2024")
    ], style={
        'position': 'fixed',
        'bottom': '0',
        'width': 'inherit',
        'textAlign': 'left',
        'padding': '20px',
        'fontSize': '12px', # Match the sidebar background color
        # 'borderTop': '1px solid #e8e8e8'  # Optional border for a visual separation
    })


]

# Cards

card_flights_on_time = dbc.Card(id='flights_on_time')
card_average_flight_time = dbc.Card(id='avg_flight_time')
card_average_delay = dbc.Card(id='avg_delay')

cards = dbc.Row([
    dbc.Col(card_flights_on_time, md=4),
    dbc.Col(card_average_flight_time, md=4),
    dbc.Col(card_average_delay, md=4)
])


graph_avg_delay_by_carrier = html.Div([
    html.H6('Average delay by carrier'),
    dvc.Vega(id='bar', spec={}, style={'width': '100%', 'height': '70%'})
])
# graph_avg_delay_by_carrier = dvc.Vega(id='bar', spec={})

graph_number_unique_flights = html.Div([
    html.H6('Number of unique flights'), 
    dvc.Vega(id='stacked_plot', spec={}, style={'width': '100%', 'height': '70%'})
])
# graph_number_unique_flights = dvc.Vega(id='stacked_plot', spec={})

graph_map = html.Div([
    html.H6('Map'),
    dvc.Vega(id='map_plot', spec={}, style={'width': '100%', 'height': '70%'})
])

graph_count_by_delay = html.Div([
    html.H6('Probability of Flight Delays'),
    dvc.Vega(id='hist', spec={}, style={'width': '100%', 'height': '70%'})
])


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(global_widgets, md=4, style={'padding': 40, 'color': 'white', 'backgroundColor': 'rgb(25, 135, 140)', 'boxShadow': "rgba(0, 0, 0, 0.24) 0px 3px 8px" }),
        dbc.Col([
            dbc.Row([
                dbc.Col(cards, md=12, style={'marginTop': 20})
            ], style={'minHeight': "20vh"}),
            dbc.Row([
                dbc.Col([
                    dbc.Row([graph_avg_delay_by_carrier], style={'flex': '1', "padding": "10px"}),
                    dbc.Row([graph_map], style={'flex': '1', "padding": "10px"})
                ], md=6, style={"display": "flex", "flexDirection": "column", "gap": "10px"}),
                dbc.Col([
                    dbc.Row([graph_number_unique_flights],style={'flex': '1', "padding": "10px"}),
                    dbc.Row([graph_count_by_delay], style={'flex': '1', "padding": "10px"})
                ], md=6, style={"display": "flex", "flexDirection": "column", "gap": "10px"})
            ], style={'display': 'flex', 'flexDirection': 'row', 'flex': '1'})
        ], md=8, style={'display': 'flex', 'flexDirection': 'column', 'height': '100vh', "paddingLeft": "40px"})
    ])
], fluid=True)


  
# Run the app/dashboard
if __name__ == '__main__':
    app.run_server(debug=False)
