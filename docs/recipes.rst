=======
Recipes
=======

Useful Elex patterns. :doc:`Contribute your own <contributing>`.

Filter with jq and upload to S3
===============================

This recipe uses the jq json filtering tool to create a national results json data file with a limited set of data fields and the AWS cli tools to upload the filtered json to S3.

Requirements:

* `Amazon web services account <http://docs.aws.amazon.com/gettingstarted/latest/swh/website-hosting-intro.html>`_
* `jq <https://stedolan.github.io/jq/>`_
* `AWS cli tools <http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html>`_

.. literalinclude:: example_scripts/jq-s3.sh
   :language: bash
   :emphasize-lines: 7-28
   :linenos:

:code:`ELEX_S3_URL` **must** be set to your s3 bucket and path.

Steps:

* Get election results in json format with :code:`elex`
* Pipe results to :code:`jq` for filtering
* Pipe filtered results to :code:`gzip` to compress
* Pipe gzipped results to :code:`aws s3 cp` to send to S3.

Inspect with an ORM using Flask and Peewee
===========================================

This recipe uses the Flask web framework and the Peewee Python ORM to model, query and update data that :code:`elex` provides.

Requirements:

* `Elex loader <https://github.com/newsdev/elex-loader>`_, an NYT project that calls :code:`elex` to load data into a Postgres database with CSV and the Postgres :code:`COPY` command.
* `Elex admin <https://github.com/newsdev/elex-admin>`_, an NYT project that is a simple, web-based admin for creating and editing data to override AP election results, including candidate names, race descriptions, and race calls.

Steps:

* Install :code:`elex-loader` using `these instructions <https://github.com/newsdev/elex-loader/blob/master/README.md>`_.
* Install :code:`elex-admin` using `these instructions <https://github.com/newsdev/elex-admin/blob/master/README.md>`_.

Extra steps:

* Use the :code:`models.py` that come with :code:`elex-admin` to query data.