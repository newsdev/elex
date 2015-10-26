import requests

import elex

def ap_request(path, **params):
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

    return requests.get(elex.BASE_URL + path, params=params).json()