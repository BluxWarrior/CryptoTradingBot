from coinbaseadvanced.client import CoinbaseAdvancedTradeAPIClient
import dotenv
import uuid
import os
import cbpro
import pandas as pd
import time

dotenv.load_dotenv("dev.env", override=True)

api_key = os.getenv('API_KEY')
secret_key = os.getenv('API_SECRET')


# Public Client
public_client = cbpro.PublicClient()

# advanced Client
advanced_client = CoinbaseAdvancedTradeAPIClient(api_key=api_key, secret_key=secret_key)

# initialize
granularity = 300
short_period = 50
long_period = 200
product_id = 'BTC-USD'
last_ordered_time = None
iscross = False


def get_balance():
    accounts_page = advanced_client.list_accounts()
    USD_balance = float([account.available_balance.value for account in accounts_page.accounts if account.available_balance.currency == 'USD'][0])
    BTC_balance = float([account.available_balance.value for account in accounts_page.accounts if account.available_balance.currency == 'BTC'][0])

    return {'USD':USD_balance, 'BTC':BTC_balance}

def get_current_price():
    ticker = public_client.get_product_ticker(product_id='BTC-USD')

    # Print the latest price
    print(ticker['price'])

def fetch_data(granularity):
    data = public_client.get_product_historic_rates(product_id, granularity=granularity)
    df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S') # Convert datetime to string

    # initialize the new dataframe

    df.set_index('time', inplace=True)
    df.sort_index(ascending=True, inplace=True)

    # calculate moving averages
    df['MA50'] = df['close'].rolling(window=short_period).mean()
    df['MA200'] = df['close'].rolling(window=long_period).mean()

    df.reset_index(level=0, inplace=True)
    return df

def check_conditions(df):
    latest_row = df.iloc[-1]
    price = get_current_price
    is_above_MA50 = latest_row['close'] > latest_row['MA50']
    is_above_MA200 = latest_row['close'] > latest_row['MA200']


    if latest_row['MA50'] > latest_row['MA200']:
        if is_above_MA50:
            global iscross
            if iscross == False:
                iscross = True
                return 'buy'
            else:
                return None
        elif not is_above_MA50:
            if iscross == True:
                iscross = False
                return 'sell'
            else:
                return None
    elif latest_row['MA50'] < latest_row['MA200']:
        if is_above_MA200:
            if iscross == False:
                iscross = True
                return 'buy'
            else:
                return None
        elif not is_above_MA200:
            if iscross == True:
                iscross = False
                return 'sell'
            else:
                return None
    return None

def generate_client_order_id():
    return str(uuid.uuid4())

def place_order(action):
    # try:
    if action == 'buy':
        # fetch your USD amount
        usd_amount = int(get_balance()['USD']*100)/100

        client_order_id = generate_client_order_id()
        advanced_client.create_buy_market_order(client_order_id=client_order_id, product_id="BTC-USD", quote_size=usd_amount)
        print(usd_amount)
        
        return usd_amount
    elif action == 'sell':
        # fetch your btc amount
        btc_amount = int(get_balance()['BTC']*1000000)/1000000

        client_order_id = generate_client_order_id()
        r = advanced_client.create_sell_market_order(client_order_id=client_order_id, product_id="BTC-USD", base_size=btc_amount)
        print(btc_amount)
        # primary_account.sell(amount=str(amount), currency='BTC', payment_method=payment_ID)
        return btc_amount
    return False

def ordering(df):
    # print(df.tail())
    action = check_conditions(df)

    if action:
        print(f'Executing {action} order')
        status = place_order(action)
        if status:
            print("Sucessfully ordered")
        else:
            print("Order was failed")
    else:
        print("No action to be taken")

def trading(granularity):
    df = fetch_data(granularity)
    currenttime = df.iloc[-1]['time']
    global last_ordered_time
    if last_ordered_time != currenttime:
        print(currenttime)
        last_ordered_time = currenttime
        ordering(df)


while True:
    trading(granularity)
    time.sleep(10)

# print(place_order('sell'))
# product_candles = advanced_client.get_product_candles(product_id="BTC-USD", granularity=300)