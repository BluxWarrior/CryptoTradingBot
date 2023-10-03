from flask import Flask, request
from flask_cors import CORS

from fetch_data import fetch_data
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    print(3)
    return 'Hello, World!'

# Fetch Data
@app.route('/api/fetchdata', methods=['Post'])
def data_get():
    # Here key is the URL parameter you want to fetch
    # print(request)
    data = request.get_json()
    granularity = data['granularity']
    # print(granularity)
    historicaldata = fetch_data(granularity)
    # print(historicaldata)
    return historicaldata

# POST Request
@app.route('/post', methods=['POST'])
def data_post():
    if not request.json:
        return "Missing JSON in Request"
        
    # Assumes, you're sending JSON with key-value pair { "key" : "value"}
    data = request.json['key']
    return 'Received value for the key is: ' + data

if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)
