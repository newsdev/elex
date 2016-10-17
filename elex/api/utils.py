"""
Utility functions to record raw election results and handle low-level HTTP
interaction with the Associated Press Election API.
"""
from __future__ import print_function
import os
import sys
import six
import elex
import ujson as json
import time
import datetime
from elex import cache
from elex.exceptions import APAPIKeyException
from pymongo import MongoClient


class UnicodeMixin(object):
    """
    Python 2 + 3 compatibility for __unicode__
    """
    if sys.version_info > (3, 0):
        __str__ = lambda x: x.__unicode__()
    else:
        __str__ = lambda x: six.text_type(x).encode('utf-8')

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.__str__())


def write_recording(payload):
    """
    Record a timestamped version of an Associated Press Elections API
    data download.

    Presumes JSON at the moment.
    Would have to refactor if using XML or FTP.
    FACTOR FOR USE; REFACTOR FOR REUSE.

    :param payload:
        JSON payload from Associated Press Elections API.
    """
    recorder = os.environ.get('ELEX_RECORDING', False)
    if recorder:
        timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
        if recorder == u"mongodb":
            MONGODB_CLIENT = MongoClient(
                os.environ.get(
                    'ELEX_RECORDING_MONGO_URL',
                    'mongodb://localhost:27017/'
                )
            )
            MONGODB_DATABASE = MONGODB_CLIENT[
                os.environ.get(
                    'ELEX_RECORDING_MONGO_DB',
                    'ap_elections_loader'
                )
            ]
            collection = MONGODB_DATABASE.elex_recording
            collection.insert({"time": timestamp, "data": payload})
        elif recorder == u"flat":
            recorder_directory = os.environ.get('ELEX_RECORDING_DIR', '/tmp')
            json_path = '%s/ap_elections_loader_recording-%s.json' % (
                recorder_directory,
                timestamp
            )
            with open(json_path, 'w') as writefile:
                writefile.write(json.dumps(payload))


def api_request(path, **params):
    """
    Function wrapping Python-requests
    for making a request to the AP's
    elections API.

    A properly formatted request:
    * Modifies the BASE_URL with a path.
    * Contains an API_KEY.
    * Returns a response object.

    :param **params:
        Extra parameters to pass to `requests`. For example,
        `apiKey="<YOUR API KEY>`, your AP API key, or `national=True`,
        for national-only results.
    """
    if not params.get('apiKey', None):
        if elex.API_KEY != '':
            params['apiKey'] = elex.API_KEY
        else:
            params['apiKey'] = None

    if not params['apiKey']:
        raise APAPIKeyException()

    params['format'] = 'json'

    params = sorted(params.items())  # Sort for consistent caching

    url = '{0}{1}'.format(elex.BASE_URL, path)

    response = cache.get(url, params=params)
    response.raise_for_status()

    write_recording(response.json())

    return response


def get_reports(params={}):
    """
    Get data from `reports` endpoints.
    """
    resp = api_request('/reports', **params)
    if resp.ok:
        return resp.json().get('reports')
    else:
        return []
