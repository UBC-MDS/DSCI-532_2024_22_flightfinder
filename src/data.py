import pandas as pd

df = pd.read_csv('data/processed/data.gzip', compression='gzip',
                 usecols=['ORIGIN_CITY',
                          'DEST_CITY',
                          'ARR_DELAY',
                          'FL_DATE',
                          'AIR_TIME',
                          'AIRLINE',
                          'AIRLINE_CODE',
                          'AIRLINE'])

all_origin = df['ORIGIN_CITY'].unique()
all_dest = df['DEST_CITY'].unique()

df['year'] = pd.DatetimeIndex(df['FL_DATE'].to_numpy()).year
df.set_index(['ORIGIN_CITY', 'DEST_CITY', 'year'], inplace=True)