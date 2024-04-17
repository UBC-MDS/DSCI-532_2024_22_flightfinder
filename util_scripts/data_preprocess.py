import pandas as pd
import numpy as np
import pickle

df = pd.read_csv('data/raw/flights_sample_3m.csv',
                 usecols = ['ORIGIN_CITY',
                            'DEST_CITY',
                            'ARR_DELAY',
                            'FL_DATE',
                            'AIR_TIME',
                            'AIRLINE',
                            'AIRLINE_CODE',
                            'FL_NUMBER'])

all_origin = df['ORIGIN_CITY'].unique()
with open('data/processed/all_origin.npy', 'wb') as f:
    np.save(f, all_origin)

all_dest = df['DEST_CITY'].unique()
with open('data/processed/all_dest.npy', 'wb') as f:
    np.save(f, all_dest)

df = df.astype({'ARR_DELAY': 'float32'})
df['year'] = pd.DatetimeIndex(df['FL_DATE'].to_numpy()).year
df.set_index(['ORIGIN_CITY', 'DEST_CITY', 'year'], inplace=True)

df.to_parquet('data/processed/data.parquet')

cities = pd.read_csv('data/raw/updated_usa_airports.csv')
cities_lat_long = cities.set_index('city')[['latitude', 'longitude']].apply(tuple, axis=1).to_dict()
with open('data/processed/cities_lat_long', 'wb') as f:
    pickle.dump(cities_lat_long, f)

