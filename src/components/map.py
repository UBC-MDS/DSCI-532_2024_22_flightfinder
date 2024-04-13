import pandas as pd
import altair as alt
from vega_datasets import data


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