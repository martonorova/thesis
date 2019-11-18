from flask import Flask, request
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

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


def create_table_data():
    pass

def read_data_from_db():
    pass



if __name__ == '__main__':
    app.run('0.0.0.0', port=6000, debug=True)
