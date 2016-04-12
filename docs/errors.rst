=================
Output and errors
=================

---------------
Output handling
---------------

In the command line interface, all data is written to stdout. All messages are
written to stderr.

.. code:: bash

    # Direct data to a file and print messages to console
    elex results 2016-02-01 > data.csv

    # Direct messages to a file and print data to console
    elex results 2016-02-01 2> messages.csv

    # Direct messages and data to individual files
    elex results 2016-02-01 > data.csv 2> elex-log.txt

URLs (which typically contain the API key as a parameter), are only output when
the ``--debug`` flag is specified.

----------
Exit codes
----------

In the command line interface, common errors are caught, logged, and the
`elex` command exits with exit code 1.

If the `elex` command is successful, it closes with exit code 0.

Unknown / unexpected errors will continue to raise the normal Python exceptions.

-------------
Common errors
-------------

~~~~~~~~~~~~~~~
ConnectionError
~~~~~~~~~~~~~~~

.. code:: bash

    2016-04-12 10:47:59,928 (ERROR) elex (v2.0.0) : Connection error (<requests.packages.urllib3.connection.HTTPConnection object at 0x108525588>: Failed to establish a new connection: [Errno 8] nodename nor servname provided, or not known)

This happens when the elex client cannot connect to the API. Make sure the
``AP_API_BASE_URL`` environment variable is correct and that you have network
connectivity.

~~~~~~~~~~~~~~~~~~~~~~~~~~
HTTP Error 401 - Forbidden
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    2016-04-12 14:37:37,470 (ERROR) elex (v2.0.0) : HTTP Error 401 - Forbidden (Invalid API key.)

These errors represent an authentication error. Typically, this is a problem with
your AP API key. Make sure the ``AP_API_KEY`` environment variable is set correctly.
If the problem persists, contact AP customer support.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HTTP Error 403 - Over Quota Limit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    2016-04-12 10:24:01,904 (ERROR) elex (v2.0.0) : HTTP Error 403 - Over quota limit.

This means it is time to cool it and make less requests. Most AP clients have a
quota of 10 requests a second.

~~~~~~~~~~~~~~~~~~~~~~~~~~
HTTP Error 404 - Not found
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    2016-04-12 14:19:41,279 (ERROR) elex (v2.0.0) : HTTP Error 404 - Not Found.

This means the network connection was fine but the endpoint URL does not exist.
Check ``AP_API_BASE_URL`` to make sure the URL is correct.


