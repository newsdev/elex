import os
import pkg_resources


__version__ = pkg_resources.get_distribution('elex').version
VERSION = os.environ.get('AP_API_VERSION', 'v2')
BASE_URL = "%s/elections" % os.environ.get(
    'AP_API_BASE_URL',
    'http://api.ap.org/%s' % VERSION
)
API_KEY = os.environ.get('AP_API_KEY', None)
