import datetime
import json
import os
import time

from pymongo import MongoClient
import requests

import elex

def write_recording(payload):
    """
    Presumes JSON at the moment.
    Would have to refactor if using XML or FTP.
    FACTOR FOR USE; REFACTOR FOR REUSE.
    """
    recorder = os.environ.get('ELEX_RECORDING', False)
    if recorder:
        timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
        if recorder == u"mongodb":
            import pymongo
            MONGODB_CLIENT = MongoClient(os.environ.get('ELEX_RECORDING_MONGO_URL', 'mongodb://localhost:27017/'))
            MONGODB_DATABASE = MONGODB_CLIENT[os.environ.get('ELEX_RECORDING_MONGO_DB', 'ap_elections_loader')]
            collection = MONGODB_DATABASE.elex_recording
            collection.insert({"time": timestamp, "data": payload})

        elif recorder == u"flat":
            recorder_directory = os.environ.get('ELEX_RECORDING_DIR', '/tmp')
            with open('%s/ap_elections_loader_recording-%s.json' % (recorder_directory, timestamp), 'w') as writefile:
                writefile.write(json.dumps(payload))

def api_request(path, **params):
    """
    Function wrapping Python-requests
    for making a request to the AP's
    elections API.

    A properly formatted request:
    * Modifies the BASE_URL with a path.
    * Contains an API_KEY.
    * Returns JSON.
    """
    if not params.get('apiKey', None):
        params['apiKey'] = elex.API_KEY

    params['format'] = 'json'

    payload = requests.get(elex.BASE_URL + path, params=params).json()
    write_recording(payload)

    return payload
