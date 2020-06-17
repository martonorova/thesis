from flask import Flask, request
import requests
from getpass import getpass
import json
import time
import logging
import re
import os

app = Flask(__name__)

server_host = f"{os.environ['RAPIDMINER_SERVER_PROTOCOL']}://{os.environ['RAPIDMINER_SERVER_HOST']}:{os.environ['RAPIDMINER_SERVER_PORT']}"


@app.route('/')
def check_connection():
    response = requests.get(server_host)
    if response.status_code == 200:
        return 'Server connection OK'
    return "Server connection error"


@app.route('/query', methods=['POST'])
def query():

    request_json = request.json
    result = []

    print("---------------- REGUEST ---------------")
    print(request_json)

    # Check what the selected metric type is ('timeserie' or 'table') for each target in the request query
    for target in request_json['targets']:
        target_type = target['type']
        target_name = target['target']
        # response from the RM Webservice containing the values for the given target
        response = requests.get(server_host + '/api/rest/process/{}'.format(target_name),
                                    auth=(request.authorization.username, request.authorization.password))
        json_data = json.loads(response.text)

        print("JSON DATA --------------------")
        print(json_data)

        if target_type == 'timeserie':
            target_result = convert_to_series(json_data, target_name)
            result.append(target_result)

        elif target_type == 'table':
            target_result = convert_to_table(json_data)
            result.append(target_result)

        else:
            raise ValueError('Unknown target type: {}'.format(target_type))

    print("RESULT -------------------------------")
    print(json.dumps(result))
    return json.dumps(result)


@app.route('/search', methods=['POST'])
def search():

    response = requests.get(server_host + '/api/rest/service/list',
                            auth=(request.authorization.username, request.authorization.password))

    webservices_json_list = json.loads(response.text)

    webservice_names = []

    for webservice in webservices_json_list:
        webservice_names.append(webservice['name'])

    return json.dumps(webservice_names)


@app.route('/annotations', methods=['POST'])
def annotations():
    return json.dumps(
        [
            {
                "annotation": 'test annotation',
                "time": int(time.time() * 1000),
                "title": 'test title'
            }
        ]
    )

# returns the parameters for a given webservice
@app.route('/parameters', methods=['GET'])
def parameters():
    if request.args:
        args = request.args
        webserviceName = args.get('webserviceName')
        if webserviceName == None:
            raise ValueError('No value provided for "webserviceName"')

        # get the list of webservices and get the parameters of the one with the name provided in the query
        response = requests.get(server_host + '/api/rest/service/list',
                                auth=(request.authorization.username, request.authorization.password))

        webservices_json_list = json.loads(response.text)

        webservice_params = []

        for webservice in webservices_json_list:
            if webservice['name'] == webserviceName:
                webservice_params = webservice['parameters']
                break

        return json.dumps(webservice_params)

    return 'Please provide a query parameter in the URL'


def get_type(value):
    if type(value) == int or type(value) == float:
        return 'number'
    else:
        return 'string'

# converts data from RM wevservice (a single target) to table format
def convert_to_table(json_data):
    columns = []
    rows = []

    # this is good for many rows
    if type(json_data) == list:
        for column in json_data[0]:
            column_obj = {
                "text": column,
                "type": get_type(json_data[0][column])
            }
            columns.append(column_obj)

        for row in json_data:
            new_row = []
            for column in columns:
                new_row.append(row[column['text']])
            rows.append(new_row)
    # this is good for only one row from the webservice
    elif type(json_data) == dict:
        row = []
        for field in json_data:
            column_obj = {
                "text": field,
                "type": get_type(json_data[field])
            }
            columns.append(column_obj)
            row.append(json_data[field])

        rows.append(row)

    result = {
        "columns": columns,
        "rows": rows,
        "type": 'table'
    }

    return result

def convert_to_series(json_data, target_name):
    datapoints = []

    # this is good for many rows
    if type(json_data) == list:
        r = re.compile("^((?!timestamp).)*$")
        value_name = list(filter(r.match, list(json_data[0].keys())))[0]
        for row in json_data:
            datapoints.append([
                row[value_name],
                row['timestamp']
            ])

    else:
        raise ValueError("Provided timeseries is not a list!")


    result = {
        "target": target_name,
        "datapoints": datapoints
    }
    return result

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
