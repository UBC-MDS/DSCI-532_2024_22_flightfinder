import numpy as np
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import pandas as pd
import altair as alt


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

df = pd.read_csv('data/raw/flights_sample_3m.csv',
                 usecols=['ORIGIN_CITY',
                          'DEST_CITY',
                          'ARR_DELAY',
                          'FL_DATE',
                          'AIR_TIME',
                          'AIRLINE_CODE'])
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
    dvc.Vega(id='bar', spec={})
])
# graph_avg_delay_by_carrier = dvc.Vega(id='bar', spec={})

graph_number_unique_flights = html.Div([
    html.P('Number of unique flights'), 
    dvc.Vega(id='stacked_plot', spec={})
])
# graph_number_unique_flights = dvc.Vega(id='stacked_plot', spec={})

graph_map = html.Div([
    html.P('Map')
])

# graph_count_by_delay = html.Div([
#     html.P('Count by delay')
# ])
graph_count_by_delay = dvc.Vega(id='hist', spec={})


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

def plot_stacked(df):
    _filtered_df = df.copy()
    _filtered_df['DAY_OF_WEEK'] = pd.to_datetime(_filtered_df['FL_DATE']).dt.day_name()
    plot_data = (_filtered_df.groupby(['DAY_OF_WEEK', 'AIRLINE_CODE'])
                               .size()
                               .reset_index(name='FLIGHT_COUNT'))
    chart = alt.Chart(plot_data).mark_bar().encode(
        x='DAY_OF_WEEK:O',  # Ordinal data
        y='FLIGHT_COUNT:Q',  # Quantitative data
        color='AIRLINE_CODE:N',  # Nominal data
        tooltip=['DAY_OF_WEEK', 'AIRLINE_CODE', 'FLIGHT_COUNT']
    ).properties(
        width=350,
        height=350,
        title='Count of Unique Flights by Day of the Week'
    ).configure_axis(
        labelAngle=0  # Adjust label angle if necessary
    ).to_dict()
    return chart
    

def _plot_bar_plot(df):
    average_delay = df[['AIRLINE_CODE', 'ARR_DELAY']].groupby('AIRLINE_CODE', as_index=False).mean(numeric_only=True)
    chart = alt.Chart(average_delay).mark_bar().encode(
        y='AIRLINE_CODE',
        x='ARR_DELAY',
        color=alt.Color('AIRLINE_CODE', legend=None),  # Optional color encoding by airline_name
        tooltip=['AIRLINE_CODE', 'ARR_DELAY']
        ).properties(
            width=400,
            height=200,
            title='Average Delay Time by Carrier'
        ).to_dict()
    return chart


def _plot_hist_plot(df):
    chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('ARR_DELAY', bin=alt.Bin(maxbins=100), title='Delay (minutes)'),
    y=alt.Y('count()', title='Frequency')
    ).properties(
        title='Histogram of Delay Minutes'
    ).to_dict()
    return chart

@callback(
    Output('flights_on_time', 'children'),
    Output('avg_flight_time', 'children'),
    Output('avg_delay', 'children'),
    Output('bar', 'spec'),
    Output('stacked_plot', 'spec'),
    Output('hist', 'spec'),
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


    # # avg flight time
    # _avg_flight_time = _df[:, 'AIR_TIME'].mean() # numerical value in minutes
    # # card to return
    # avg_flight_time = [dbc.CardHeader('Flights on Time'),
    #                    dbc.CardBody(f'{_avg_flight_time}')] # card to return
    stacked_bar_plot = plot_stacked(_df)

    return None, None, None, bar_plot, stacked_bar_plot, hist_plot

# Run the app/dashboard
if __name__ == '__main__':
    # app.run()
    app.run_server(debug = True, host = '127.0.0.1')