import os
import pkg_resources
import requests
import tempfile

from cachecontrol import CacheControl
from cachecontrol.caches import FileCache

__version__ = pkg_resources.get_distribution('elex').version
API_VERSION = os.environ.get('AP_API_VERSION', 'v2')
BASE_URL = os.environ.get('AP_API_BASE_URL', 'http://api.ap.org/{0}'.format(API_VERSION))
API_KEY = os.environ.get('AP_API_KEY', None)
CACHE_DIRECTORY = os.path.join(tempfile.gettempdir(), 'elex-cache')
cache = CacheControl(requests.session(),
                     cache=FileCache(CACHE_DIRECTORY))
