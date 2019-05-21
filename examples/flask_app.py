
from flask import Flask
from flask import request

from glutemulo.kafka.producer import JsonKafka


app = Flask(__name__)

log = app.logger

VENUES = ['v1', 'v2']


def process_data(source, data):
    log.info(source, data)
    productor = JsonKafka(bootstrap_servers="localhost:9092")
    productor.produce(source, data)


@app.route('/<venue>/', methods=['POST'])
def endpoint(venue):
    if not request.json:
        return ("invalid data", 400)
    if venue not in VENUES:
        log.warn(f'Source "{venue}" not found in preset VENUES')
    try:
        process_data(venue, request.json)
        return "DATA Received", 201
    except Exception as err:
        # log.exception(err)
        return str(err), 500
