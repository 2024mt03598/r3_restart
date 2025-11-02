from flask import Flask, request

from flask_cors import CORS, cross_origin

from prometheus_client import start_http_server, Summary, Counter, generate_latest, CONTENT_TYPE_LATEST

import os

import time


app = Flask(__name__)

cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'


# Prometheus metrics

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

REQUEST_COUNT = Counter('request_count', 'Total number of requests', ['method', 'endpoint'])


# Metrics endpoint

@app.route('/metrics')

def metrics():

    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


# Instrumented route

@app.get('/get_info')

@cross_origin()

@REQUEST_TIME.time()

def get_info():

    REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()


    app_title = os.getenv("APP_TITLE", "default: BITS k8s demo app")

    app_version = os.getenv("APP_VERSION", "default: 1.0")

    api_key = os.getenv("API_KEY", "default: rkjhrfviefve")


    return {

        "app_title": app_title,

        "app_version": app_version,

        "api_key": api_key

    }


if __name__ == '__main__':

    # Start Prometheus metrics server on a different port if needed

    # start_http_server(8001)  # Optional: expose metrics on a separate port

    app.run(host='0.0.0.0', port=8000)
