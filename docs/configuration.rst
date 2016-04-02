*************
Configuration
*************

The following environment variables may be set:

::

    export API_VERSION='v2'
    export BASE_URL='http://api.ap.org/v2'
    export API_KEY='<<YOURAPIKEY>>'
    export ELEX_DELEGATE_REPORT_ID_CACHE_FILE='/tmp/elex-cache'
    export ELEX_RECORDING='flat'
    export ELEX_RECORDING_DIR='/tmp/elex-recording'

API_VERSION
===========

The AP API version. You should never need to change this.

BASE_URL
========

Use a different base url for API requests. Helpful if running a mirror or archive of raw AP data like `Elex Deja Vu <https://github.com/newsdev/ap-deja-vu>`_.

API_KEY
=======

Your API key. Must be set.


ELEX_DELEGATE_REPORT_ID_CACHE_FILE
==================================

To cut down on requests for a rarely changing ID, Elex caches this ID in a file stored in a temporary directory. You can override the default temporary directory (which is found in an OS-agnostic way with the Python tempfile library) by specifying this environment variable. You shouldn't need to set this in most cases.

ELEX_RECORDING, ELEX_RECORDING_DIR
==================================

Configure full data recording. See :doc:`recording`.
