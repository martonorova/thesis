from flask_api import FlaskAPI, status
from flask import request
import csv

app = FlaskAPI(__name__)


@app.route('/example/')
def example():
    return {'hello': 'world'}


def read_data():

    data = []

    with open('/weather-data/data.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            data.append(row)
            line_count += 1
    return data


def get_historical_max_temps_by_day():
    max_temps = dict()
    data = read_data()
    for record in data:
        

if __name__ == "__main__":
    app.run('0.0.0.0', port='7000', debug=True)
