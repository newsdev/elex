=======
Recipes
=======

Useful Elex patterns. :doc:`Contribute your own <contributing>`.

Get test data
=============

.. code:: bash

    elex results -t 2016-03-15

Get data from existing data file
================================

.. code:: bash

    elex results -d /path/to/file.json

Get results at a specific level
===============================

Get only state level results:

.. code:: bash

    elex results 03-15-16 --results-level state

.. csv-table::

    id,unique_id,raceid,racetype,racetypeid,ballotorder,candidateid,description,delegatecount,electiondate,fipscode,first,incumbent,initialization_data,is_ballot_measure,last,lastupdated,level,national,officeid,officename,party,polid,polnum,precinctsreporting,precinctsreportingpct,precinctstotal,reportingunitid,reportingunitname,runoff,seatname,seatnum,statename,statepostal,test,uncontested,votecount,votepct,winner
    10673-polid-8639-state-1,polid-8639,10673,Primary,R,13,20428,,0,2016-03-15,,Donald,False,False,False,Trump,2016-03-16T21:05:09Z,state,True,P,President,GOP,8639,14574,5810,1.0,5810,state-1,,False,,,Florida,FL,False,False,1077221,0.457383,True
    10673-polid-53044-state-1,polid-53044,10673,Primary,R,11,20425,,0,2016-03-15,,Marco,False,False,False,Rubio,2016-03-16T21:05:09Z,state,True,P,President,GOP,53044,12082,5810,1.0,5810,state-1,,False,,,Florida,FL,False,False,636653,0.27032,False


To cut down on load and bandwidth use and speed up loading when you are
repeatedly loading results, specify only the level(s) you need to display.


Add timestamp or batch name column to any data command
======================================================

You can add a timestamp column to track results (or any other
data output by elex) with the ``--with-timestamp`` flag).

.. code:: bash

    elex elections --with-timestamp

.. csv-table::

    id,electiondate,liveresults,testresults,timestamp
    2012-03-13,2012-03-13,True,False,1460438301
    2012-11-06,2012-11-06,True,False,1460438301
    ...


If you prefer, you can set a batch name. This is useful when
executing multiple commands that need a single grouping column.

.. code:: bash

    elex elections --batch-name batch-031

.. csv-table::

    id,electiondate,liveresults,testresults,timestamp
    2016-02-23,2016-02-23,True,False,batch-031
    2016-02-27,2016-02-27,True,False,batch-031
    ...


Get only local data
===================

Get only local races:

.. code:: bash

    elex races 03-15-16 --local-only

..csv-table::

    id,raceid,racetype,racetypeid,description,electiondate,initialization_data,is_ballot_measure,lastupdated,national,officeid,officename,party,seatname,seatnum,statename,statepostal,test,uncontested
    14897,14897,Primary,R,,2016-03-15,True,False,2016-03-18T12:29:42Z,True,0,State's Attorney,GOP,Cook County,,,IL,False,True
    15329,15329,Primary,D,,2016-03-15,True,False,2016-03-18T12:29:42Z,True,0,Recorder of Deeds,Dem,Cook County,,,IL,False,True

Get only local results:

.. code:: bash

    elex races 03-15-16 --local-only

Get AP zero count data
======================

.. code:: bash

    elex results 03-15-16 --set-zero-counts

.. csv-table::

    id,unique_id,raceid,racetype,racetypeid,ballotorder,candidateid,description,delegatecount,electiondate,fipscode,first,incumbent,initialization_data,is_ballot_measure,last,lastupdated,level,national,officeid,officename,party,polid,polnum,precinctsreporting,precinctsreportingpct,precinctstotal,reportingunitid,reportingunitname,runoff,seatname,seatnum,statename,statepostal,test,uncontested,votecount,votepct,winner
    10673-polid-8639-state-1,polid-8639,10673,Primary,R,13,20428,,0,2016-03-15,,Donald,False,False,False,Trump,2016-03-16T21:05:09Z,state,True,P,President,GOP,8639,14574,0,0.0,5810,state-1,,False,,,Florida,FL,False,False,0,0.0,False
    10673-polid-53044-state-1,polid-53044,10673,Primary,R,11,20425,,0,2016-03-15,,Marco,False,False,False,Rubio,2016-03-16T21:05:09Z,state,True,P,President,GOP,53044,12082,0,0.0,5810,state-1,,False,,,Florida,FL,False,False,0,0.0,False

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
