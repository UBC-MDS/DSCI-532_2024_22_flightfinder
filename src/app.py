import numpy as np
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
from typing import Tuple
import altair as alt

from vega_datasets import data
alt.data_transformers.enable('vegafusion')
cities = pd.read_csv('data/raw/updated_usa_airports.csv')
cities_lat_long = cities.set_index('city')[['latitude', 'longitude']].apply(tuple, axis=1).to_dict()


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

df = pd.read_csv('data/processed/data.gzip', compression='gzip',
                 usecols=['ORIGIN_CITY',
                          'DEST_CITY',
                          'ARR_DELAY',
                          'FL_DATE',
                          'AIR_TIME',
                          'AIRLINE',
                          'AIRLINE_CODE',
                          'AIRLINE'])

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
        value=[2019, 2023],  # A list since it's a range slideer
        step=1,  # The step between values
        marks={i: str(i) for i in range(2019, 2024)},  # The marks on the slider
        tooltip={'always_visible': True, 'placement': 'bottom'}  # Show the current values
    ),
    html.Br(),
    html.Label('Origin'),
    dcc.Dropdown(
        id='origin_dropdown',
        options=all_origin,
        value='Atlanta, GA',
        multi=False,
        # placeholder='Select a city...'
    ),
    html.Br(),
    html.Label('Destination'),
    dcc.Dropdown(
        id='dest_dropdown',
        options=all_dest,
        value='Denver, CO',
        multi=False,
        # placeholder='Select a city...'
    )
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

mock_data = {
    'x': [1, 2, 3, 4, 5],
    'y': [10, 20, 30, 40, 50]
}


graph_avg_delay_by_carrier = html.Div([
    html.P('Average delay by carrier'),
    dvc.Vega(id='bar', spec={}, style={'width': '100%', 'height': '70%'})
])
# graph_avg_delay_by_carrier = dvc.Vega(id='bar', spec={})

graph_number_unique_flights = html.Div([
    html.P('Number of unique flights'), 
    dvc.Vega(id='stacked_plot', spec={}, style={'width': '100%', 'height': '70%'})
])
# graph_number_unique_flights = dvc.Vega(id='stacked_plot', spec={})

graph_map = html.Div([
    html.P('Map'),
    dvc.Vega(id='map_plot', spec={}, style={'width': '100%', 'height': '70%'})
])

graph_count_by_delay = html.Div([
    html.P('Probability of Flight Delays'),
    dvc.Vega(id='hist', spec={}, style={'width': '100%', 'height': '70%'})
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
def __pct_on_time_calc(delay_times: np.ndarray) -> Tuple[int, float]:

    # consider delay less than this number to be on time
    tol = 5
    if delay_times.size > 0:
        return (delay_times <= tol).sum() / delay_times.size * 100
    return 0.0


def __avg_flight_time(flight_times: np.ndarray) -> Tuple[int, int]:
    if flight_times.size > 0:
        m = np.nanmean(flight_times)
        if isinstance(m, float):
            hrs = int(m // 60)
            mins = int(m % 60)
            return hrs, mins
    return 0, 0


def __avg_delay(delay_times: np.ndarray) -> float:
    if delay_times.size > 0:
        m = np.nanmean(delay_times)
        return m
    return 0

  
def plot_stacked(df):
    _filtered_df = df.copy()
    _filtered_df['DAY_OF_WEEK'] = pd.to_datetime(_filtered_df['FL_DATE']).dt.day_name().apply(lambda x: x[:3])
    plot_data = (_filtered_df.groupby(['DAY_OF_WEEK', 'AIRLINE_CODE'])
                               .size()
                               .reset_index(name='FLIGHT_COUNT'))
    chart = alt.Chart(plot_data).mark_bar().encode(
        x='DAY_OF_WEEK:O',  # Ordinal data
        y='FLIGHT_COUNT:Q',  # Quantitative data
        color='AIRLINE_CODE:N',  # Nominal data
        tooltip=['DAY_OF_WEEK', 'AIRLINE_CODE', 'FLIGHT_COUNT']
    ).properties(
        width='container', 
        height='container',
        title='Count of Unique Flights by Day of the Week'
    ).configure_axis(
        labelAngle=0  # Adjust label angle if necessary
    ).to_dict(format = "vega")
    return chart
    

def _plot_bar_plot(df):
    average_delay = df[['AIRLINE', 'ARR_DELAY']].groupby('AIRLINE', as_index=False).mean(numeric_only=True)
    chart = alt.Chart(average_delay).mark_bar().encode(
        y=alt.Y('AIRLINE', sort=alt.EncodingSortField(field='ARR_DELAY', order='descending')),
        x=alt.X('ARR_DELAY', title='Average Delay (minutes)'),
        color=alt.Color('AIRLINE', legend=None),  # Optional color encoding by airline_name
        tooltip=['AIRLINE', 'ARR_DELAY']
        ).properties(
        width='container', 
        height='container',
        ).to_dict(format = "vega")
    return chart



def _plot_hist_plot(df):
    alt.data_transformers.enable('default')
    return alt.Chart(df).transform_joinaggregate(
        total='count(*)'
    ).transform_calculate(
        pct='1 / datum.total'
    ).mark_bar().encode(
        x=alt.X('ARR_DELAY:Q', bin=alt.Bin(step=30), title='Delay (minutes)'),
        y=alt.Y('sum(pct):Q', axis=alt.Axis(format='.0%'), title='Percentage of Total Flights')
    ).properties(
        width='container', 
        height='container'
    ).to_dict()

def _plot_map(origin, destination, cities_lat_long):
    
    us_states = alt.topo_feature(data.us_10m.url, 'states')

    # Define origin and destination coordinates
    origin_city = origin.split(",")[0]
    if '/' in origin_city:
        origin_city = origin_city.split("/")[0]

    dest_city = destination.split(",")[0]
    if '/' in dest_city:
        dest_city = dest_city.split("/")[0]

    origin_lat, origin_long = cities_lat_long[origin_city]
    dest_lat, dest_long = cities_lat_long[dest_city]



    origin = {'city': origin_city, 'latitude': origin_lat, 'longitude': origin_long}
    destination = {'city': dest_city, 'latitude': dest_lat, 'longitude': dest_long}

    # Create DataFrame for points
    points_df = pd.DataFrame([origin, destination])

    # Create DataFrame for the line
    line_df = pd.DataFrame({
        'latitude': [origin['latitude'], destination['latitude']],
        'longitude': [origin['longitude'], destination['longitude']]
    })

    # Create a map of the US
    us_map = alt.Chart(us_states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).properties(
        width='container', 
        height='container',
    ).project('albersUsa')

    # Plot points
    points = alt.Chart(points_df).mark_point(
        filled=True,
        color='red'
    ).encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        tooltip=['city:N']
    )

    # Plot lines
    lines = alt.Chart(line_df).mark_line(
        color='blue'
    ).encode(
        longitude='longitude:Q',
        latitude='latitude:Q'
    )
    chart = (us_map + points + lines).to_dict(format = "vega")
    return chart

@app.callback(
    Output('dest_dropdown', 'options'),
    Input('origin_dropdown', 'value')
)
def update_destination_options(selected_origin):
    filtered_df = df[df['ORIGIN_CITY'] == selected_origin]
    destinations = filtered_df['DEST_CITY'].unique()
    dest_options = [{'label': dest, 'value': dest} for dest in destinations]
    return dest_options

@app.callback(
    Output('origin_dropdown', 'options'),
    Input('dest_dropdown', 'value')
)
def update_origin_options(selected_destination):
    filtered_df = df[df['DEST_CITY'] == selected_destination]
    origins = filtered_df['ORIGIN_CITY'].unique()
    origin_options = [{'label': origin, 'value': origin} for origin in origins]
    return origin_options


@callback(
    Output('flights_on_time', 'children'),
    Output('avg_flight_time', 'children'),
    Output('avg_delay', 'children'),
    Output('bar', 'spec'),
    Output('stacked_plot', 'spec'),
    Output('hist', 'spec'),
    Output('map_plot', 'spec'),
    Input('origin_dropdown', 'value'),
    Input('dest_dropdown', 'value'),
    Input('year_range', 'value')
)
def cb(origin_dropdown, dest_dropdown, year_range):

    # temporarily disable multi dest
    if isinstance(dest_dropdown, list):
        dest_dropdown = dest_dropdown[0]
    msk = ((df['ORIGIN_CITY'] == origin_dropdown)
           & (df['DEST_CITY'] == dest_dropdown)
           & (pd.DatetimeIndex(df['FL_DATE'].to_numpy()).year >= year_range[0])
           & (pd.DatetimeIndex(df['FL_DATE'].to_numpy()).year <= year_range[1]))

    _df = df.loc[msk, :]
    bar_plot = _plot_bar_plot(_df)
    hist_plot = _plot_hist_plot(_df)


    # flights on time
    pct_flights_on_time = __pct_on_time_calc(_df.loc[:, 'ARR_DELAY'].to_numpy())
    pct_flights_on_time = [dbc.CardHeader('Flights on Time'),
                           dbc.CardBody(f'{pct_flights_on_time:.2f}%')]

    # avg flight time
    f_hrs, f_mins = __avg_flight_time(_df.loc[:, 'AIR_TIME'].to_numpy()) # numerical value in minutes
    # card to return
    avg_flight_time = [dbc.CardHeader('Average Flight Time'),
                       dbc.CardBody(f'{f_hrs}h {f_mins}min')] # card to return

    # average delay
    _avg_delay = __avg_delay(_df.loc[:, 'ARR_DELAY'].to_numpy())
    avg_delay = [dbc.CardHeader('Average Delay'),
                 dbc.CardBody(f'{int(_avg_delay)}')] # card to return

    bar_plot = _plot_bar_plot(_df)
    hist_plot = _plot_hist_plot(_df)
    stacked_bar_plot = plot_stacked(_df)
    map_plot = _plot_map(origin_dropdown, dest_dropdown, cities_lat_long)

    return pct_flights_on_time, avg_flight_time, avg_delay, bar_plot, stacked_bar_plot, hist_plot, map_plot

  
# Run the app/dashboard
if __name__ == '__main__':
    app.run_server(debug = True, host = '127.0.0.1')
