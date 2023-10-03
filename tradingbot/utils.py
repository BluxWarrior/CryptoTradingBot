import json

def post_api(granularity):
    # data = fetch_data(granularity)
    # currenttime = data['historical_data'][-1]['time']
    # global last_ordered_time
    # if last_ordered_time != currenttime:
    #     print(currenttime)
    #     last_ordered_time = currenttime
    #     ordering(data)

    # data["ordering_history"] = ordering_history
    with open("history.json", "r") as f:
        data = json.load(f)
    return data

# print(fetch_data('BTC-USD', 300))