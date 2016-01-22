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
