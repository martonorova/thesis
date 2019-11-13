from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
def test_datasource():
    return "HELLO"

if __name__ == '__main__':
    app.run('0.0.0.0', port=6000, debug=True)
