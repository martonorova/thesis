from flask import Flask, request
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
import requests
import mysql.connector
from mysql.connector import Error
import json

app = Flask(__name__)
CORS(app)

weather_api_host = 'http://weather-api:7000'

table = {
    'columns': [
        {'text': 'Month', 'type': 'string'},
        {'text': 'Close Maxs', 'type': 'number'},
        {'text': 'Close Mins', 'type': 'number'}
    ],
    'rows': [],
    'type': 'table'
}

@app.route('/')
def test_datasource():
    return "Test success"

@app.route('/search')
def search():
    pass

@app.route('/query')
def query():
    return "QUERY"
    

def get_all_time_records():
    response = requests.get(weather_api_host + '/all')

    json_data = json.loads(response.text)

    return json_data


def create_table_data():

    delta = 0.2

    all_time_records = get_all_time_records()
    new_data = read_data_from_db()

    for record in all_time_records:
        


# https://pynative.com/python-mysql-select-query-to-fetch-data/
def read_data_from_db():
    try:
        connection = mysql.connector.connect(
            host='mysql',
            database='weather',
            user='weatheruser',
            password='userpass'
        )

        sql_select_records_query = "SELECT * FROM newyork"
        cursor = connection.cursor()
        cursor.execute(sql_select_records_query)
        records = cursor.fetchall()

        # print(type(records))
        # print(records)

        data = []

        for row in records:
            record = {
                'date': row[0],
                'day_of_the_year': int(row[1]),
                'max_temp': float(row[2]),
                'min_temp': float(row[3])
            }
            data.append(record)
        
        # print(data)
        # print(type(data[0]['date']))
        # print(type(int(data[0]['day_of_the_year'])))
        # print(type(data[0]['max_temp']))
        # print(type(data[0]['min_temp']))

        return data

    except Error as error:
        print("Error reading data from MySQL ", error)
    finally:
        if (connection.is_connected()):
            connection.close()
            #cursor.close()
            print("MySQL connection closed")



if __name__ == '__main__':
    app.run('0.0.0.0', port=6000, debug=True)
