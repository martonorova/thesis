from flask import Flask, request
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
import requests
import mysql.connector
from mysql.connector import Error
import json
from collections import OrderedDict
import time

app = Flask(__name__)
CORS(app)

weather_api_host = 'http://weather-api:7000'


@app.route('/')
def test_datasource():
    return "Test success"


@app.route('/search', methods=['POST'])
def search():
    return json.dumps(['weather-table'])


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


@app.route('/query', methods=['POST'])
def query():
    table_data = create_table_data()
    return json.dumps(table_data)


def get_all_time_records():
    response = requests.get(weather_api_host + '/all')

    json_data = json.loads(response.text)

    return json_data


def create_table_data():

    delta = 2

    table = {
        'columns': [
            {'text': 'Month', 'type': 'string'},
            {'text': 'Close Maxs', 'type': 'number'},
            {'text': 'Close Mins', 'type': 'number'}
        ],
        'rows': [],
        'type': 'table'
    }

    table_rows_dict = OrderedDict()

    all_time_records = get_all_time_records()
    new_data = read_data_from_db()

    for row in new_data:
        date = row['date']
        day_of_the_year = row['day_of_the_year']
        daily_max_temp = float(row['max_temp'])
        daily_min_temp = float(row['min_temp'])

        alltime_record = all_time_records[str(day_of_the_year)]
        alltime_max_temp = float(alltime_record['alltime_max'])
        alltime_min_temp = float(alltime_record['alltime_min'])

        monthname = date.strftime('%B')
        year = date.year
        key = f'{year} {monthname}'

        if key in table_rows_dict:
            # TODO maybe a function for this
            if daily_max_temp > alltime_max_temp - delta:
                table_rows_dict[key][1] += 1
            if daily_min_temp < alltime_min_temp + delta:
                table_rows_dict[key][2] += 1
        else:
            table_row = [key, 0, 0]
            if daily_max_temp > alltime_max_temp + delta:
                table_row[1] = 1
            if daily_min_temp < alltime_min_temp + delta:
                table_row[2] = 1
            table_rows_dict[key] = table_row

    for row_key in table_rows_dict:
        table['rows'].append(table_rows_dict[row_key])

    # need the list because of JSON datasource format
    return [table]


# https://pynative.com/python-mysql-select-query-to-fetch-data/
def read_data_from_db():
    try:
        connection = mysql.connector.connect(
            host='mysql',
            database='weather',
            user='weatheruser',
            password='userpass',
            auth_plugin='mysql_native_password'
        )

        sql_select_records_query = "SELECT * FROM newyork"
        cursor = connection.cursor()
        cursor.execute(sql_select_records_query)
        records = cursor.fetchall()

        data = []

        for row in records:
            record = {
                'date': row[0],
                'day_of_the_year': int(row[1]),
                'max_temp': float(row[2]),
                'min_temp': float(row[3])
            }
            data.append(record)

        return data

    except Error as error:
        print("Error reading data from MySQL ", error)
    finally:
        if (connection.is_connected()):
            connection.close()
            print("MySQL connection closed")


if __name__ == '__main__':
    app.run('0.0.0.0', port=6000, debug=True)
