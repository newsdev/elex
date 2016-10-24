=======
Caching
=======

Elex uses a simple file-based caching system based using `CacheControl <https://github.com/ionrock/cachecontrol>`_.

Each request to the AP Election API is cached. Each subsequent API request sends the etag. If the API returns a 304 not modified response, the cached version of the request is used.

Exit codes
==========

If the underlying API call is returned from the cache, Elex exits with exit code 64.

For example, the first time you run an Elex results command, the exit code will be ``0``.

.. code:: bash

    elex results '02-01-2016'
    echo $?
    0

The next time you run the command, the exit code will be ``64``.

.. code:: bash

    elex results '02-01-2016'
    echo $?
    64

Clearing the cache
==================

To clear the cache, run:

.. code:: bash

    elex clear-cache

If the cache is empty, the command will return with exit code ``65``. This is unlikely to be helpful to end users, but helps with automated testing.

Configuring the cache
=====================

To set the cache directory, set the ``ELEX_CACHE_DIRECTORY`` environment variable.

If ``ELEX_CACHE_DIRECTORY`` is not set, the default temp directory as determined by Python's tempfile module will be used.
