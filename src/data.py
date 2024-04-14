import pandas as pd

df = pd.read_csv('data/processed/df.gzip', compression='gzip',
                 usecols=['ORIGIN_CITY',
                          'DEST_CITY',
                          'ARR_DELAY',
                          'FL_DATE',
                          'AIR_TIME',
                          'FL_NUMBER',
                          'AIRLINE_CODE',
                          'AIRLINE',
                          'FL_NUMBER'])

all_origin = df['ORIGIN_CITY'].unique()
all_dest = df['DEST_CITY'].unique()

df['year'] = pd.DatetimeIndex(df['FL_DATE'].to_numpy()).year
df.set_index(['ORIGIN_CITY', 'DEST_CITY', 'year'], inplace=True)


cities = pd.read_csv('data/raw/updated_usa_airports.csv')
cities_lat_long = cities.set_index('city')[['latitude', 'longitude']].apply(tuple, axis=1).to_dict()