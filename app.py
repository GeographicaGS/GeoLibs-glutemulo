
from flask import Flask
from flask import request

app = Flask(__name__)

log = app.logger

VENUES = ['v1', 'v2']


def process_data(source, data):
    log.info(source, data)
    # if cfg.USE_REDIS_QUEUE:
    #     return queue_observations(cmxjson, source)
    # if cfg.USE_CELERY:
    #     return import_observations.delay(cmxjson, source)
    # import_observations(cmxjson, source)


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
