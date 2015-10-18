from dateutil import parser
import requests

import elections

def ap_request(path, **params):
    """
    A properly formatted request:
    * Modifies the BASE_URL with a path.
    * Contains an API_KEY.
    * Contains a format.
    """
    if not params.get('apiKey', None):
        params['apiKey'] = elections.API_KEY
    if not params.get('format', None):
        params['format'] = 'json'

    return requests.get(elections.BASE_URL + path, params=params)

class BaseObject(object):
    def set_dates(self, date_fields):
        for field in date_fields:
            setattr(self, field + '_parsed', parser.parse(getattr(self, field)))

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