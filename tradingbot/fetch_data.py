import cbpro
import pandas as pd

public_client = cbpro.PublicClient()

def calculate_moving_averages(df, short_period, long_period):
    df['50_MA'] = df['close'].rolling(window=short_period).mean()
    df['200_MA'] = df['close'].rolling(window=long_period).mean()
    return df

def fetch_data(product_id, granularity, short_period, long_period):
    data = public_client.get_product_historic_rates(product_id, granularity=granularity)
    df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    df.sort_index(ascending=True, inplace=True)

    df = calculate_moving_averages(df, short_period, long_period)
    return df

print(fetch_data('BTC-USD', 300, 50, 200))