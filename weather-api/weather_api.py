from flask_api import FlaskAPI, status, exceptions
from flask import request
import csv

app = FlaskAPI(__name__)
data = dict()


@app.route('/example/')
def example():
    return {'hello': 'world'}

@app.route('/all')
def get_all():
    return data

@app.route('/single/<day_of_the_year>')
def get_single(day_of_the_year):
    try:
        return data[day_of_the_year]
    except KeyError:
        raise exceptions.NotFound()

def read_data():

    data = dict()

    with open('/weather-data/data.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                # continue
            key = row["day_of_the_year"]
            data[key] = dict(row)
            line_count += 1
    return data
        

if __name__ == "__main__":
    data = read_data()
    app.run('0.0.0.0', port='7000', debug=True)