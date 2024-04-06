import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('data/raw/flights_sample_3m.csv',
                     usecols=['ORIGIN_CITY',
                              'DEST_CITY',
                              'ARR_DELAY',
                              'FL_DATE',
                              'AIR_TIME',
                              'AIRLINE',
                              'AIRLINE_CODE'])
    df.to_csv('data/processed/data.gzip', compression='gzip')
