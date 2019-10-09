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

    logging.warning(str(request.json))

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
    return json.dumps(result)

@app.route('/search', methods=['POST'])
def search():
    #TODO query web services dynamically
    return json.dumps(['Predictive_Maintenance_web_service_without_parameters'])

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


def get_type(value):
    if type(value) == int or type(value) == float:
        return 'number'
    else:
        return 'string'

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)