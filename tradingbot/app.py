from flask import Flask, request
from flask_cors import CORS

from utils import post_api
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    print(3)
    return 'Hello, World!'

### Fetch Data
@app.route('/api/post', methods=['Post'])
def data_post():
    # Here key is the URL parameter you want to fetch
    # print(request)
    data = request.get_json()
    granularity = data['granularity']
    # print(granularity)
    historicaldata = post_api(granularity)
    # print(historicaldata)
    return historicaldata



if __name__ == '__main__':
    app.debug = True
    app.run(port=5000, host='0.0.0.0')
