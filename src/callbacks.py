import numpy as np
from dash import Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
from typing import Tuple
import altair as alt
from vega_datasets import data

from data import df, cities_lat_long
alt.data_transformers.enable('vegafusion')

def pct_on_time_calc(delay_times: np.ndarray) -> Tuple[int, float]:

    # consider delay less than this number to be on time
    tol = 5
    if delay_times.size > 0:
        return (delay_times <= tol).sum() / delay_times.size * 100
    return 0.0


def avg_flight_time(flight_times: np.ndarray) -> Tuple[int, int]:
    if flight_times.size > 0:
        m = np.nanmean(flight_times)
        if isinstance(m, float):
            hrs = int(m // 60)
            mins = int(m % 60)
            return hrs, mins
    return 0, 0


def avg_delay(delay_times: np.ndarray) -> float:
    if delay_times.size > 0:
        m = np.nanmean(delay_times)
        return m
    return 0

  

def plot_stacked(df):

    _filtered_df = df.copy()
    _filtered_df['DAY_OF_WEEK'] = pd.to_datetime(_filtered_df['FL_DATE']).dt.day_name().apply(lambda x: x[:3])
    _filtered_df['FLIGHT_ID'] = _filtered_df['AIRLINE'] + '-' + _filtered_df['AIRLINE_CODE']
    plot_data = (_filtered_df.groupby(['DAY_OF_WEEK', 'AIRLINE_CODE'])
                               .agg(FLIGHT_COUNT=('FLIGHT_ID', 'nunique'))
                               .reset_index())
    chart = alt.Chart(plot_data).mark_bar().encode(
        x='DAY_OF_WEEK:O',  # Ordinal data
        y='FLIGHT_COUNT:Q',  # Quantitative data
        color='AIRLINE_CODE:N',  # Nominal data
        tooltip=['DAY_OF_WEEK', 'AIRLINE_CODE', 'FLIGHT_COUNT']
    ).properties(
        width='container', 
        height='container'
    ).configure_axis(
        labelAngle=0  # Adjust label angle if necessary
    ).to_dict(format = "vega")
    return chart
    

def plot_bar_plot(df):
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



def plot_hist_plot(df):
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

def plot_map(origin, destination, cities_lat_long):

    us_states = alt.topo_feature(data.us_10m.url, 'states')

    if not origin or not destination:
        us_map = alt.Chart(us_states).mark_geoshape(
            fill='lightgray',
            stroke='white'
        ).properties(
            width='container',
            height='container'
        ).project('albersUsa')

        return us_map.to_dict()
    
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
    pct_flights_on_time = [dbc.CardHeader('Flights on Time'),
                           dbc.CardBody(f'{pct_flights_on_time:.2f}%')]

    # avg flight time
    f_hrs, f_mins = avg_flight_time(_df.loc[:, 'AIR_TIME'].to_numpy()) # numerical value in minutes
    # card to return
    _avg_flight_time = [dbc.CardHeader('Average Flight Time'),
                       dbc.CardBody(f'{f_hrs}h {f_mins}min')] # card to return

    # average delay
    tmp_avg_delay = avg_delay(_df.loc[:, 'ARR_DELAY'].to_numpy())
    _avg_delay = [dbc.CardHeader('Average Delay'),
                 dbc.CardBody(f'{int(tmp_avg_delay)}min')] # card to return

    bar_plot = plot_bar_plot(_df)
    hist_plot = plot_hist_plot(_df)
    stacked_bar_plot = plot_stacked(_df)
    map_plot = plot_map(origin_dropdown, dest_dropdown, cities_lat_long)

    return pct_flights_on_time, _avg_flight_time, _avg_delay, bar_plot, stacked_bar_plot, hist_plot, map_plot