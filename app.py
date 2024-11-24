from flask import Flask, request
from flask_cors import CORS
from LogPoint import get_dpi
import json
app = Flask(__name__)
CORS(app)

@app.route("/api/LogPoint_ai", methods=['POST'])
def getdpi():
    data = request.get_json()
    a = data['a']
    b = data['b']
    r = data['r']

    # -- 더미 데이터 --
    # a = [(1, 5), (3, 2), (8, 7), (3, 4), (9, 10)]
    # b = [(3, 9), (2, 82), (63, 89), (67, 13), (9, 10)]
    # r = [(6, 7), (24, 5), (7, 7), (3, 8), (9, 10)]

    result = []
    for a_, b_, r_ in zip(a, b, r):
        v = get_dpi(a_, b_, r_)
        result.append(v.dpi_per)
    res = sum(result) / len(result)
    print(json.dumps(res))
    return json.dumps(res)
getdpi()


