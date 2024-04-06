import numpy as np
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

df = pd.read_csv('../flights_sample_3m.csv',
                 usecols=['ORIGIN_CITY',
                          'DEST_CITY',
                          'ARR_DELAY',
                          'FL_DATE',
                          'AIR_TIME'])
all_origin = df['ORIGIN_CITY'].unique()
all_dest = df['DEST_CITY'].unique()

# Layout


# Global widgets

global_widgets = [
    html.H1('FlightFinder'),
    html.P('Which airline has the smallest delays for your route?'),
    html.Br(),
    html.Label('Years'),
    dcc.RangeSlider(
        id='year_range',
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
        id='origin_dropdown',
        options=all_origin,
        value='Vancouver',
        multi=False,
        placeholder='Select a city...'
    ),
    html.Br(),
    html.Label('Destination'),
    dcc.Dropdown(
        id='dest_dropdown',
        options=all_dest,
        value='Montreal',
        multi=False,
        placeholder='Select a city...'
    )
]

# Cards

# card_flights_on_time = dbc.Card(
#     [
#         dbc.CardBody(
#             [
#                 html.H4('Flights on Time'),
#                 html.H2('99.9%'),
#             ]
#         )
#     ]
# )

card_flights_on_time = dbc.Card(id='flights_on_time')

# card_average_flight_time = dbc.Card(
#     [
#         dbc.CardBody(
#             [
#                 html.H4('Average Flight Time'),
#                 html.H2('3h 45m'),
#             ]
#         )
#     ]
# )
card_average_flight_time = dbc.Card(id='avg_flight_time')

# card_average_delay = dbc.Card(
#     [
#         dbc.CardBody(
#             [
#                 html.H4('Average Delay'),
#                 html.H2('15m'),
#             ]
#         )
#     ]
# )
card_average_delay = dbc.Card(id='avg_delay')

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
def __pct_on_time_calc(delay_times: np.ndarray) -> float:

    # consider delay less than this number to be on time
    tol = 5
    if delay_times.size > 0:
        return (delay_times <= tol).sum() / delay_times.size * 100
    return 0.0


def __avg_flight_time(flight_times: np.ndarray) -> float:
    if flight_times.size > 0:
        m = flight_times.mean()
        if isinstance(m, float):
            return m
    return 0.0


@callback(
    Output('flights_on_time', 'children'),
    Output('avg_flight_time', 'children'),
    Output('avg_delay', 'children'),
    Input('origin_dropdown', 'value'),
    Input('dest_dropdown', 'value'),
    Input('year_range', 'value')
)
def cb(origin_dropdown, dest_dropdown, year_range):

    # temporarily disable multi dest
    if isinstance(dest_dropdown, list):
        dest_dropdown = dest_dropdown[0]
    print(dest_dropdown)
    msk = ((df['ORIGIN_CITY'] == origin_dropdown)
           & (df['DEST_CITY'] == dest_dropdown)
           & (pd.DatetimeIndex(df['FL_DATE'].to_numpy()).year >= year_range[0])
           & (pd.DatetimeIndex(df['FL_DATE'].to_numpy()).year <= year_range[1]))
    print(origin_dropdown)
    print(dest_dropdown)
    print(msk.sum())

    _df = df.loc[msk, :]

    # flights on time
    pct_flights_on_time = __pct_on_time_calc(_df.loc[:, 'ARR_DELAY'].to_numpy())
    pct_flights_on_time = [dbc.CardHeader('Flights on Time'),
                           dbc.CardBody(f'{pct_flights_on_time}%')]

    # avg flight time
    _avg_flight_time = _df[:, 'AIR_TIME'].mean() # numerical value in minutes
    # card to return
    avg_flight_time = [dbc.CardHeader('Flights on Time'),
                       dbc.CardBody(f'{_avg_flight_time}')] # card to return

    return pct_flights_on_time, avg_flight_time


# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)

#%%
