*************
Configuration
*************

The following environment variables may be set:

::

    export API_VERSION='v2'
    export BASE_URL='http://api.ap.org/v2'
    export AP_API_KEY='<<YOURAPIKEY>>'
    export ELEX_RECORDING='flat'
    export ELEX_RECORDING_DIR='/tmp/elex-recording'
    export ELEX_CACHE_DIRECTORY='/tmp/elex-cache'

API_VERSION
===========

The AP API version. You should never need to change this.

BASE_URL
========

Use a different base url for API requests. Helpful if running a mirror or archive of raw AP data like `Elex Deja Vu <https://github.com/newsdev/ap-deja-vu>`_.

AP_API_KEY
==========

Your API key. Must be set.

ELEX_CACHE_DIRECTORY
====================

Path to the Elex cache directory. If not set, defaults to ``<tempdir>/elex-cache`` where ``<tempdir>`` is whatever Python's ``tempfile.gettempdir()`` returns.

ELEX_RECORDING, ELEX_RECORDING_DIR
==================================

Configure full data recording. See :doc:`recording`.
