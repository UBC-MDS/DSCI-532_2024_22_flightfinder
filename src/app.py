from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from src.data import all_origin, all_dest
import src.callbacks


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

import base64

# Encode the image for inline display
encoded_image = base64.b64encode(open("img/airplane.png", "rb").read()).decode('ascii')


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
        value=[2020, 2023],  # A list since it's a range slider
        step=1,  # The step between values
        marks={i: {'label': str(i), 'style': {'color': 'white'}} for i in range(2020, 2024)},
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
    html.Br(),
    dbc.Button("Submit", id='submit_button', n_clicks=0, color="secondary"),
    html.Br(),
     html.Div(
             html.Img(src='data:image/png;base64,{}'.format(encoded_image), style={'width': "65%", "opacity": 0.2}),
             style={'width': "100%", "display": "flex", "justifyContent": "center", "paddingTop": "20px"}
     ),
    html.Div(id='app-info', children=[
        html.P("This Dash app was developed by Team 22 of the MDS program to provide insights into delay times of flights"),
        html.P("Credits: Rory White, Allan Lee, Vincent Zhang and Lily Tao"),
        html.P("Data: US Department of Transportation, Patrick Zelazko"),
        html.P(["Check out the source code on ", html.A("GitHub", href="https://github.com/UBC-MDS/DSCI-532_2024_22_flightfinder", target="_blank", style={'color': 'white'})]),
        html.P("Last updated: April 13, 2024")
    ], style={
        'position': 'absolute',
        'bottom': '0',
        'maxWidth': '29%',
        'textAlign': 'left',
        'fontSize': '12px', # Match the sidebar background color
        # 'borderTop': '1px solid #e8e8e8'  # Optional border for a visual separation
    })


]

# Cards


card_flights_on_time = dbc.Card(id='flights_on_time')
card_average_flight_time = dbc.Card(id='avg_flight_time')
card_average_delay = dbc.Card(id='avg_delay')

cards = dcc.Loading(
        id="spinner",
        children=[dbc.Row([
    dbc.Col(card_flights_on_time, md=4),
    dbc.Col(card_average_flight_time, md=4),
    dbc.Col(card_average_delay, md=4)
])],
        type="cube",
        fullscreen=True,
        color="white",
        style={"paddingTop": "50px", "backgroundColor": "rgb(25, 135, 140)"}
),


graph_avg_delay_by_carrier = html.Div([
    html.H6('Average delay by carrier'),
    dvc.Vega(id='bar', spec={}, style={'width': '100%', 'height': '70%'}, opt={'actions': False},)
])
# graph_avg_delay_by_carrier = dvc.Vega(id='bar', spec={})

graph_number_unique_flights = html.Div([
    html.H6('Number of unique flights'), 
    dvc.Vega(id='stacked_plot', spec={}, style={'width': '100%', 'height': '70%'}, opt={'actions': False},)
])
# graph_number_unique_flights = dvc.Vega(id='stacked_plot', spec={})

graph_map = html.Div([
    dvc.Vega(id='map_plot', spec={}, style={'width': '100%', 'height': '90%'}, opt={'actions': False},)
])

graph_count_by_delay = html.Div([
    html.H6('Probability of Flight Delays'),
    dvc.Vega(id='hist', spec={}, style={'width': '100%', 'height': '70%'}, opt={'actions': False},)
])


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(global_widgets, md=4, style={'padding': 40, 'color': 'white', 'backgroundColor': 'rgb(25, 135, 140)', 'boxShadow': "rgba(0, 0, 0, 0.24) 0px 3px 8px" }),
        dbc.Col([
            dbc.Row([
                dbc.Col(cards, md=12, style={'marginTop': 20, "paddingBottom": "20px"})
            ], style={'minHeight': "20vh"}),
            dbc.Row([
                dbc.Col([
                    dbc.Row([graph_map], style={'flex': '1', "paddingBottom": "10px"}),
                    dbc.Row([graph_avg_delay_by_carrier], style={'flex': '1', "padding": "10px"}),
                ], md=6, style={"display": "flex", "flexDirection": "column", "gap": "10px"}),
                dbc.Col([
                    dbc.Row([graph_count_by_delay], style={'flex': '1', "padding": "10px"}),
                    dbc.Row([graph_number_unique_flights],style={'flex': '1', "padding": "10px"}),
                ], md=6, style={"display": "flex", "flexDirection": "column", "gap": "10px"})
            ], style={'display': 'flex', 'flexDirection': 'row', 'flex': '1'})
        ], md=8, style={'display': 'flex', 'flexDirection': 'column', 'height': '100vh', "paddingLeft": "40px", "paddingRight": "40px"})
    ])
], fluid=True)


  
# Run the app/dashboard
if __name__ == '__main__':
    app.run_server(debug=False)
