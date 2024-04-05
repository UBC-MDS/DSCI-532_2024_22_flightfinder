from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout


# Global widgets

global_widgets = [
    html.H1('FlightFinder'),
    html.P('Which airline has the smallest delays for your route?'),
    html.Br(),
    html.Label('Years'),
    dcc.RangeSlider(
        min=2019,
        max=2023,
        value=[1, 12],  # A list since it's a range slideer
        step=1,  # The step between values
        marks={i: str(i) for i in range(2019, 2024)},  # The marks on the slider
        tooltip={'always_visible': True, 'placement': 'bottom'}  # Show the current values
    ),
    html.Br(),
    html.Label('Origin'),
    dcc.Dropdown(
        options=['New York City', 'Montreal', 'San Francisco', 'Vancouver'],
        value='Vancouver',
        multi=False,
        placeholder='Select a city...'
    ),
    html.Br(),
    html.Label('Destination'),
    dcc.Dropdown(
        options=['New York City', 'Montreal', 'San Francisco', 'Vancouver'],
        value='Montreal',
        multi=True,
        placeholder='Select a city...'
    )
]

# Cards

card_flights_on_time = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4('Flights on Time'),
                html.H2('99.9%'),
            ]
        )
    ]
)

card_average_flight_time = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4('Average Flight Time'),
                html.H2('3h 45m'),
            ]
        )
    ]
)

card_average_delay = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4('Average Delay'),
                html.H2('15m'),
            ]
        )
    ]
)


cards = dbc.Row([
    dbc.Col(card_flights_on_time, md=4),
    dbc.Col(card_average_flight_time, md=4),
    dbc.Col(card_average_delay, md=4)
])

mock_data = {
    'x': [1, 2, 3, 4, 5],
    'y': [10, 20, 30, 40, 50]
}

graph_avg_delay_by_carrier = html.Div([ 
    html.P('Average delay by carrier'),
])

graph_number_unique_flights = html.Div([
    html.P('Number of unique flights')
])

graph_map = html.Div([
    html.P('Map')
])

graph_count_by_delay = html.Div([
    html.P('Count by delay')
])





app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(global_widgets, md=4, style={'marginTop': 20}),
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
                    dbc.Row([graph_number_unique_flights], style={'flex': '1', "padding": "10px"}),
                    dbc.Row([graph_count_by_delay], style={'flex': '1', "padding": "10px"})
                ], md=6, style={"display": "flex", "flexDirection": "column", "gap": "10px"})
            ], style={'display': 'flex', 'flexDirection': 'row', 'flex': '1'})
        ], md=8, style={'display': 'flex', 'flexDirection': 'column', 'height': '100vh'})
    ])
], fluid=True)


# Server side callbacks/reactivity
# ...

# Run the app/dashboard
if __name__ == '__main__':
    app.run()