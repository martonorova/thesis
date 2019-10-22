from flask import Flask, request
import requests
from getpass import getpass
import json
import time
import logging

app = Flask(__name__)

server_host = 'http://rapidminer-server:8080'

@app.route('/')
def hello_world():

    response = requests.get(server_host)
    if response.status_code == 200:
        return 'Hello World'
    return "Sad"


@app.route('/query', methods=['POST'])
def query():

    print("Query Data")
    print(request.data)

    # WARNING this only extracts the first target, it disregards the others, if provided
    target = request.json['targets'][0]['target']

    response = requests.get(server_host + '/api/rest/process/{}'.format(target),
                       auth=('admin', 'changeit'))

    json_data = json.loads(response.text)
    
    # print("JSON DATA: {}".format(json_data))

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

    result = [
        {
            "columns": columns,
            "rows": rows,
            "type": 'table'
        }
    ]

    print('Result:')
    print(json.dumps(result))
    return json.dumps(result)

@app.route('/search', methods=['POST'])
def search():

    response = requests.get(server_host + '/api/rest/service/list',
                       auth=('admin', 'changeit'))

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
        # TODO refactor this, duplicate of /search endpoint
        response = requests.get(server_host + '/api/rest/service/list',
                       auth=('admin', 'changeit'))

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

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)