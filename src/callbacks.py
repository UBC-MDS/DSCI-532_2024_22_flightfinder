from dash import Input, Output, callback, State
import dash_bootstrap_components as dbc
from dash import callback_context
import altair as alt
from src.data import df, cities_lat_long
alt.data_transformers.enable('vegafusion')

from src.components.cards import pct_on_time_calc, avg_flight_time, avg_delay
from src.components.charts import plot_stacked, plot_bar_plot, plot_hist_plot
from src.components.map import plot_map
#import functools


#@functools.lru_cache()
@callback(
    Output('dest_dropdown', 'options'),
    Input('origin_dropdown', 'value')
)
def update_destination_options(selected_origin):
    _df = df[[]].copy().reset_index()
    if not selected_origin:  # This checks if selected_origin is None or an empty string
        # Reset to show all destinations
        all_destinations = _df['DEST_CITY'].unique()
        return [{'label': dest, 'value': dest} for dest in all_destinations]
    else:
        filtered_df = _df[_df['ORIGIN_CITY'] == selected_origin]
        destinations = filtered_df['DEST_CITY'].unique()
        return [{'label': dest, 'value': dest} for dest in destinations]


#@functools.lru_cache()
@callback(
    Output('origin_dropdown', 'options'),
    Input('dest_dropdown', 'value')
)
def update_origin_options(selected_destination):
    _df = df[[]].copy().reset_index()
    if not selected_destination:  # This checks if selected_destination is None or an empty string
        # Reset to show all origins
        all_origins = _df['ORIGIN_CITY'].unique()
        return [{'label': origin, 'value': origin} for origin in all_origins]
    else:
        filtered_df = _df[_df['DEST_CITY'] == selected_destination]
        origins = filtered_df['ORIGIN_CITY'].unique()
        return [{'label': origin, 'value': origin} for origin in origins]
    

@callback(
    [
        Output('flights_on_time', 'children'),
        Output('avg_flight_time', 'children'),
        Output('avg_delay', 'children'),
        Output('bar', 'spec'),
        Output('stacked_plot', 'spec'),
        Output('hist', 'spec'),
        Output('map_plot', 'spec')
    ],
    [
        Input('submit_button', 'n_clicks')
    ],
    [
        State('origin_dropdown', 'value'),
        State('dest_dropdown', 'value'),
        State('year_range', 'value')
    ]
)
def update_charts(n_clicks, origin_dropdown, dest_dropdown, year_range):
    ctx = callback_context
    if not ctx.triggered or ctx.triggered[0]['prop_id'] == 'submit_button.n_clicks' and n_clicks is None:
        return cb(origin_dropdown, dest_dropdown, year_range)
    elif ctx.triggered:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == 'submit_button':
            return cb(origin_dropdown, dest_dropdown, year_range)

    return [], [], [], None, None, None, None

def cb(origin_dropdown, dest_dropdown, year_range):

    # temporarily disable multi dest
    if isinstance(dest_dropdown, list):
        dest_dropdown = dest_dropdown[0]

    origin = origin_dropdown if origin_dropdown is not None else slice(None)
    destination = dest_dropdown if dest_dropdown is not None else slice(None)
    year = year_range if year_range is not None else slice(None)

    # Define columns to load based on input conditions
    if origin_dropdown is not None and dest_dropdown is not None:
        # If specific origin and destination are provided, load all necessary data columns
        necessary_columns = slice(None)  # This selects all columns
    else:
        # If not both are provided, just work with the index or no specific data columns needed
        necessary_columns = []

    # Load data from the DataFrame
    if necessary_columns:
        _df = df.loc[(origin, destination, year), necessary_columns].copy()
        _df.reset_index(inplace=True)  # This might be necessary if you need to manipulate the index columns as data columns
    else:
        # Minimal load, assuming index information is self-sufficient for the required operation
        _df = df.loc[(origin, destination, year)].copy()
        _df.reset_index(inplace=True)

    # flights on time
    pct_flights_on_time = pct_on_time_calc(_df.loc[:, 'ARR_DELAY'].to_numpy())
    pct_flights_on_time = [dbc.CardHeader('Flights on Time', style={'backgroundColor': 'rgb(25, 135, 140)',
                                                                    'color': 'white',
                                                                    'textAlign': 'center',
                                                                    'fontSize': '20px'}),
                           dbc.CardBody(f'{int(pct_flights_on_time)}%', style={'textAlign': 'center',
                                                                               'fontSize': '35px'})]

    # avg flight time
    f_hrs, f_mins = avg_flight_time(_df.loc[:, 'AIR_TIME'].to_numpy()) # numerical value in minutes
    # card to return
    _avg_flight_time = [dbc.CardHeader('Average Flight Time', style={'backgroundColor': 'rgb(25, 135, 140)',
                                                                     'color': 'white',
                                                                     'textAlign': 'center',
                                                                     'fontSize': '20px'}),
                       dbc.CardBody(f'{f_hrs}h {f_mins}min', style={'textAlign': 'center',
                                                                    'fontSize': '35px'})] # card to return

    # average delay
    tmp_avg_delay = avg_delay(_df.loc[:, 'ARR_DELAY'].to_numpy())
    _avg_delay = [dbc.CardHeader('Average Delay', style={'backgroundColor': 'rgb(25, 135, 140)',
                                                         'color': 'white',
                                                         'textAlign': 'center',
                                                         'fontSize': '20px'}),
                 dbc.CardBody(f'{int(tmp_avg_delay)}min', style={'textAlign': 'center',
                                                                 'fontSize': '35px'})] # card to return

    if origin_dropdown is not None and dest_dropdown is not None:
        bar_plot = plot_bar_plot(_df)
        hist_plot = plot_hist_plot(_df)
        stacked_bar_plot = plot_stacked(_df)
    else:
        bar_plot = None
        hist_plot = None
        stacked_bar_plot = None

    map_plot = plot_map(origin_dropdown, dest_dropdown, cities_lat_long)

    return pct_flights_on_time, _avg_flight_time, _avg_delay, bar_plot, stacked_bar_plot, hist_plot, map_plot
