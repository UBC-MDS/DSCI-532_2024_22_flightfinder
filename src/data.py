import pandas as pd
import numpy as np
import pickle

df = pd.read_parquet('data/processed/data.parquet')

with open('data/processed/all_origin.npy', 'rb') as f:
    all_origin = np.load(f, allow_pickle=True)
with open('data/processed/all_dest.npy', 'rb') as f:
    all_dest = np.load(f, allow_pickle=True)

with open('data/processed/cities_lat_long', 'rb') as f:
    cities_lat_long = pickle.load(f)

# cities = pd.read_csv('data/raw/updated_usa_airports.csv')
# cities_lat_long = cities.set_index('city')[['latitude', 'longitude']].apply(tuple, axis=1).to_dict()
