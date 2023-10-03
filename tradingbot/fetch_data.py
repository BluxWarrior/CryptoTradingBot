import cbpro
import pandas as pd

public_client = cbpro.PublicClient()

short_period = 50
long_period = 200
product_id = 'BTC-USD'

def calculate_moving_averages(df, short_period, long_period):
    df['MA50'] = df['close'].rolling(window=short_period).mean()
    df['MA200'] = df['close'].rolling(window=long_period).mean()
    return df

def fetch_data(granularity):
    data = public_client.get_product_historic_rates(product_id, granularity=granularity)
    df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S') # Convert datetime to string

    # initialize the new dataframe
    new_df = df['time']

    df.set_index('time', inplace=True)
    df.sort_index(ascending=True, inplace=True)

    df = calculate_moving_averages(df, short_period, long_period)

    df.reset_index(level=0, inplace=True)
    new_df = df[['time', 'close', 'MA50', 'MA200']]

    # # get the specific columns
    # print(new_df.tail())
    # new_df = pd.concat([new_df, df[['close', 'MA50', 'MA200']]], axis=1)
    # # [200:]
    # print(new_df.tail())
    new_df = new_df.rename(columns={'close': 'price'})[250:]
    
    # # print(new_df.tail())
    json_data = new_df.to_json(orient='records')
    return json_data

# print(fetch_data('BTC-USD', 300))