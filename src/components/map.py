import pandas as pd
import altair as alt
from vega_datasets import data


def plot_map(origin, destination, cities_lat_long):

    us_states = alt.topo_feature(data.us_10m.url, 'states')

    us_map = alt.Chart(us_states).mark_geoshape(
        fill='rgba(25, 135, 140, 0.2)',
        stroke='white'
    ).properties(
        width='container', 
        height='container',
    ).project('albersUsa')

    if not origin or not destination:
        return us_map.to_dict()
    
    def process_city(city_name):
        if '/' in city_name:
            return city_name.split('/')[0]
        return city_name.split(',')[0]
    
    origin_city = process_city(origin)
    dest_city = process_city(destination)

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

    # Plot points
    points = alt.Chart(points_df).mark_point(
        filled=True,
        color='cyan',
        size=50,
        shape='square',
        stroke='rgba(25, 135, 140)',
        strokeWidth=1
    ).encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        tooltip=['city:N']
    )

    labels = alt.Chart(points_df).mark_text(
        align='left',
        baseline='middle',
        dx=7,
        dy=3,
        fontWeight='bold',
        
    ).encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        text='city'
    )

    # Plot lines
    lines = alt.Chart(line_df).mark_line(
        color='rgba(25, 135, 140)'
    ).encode(
        longitude='longitude:Q',
        latitude='latitude:Q'
    )

    chart = (us_map + lines + points + labels).to_dict(format = "vega")
    return chart