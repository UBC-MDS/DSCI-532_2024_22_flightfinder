import pandas as pd
import altair as alt

SCHEME = 'viridis'

def plot_stacked(df):
    day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    plot_data = (df.groupby(['DAY_OF_WEEK', 'AIRLINE'])
                               .agg(FLIGHT_COUNT=('FL_NUMBER', 'nunique'))
                               .reset_index())
    chart = alt.Chart(plot_data).mark_bar().encode(
        x=alt.X('DAY_OF_WEEK:O', axis=alt.Axis(title='Day of the Week'), sort=day_order),  # Ordinal data
        y=alt.Y('FLIGHT_COUNT:Q', axis=alt.Axis(title='Number of Unique Flights')),  # Quantitative data
        color=alt.Color('AIRLINE:N', scale=alt.Scale(scheme=SCHEME)),  # Nominal data
        tooltip=['DAY_OF_WEEK', 'AIRLINE', 'FLIGHT_COUNT']
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
        y=alt.Y('AIRLINE', sort=alt.EncodingSortField(field='ARR_DELAY', order='descending'), title=''),
        x=alt.X('ARR_DELAY', title='Average Delay (minutes)'),
        color=alt.Color('ARR_DELAY', legend=None, scale=alt.Scale(scheme=SCHEME)),  # Optional color encoding by airline_name
        tooltip=['AIRLINE', 'ARR_DELAY']
        ).properties(
        width='container', 
        height='container',
        ).to_dict(format = "vega")
    return chart




def plot_hist_plot(df):
    alt.data_transformers.enable('default')
    bind = alt.selection_interval(bind='scales')
    
    base_chart = alt.Chart(df).transform_joinaggregate(
        total='count(*)',  # Compute total number of flights once
    ).transform_calculate(
        pct='1 / datum.total'  # Calculate the reciprocal of the total count
    )
    
    # Create a cumulative sum of percentages for calculating delays by at least this amount
    cumulative_chart = base_chart.transform_window(
        cumulative_pct='sum(pct)',
        sort=[{'field': 'ARR_DELAY', 'order': 'descending'}]  # Cumulative from highest to lowest
    ).mark_bar().encode(
        x=alt.X('ARR_DELAY:Q', title='Delay (minutes)'),
        y=alt.Y('sum(pct):Q', axis=alt.Axis(format='.0%'), title='Percentage of Total Flights'),
        tooltip=[
            alt.Tooltip('ARR_DELAY:Q', title='Delay (minutes)'),
            alt.Tooltip('cumulative_pct:Q', format='.0%', title='Probability of Being Delayed by at Least This Amount')
        ]
    ).properties(
        width='container', 
        height='container'
    ).add_selection(
        bind
    )
    return cumulative_chart.to_dict()

