import os
import pkg_resources
import requests
import tempfile

from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from elex.cachecontrol_heuristics import EtagOnlyCache

__version__ = pkg_resources.get_distribution('elex').version
_DEFAULT_CACHE_DIRECTORY = os.path.join(tempfile.gettempdir(), 'elex-cache')

API_KEY = os.environ.get('AP_API_KEY', None)
API_VERSION = os.environ.get('AP_API_VERSION', 'v2')
BASE_URL = os.environ.get('AP_API_BASE_URL', 'http://api.ap.org/{0}'.format(API_VERSION))
CACHE_DIRECTORY = os.environ.get('ELEX_CACHE_DIRECTORY', _DEFAULT_CACHE_DIRECTORY)

session = requests.session()
session.headers.update({'Accept-Encoding': 'gzip'})
cache = CacheControl(session,
                     cache=FileCache(CACHE_DIRECTORY),
                     heuristic=EtagOnlyCache())
