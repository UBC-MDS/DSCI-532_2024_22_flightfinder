from dash import Input, Output, callback
import dash_bootstrap_components as dbc
import altair as alt
from src.data import df, cities_lat_long
alt.data_transformers.enable('vegafusion')

from src.components.cards import pct_on_time_calc, avg_flight_time, avg_delay
from src.components.charts import plot_stacked, plot_bar_plot, plot_hist_plot
from src.components.map import plot_map


@callback(
    Output('dest_dropdown', 'options'),
    Input('origin_dropdown', 'value')
)
def update_destination_options(selected_origin):
    _df = df.copy().reset_index()
    if not selected_origin:  # This checks if selected_origin is None or an empty string
        # Reset to show all destinations
        all_destinations = _df['DEST_CITY'].unique()
        return [{'label': dest, 'value': dest} for dest in all_destinations]
    else:
        filtered_df = _df[_df['ORIGIN_CITY'] == selected_origin]
        destinations = filtered_df['DEST_CITY'].unique()
        return [{'label': dest, 'value': dest} for dest in destinations]

@callback(
    Output('origin_dropdown', 'options'),
    Input('dest_dropdown', 'value')
)
def update_origin_options(selected_destination):
    _df = df.copy().reset_index()
    if not selected_destination:  # This checks if selected_destination is None or an empty string
        # Reset to show all origins
        all_origins = _df['ORIGIN_CITY'].unique()
        return [{'label': origin, 'value': origin} for origin in all_origins]
    else:
        filtered_df = _df[_df['DEST_CITY'] == selected_destination]
        origins = filtered_df['ORIGIN_CITY'].unique()
        return [{'label': origin, 'value': origin} for origin in origins]


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

    _df = df.loc[(origin_dropdown, dest_dropdown, year_range), :].copy()
    _df.reset_index(inplace=True)

    # flights on time
    pct_flights_on_time = pct_on_time_calc(_df.loc[:, 'ARR_DELAY'].to_numpy())
    pct_flights_on_time = [dbc.CardHeader('Flights on Time', style={'backgroundColor': 'rgb(25, 135, 140)',
                                                                    'color': 'white',
                                                                    'textAlign': 'center',
                                                                    'fontSize': '20px'}),
                           dbc.CardBody(f'{int(pct_flights_on_time)}%', style={'textAlign': 'center',
                                                                               'fontSize': '40px'})]

    # avg flight time
    f_hrs, f_mins = avg_flight_time(_df.loc[:, 'AIR_TIME'].to_numpy()) # numerical value in minutes
    # card to return
    _avg_flight_time = [dbc.CardHeader('Average Flight Time', style={'backgroundColor': 'rgb(25, 135, 140)',
                                                                     'color': 'white',
                                                                     'textAlign': 'center',
                                                                     'fontSize': '20px'}),
                       dbc.CardBody(f'{f_hrs}h {f_mins}min', style={'textAlign': 'center',
                                                                    'fontSize': '40px'})] # card to return

    # average delay
    tmp_avg_delay = avg_delay(_df.loc[:, 'ARR_DELAY'].to_numpy())
    _avg_delay = [dbc.CardHeader('Average Delay', style={'backgroundColor': 'rgb(25, 135, 140)',
                                                         'color': 'white',
                                                         'textAlign': 'center',
                                                         'fontSize': '20px'}),
                 dbc.CardBody(f'{int(tmp_avg_delay)}min', style={'textAlign': 'center',
                                                                 'fontSize': '40px'})] # card to return

    bar_plot = plot_bar_plot(_df)
    hist_plot = plot_hist_plot(_df)
    stacked_bar_plot = plot_stacked(_df)
    map_plot = plot_map(origin_dropdown, dest_dropdown, cities_lat_long)

    return pct_flights_on_time, _avg_flight_time, _avg_delay, bar_plot, stacked_bar_plot, hist_plot, map_plot
