from dateutil import parser
import requests

import elex


class BaseObject(object):
    """
    Base class for most objects.
    Handy container for methods for first level
    transformation of data and AP connections.
    """
    def set_dates(self, date_fields):
        for field in date_fields:
            try:
                setattr(self, field + '_parsed', parser.parse(getattr(self, field)))
            except AttributeError:
                pass

    def set_fields(self, **kwargs):
        fieldnames = self.__dict__.keys()
        for k,v in kwargs.items():
            k = k.lower().strip()
            try:
                v = unicode(v.decode('utf-8'))
            except AttributeError:
                pass
            if k in fieldnames:
                setattr(self, k, v)

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()

    @classmethod
    def get(cls, path, **params):
        return ap_request(path, **params)


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

    print elex.BASE_URL + path
    print params

    return requests.get(elex.BASE_URL + path, params=params).json()