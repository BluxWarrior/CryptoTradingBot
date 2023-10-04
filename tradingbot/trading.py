import cbpro
import pandas as pd
import dotenv
from coinbaseadvanced.client import CoinbaseAdvancedTradeAPIClient
import json
from coinbase.wallet.client import Client
import time

dotenv.load_dotenv("dev.env", override=True)
import os

api_key = os.getenv('API_KEY')
secret_key = os.getenv('API_SECRET')


# Public Client
public_client = cbpro.PublicClient()

# advanced Client
advanced_client = CoinbaseAdvancedTradeAPIClient(api_key=api_key, secret_key=secret_key)

# Authorized Client
auth_client = Client(api_key, secret_key)
primary_account = auth_client.get_primary_account()
payment_methods = auth_client.get_payment_methods()
payment_ID = payment_methods[0]['id']

# import history
with open("ordering_history.json", "r") as f:
    ordering_history = json.load(f)

granularity = 300
short_period = 50
long_period = 200
product_id = 'BTC-USD'
last_ordered_time = None
iscross = True

def get_balance():
    accounts_page = advanced_client.list_accounts()
    USD_balance = float([account.available_balance.value for account in accounts_page.accounts if account.available_balance.currency == 'USD'][0])
    BTC_balance = float([account.available_balance.value for account in accounts_page.accounts if account.available_balance.currency == 'BTC'][0])

    return {'USD':USD_balance, 'BTC':BTC_balance}

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
    new_df = df[['time', 'close', 'MA50', 'MA200']]
    new_df = new_df.rename(columns={'close': 'price'})[250:]
    
    # convert to the json format
    new_df = new_df.to_json(orient='records')
    new_df = json.loads(new_df)

    # get the current balance
    balance = get_balance()
    json_data = {"historical_data": new_df, "balance": balance}
    return json_data

def check_conditions(historical_data):
    latest_row = historical_data[-1]
    is_above_MA50 = latest_row['price'] > latest_row['MA50']
    is_above_MA200 = latest_row['price'] > latest_row['MA200']

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

def place_order(action):
    try:
        if action == 'buy':
            # accounts = auth_client.get_accounts()
            # fetch your USD account
            usd_amount = int(get_balance()['USD']*0.95)
            # print(usd_amount-10)
            # break
            btc_price = auth_client.get_buy_price(currency_pair='BTC-USD')

            # Calculate how much BTC to buy for the specified USD amount
            amount = usd_amount / float(btc_price.amount)
            primary_account.buy(amount=str(amount), currency='BTC', payment_method=payment_ID)
            
            return usd_amount
        elif action == 'sell':
            amount = get_balance()['BTC']
            primary_account.sell(amount=str(amount), currency='BTC', payment_method=payment_ID)
            return amount
        return False
    except:
        return False


def ordering(data):
    balance = data['balance']
    historical_data = data['historical_data']

    action = check_conditions(historical_data)

    current_log = {"time": historical_data[-1]['time']}

    if action:
        print(f'Executing {action} order')
        current_log['action'] = action
        price = place_order(action)
        if price:
            current_log["price"] = price
            print("Sucessfully ordered")
        else:
            current_log["price"] = "Order was failed"
            print("Order was failed")
        
    else:
        current_log["action"] = "No action to be taken"

    # insert the hiostry
    global ordering_history
    ordering_history.append(current_log)
    with open("ordering_history.json", "w") as f:
        json.dump(ordering_history, f)


def trading(granularity):
    data = fetch_data(granularity)
    currenttime = data['historical_data'][-1]['time']
    global last_ordered_time
    if last_ordered_time != currenttime:
        print(currenttime)
        last_ordered_time = currenttime
        ordering(data)

    data["ordering_history"] = ordering_history

    with open("history.json", "w") as f:
        json.dump(data, f)
    return data

while True:
    trading(granularity)
    time.sleep(10)


# print(fetch_data('BTC-USD', 300))