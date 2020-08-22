from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

COVID_CASES_API = "https://coronavirus-19-api.herokuapp.com/countries/"

# 🛩 Helper function🇬🇭 to get a particular country😇


# def getFunction(dataList, country):
#     for item in dataList:
#         if item.country is country:
#             return item


class Filter():
    data_list = []
    result = []
    query = {
        "skip": None,
        "take": None
    }

    def __init__(self, data_list, query):
        self.result = data_list
        self.query = {**self.query, **query}

    def filter(self):
        # Doing SKip
        skip = self.query['skip']
        if skip is not None:
            self.result = self.data_list[skip:]

        # Doing Take
        take = self.query['take']
        if(take is not None) and (len(self.result) > take):
            self.result = self.result[0:take]

        return self.result



@app.route("/")
# Hello function
def home():
    query = {}
    # Check for take
    if "take" in request.args:
        query.update({"take": int(request.args["take"])})

    # Check for skip
    if "skip" in request.args:
        query.update({"skip": int(request.args["skip"])})

    # To make a request to get our cases data
    response = requests.get(COVID_CASES_API)
    # To convert incoming data into a list
    data = list(response.json())

    # Filtering the Data
    data_filter = Filter(data, query)
    data = data_filter.filter()

    # Returning the data after running the function
    return jsonify(data_filter.result)


# if __name__ == '__main__':
#     app.run(debug=True)
