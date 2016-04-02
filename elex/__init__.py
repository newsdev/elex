import os
import pkg_resources
import tempfile


__version__ = pkg_resources.get_distribution('elex').version
API_VERSION = os.environ.get('AP_API_VERSION', 'v2')
BASE_URL = os.environ.get('AP_API_BASE_URL', 'http://api.ap.org/{0}'.format(API_VERSION))
API_KEY = os.environ.get('AP_API_KEY', None)
DEFAULT_TEMPDIR = os.path.join(tempfile.gettempdir(), 'elex-cache')
DELEGATE_REPORT_ID_CACHE_FILE = os.environ.get('ELEX_DELEGATE_REPORT_ID_CACHE_FILE', DEFAULT_TEMPDIR)
