=======
Recipes
=======

Useful Elex patterns. :doc:`Contribute your own <contributing>`.

All examples specify a data file instead of a live or test election date
so that all examples can be followed even if you don't have an AP API key.
For real election data, replace ``-d FILENAME`` in these examples with an
election date.

Get results at a specific level
===============================

Get only state level results:

.. code:: bash

    elex results --results-level state -d "${VIRTUAL_ENV}/src/elex/tests/data/20160301_super_tuesday.json"

.. csv-table::

    id,raceid,racetype,racetypeid,ballotorder,candidateid,description,delegatecount,electiondate,fipscode,first,incumbent,initialization_data,is_ballot_measure,last,lastupdated,level,national,officeid,officename,party,polid,polnum,precinctsreporting,precinctsreportingpct,precinctstotal,reportingunitid,reportingunitname,runoff,seatname,seatnum,statename,statepostal,test,uncontested,votecount,votepct,winner
    24547-polid-8639-state-1,24547,Primary,R,2,33360,,0,2016-03-01,,Donald,False,False,False,Trump,2016-03-02T20:35:54Z,state,True,P,President,GOP,8639,27533,2172,0.9995,2173,state-1,,False,,,Massachusetts,MA,False,False,311313,0.493056,True
    24547-polid-36679-state-1,24547,Primary,R,13,33366,,0,2016-03-01,,John,False,False,False,Kasich,2016-03-02T20:35:54Z,state,True,P,President,GOP,36679,27528,2172,0.9995,2173,state-1,,False,,,Massachusetts,MA,False,False,113783,0.180209,False
    ...

To cut down on load and bandwidth use and speed up loading when you are
repeatedly loading results, specify only the level(s) you need to display.


Add timestamp or batch name column to any data command
======================================================

You can add a timestamp column to track results (or any other
data output by elex) with the ``--with-timestamp`` flag).

.. code:: bash

    elex elections --with-timestamp -d "${VIRTUAL_ENV}/elex-dev/src/elex/tests/data/00000000_elections.json"

.. csv-table::

    id,electiondate,liveresults,testresults,timestamp
    2012-03-13,2012-03-13,True,False,1460438301
    2012-11-06,2012-11-06,True,False,1460438301
    ...


If you prefer, you can set a batch name. This is useful when
executing multiple commands that need a single grouping column.

.. code:: bash

    elex elections --batch-name batch-031 -d "${VIRTUAL_ENV}/elex-dev/src/elex/tests/data/00000000_elections.json"

.. csv-table::

    id,electiondate,liveresults,testresults,timestamp
    2016-02-23,2016-02-23,True,False,batch-031
    2016-02-27,2016-02-27,True,False,batch-031
    ...


Get local election results
===============================

Get only local races:

.. code:: bash

    elex races 03-15-16 --local-only -d "${VIRTUAL_ENV}/src/elex/tests/data/20160301_super_tuesday.json"

.. csv-table::

    id,raceid,racetype,racetypeid,description,electiondate,initialization_data,is_ballot_measure,lastupdated,national,officeid,officename,party,seatname,seatnum,statename,statepostal,test,uncontested
    14897,14897,Primary,R,,2016-03-15,True,False,2016-03-18T12:29:42Z,True,0,State's Attorney,GOP,Cook County,,,IL,False,True
    15329,15329,Primary,D,,2016-03-15,True,False,2016-03-18T12:29:42Z,True,0,Recorder of Deeds,Dem,Cook County,,,IL,False,True
    ...

Get only local results:

.. code:: bash

    elex results --local-only


Get AP zero count data
======================

AP's set zero count parameter is a special server feature that only makes sense to
query live.

.. code:: bash

    elex results 03-15-16 --set-zero-counts

.. csv-table::

    id,raceid,racetype,racetypeid,ballotorder,candidateid,description,delegatecount,electiondate,fipscode,first,incumbent,initialization_data,is_ballot_measure,last,lastupdated,level,national,officeid,officename,party,polid,polnum,precinctsreporting,precinctsreportingpct,precinctstotal,reportingunitid,reportingunitname,runoff,seatname,seatnum,statename,statepostal,test,uncontested,votecount,votepct,winner
    10673-polid-8639-state-1,10673,Primary,R,13,20428,,0,2016-03-15,,Donald,False,False,False,Trump,2016-03-16T21:05:09Z,state,True,P,President,GOP,8639,14574,0,0.0,5810,state-1,,False,,,Florida,FL,False,False,0,0.0,False
    ...

Auto-generate SQL schemas with csvkit
=====================================

Install `csvkit <http://csvkit.readthedocs.org/>`_, a handy tool for working with CSVs.

Now build the results schema by using the ``candidate-reporting-units`` command.

.. code:: bash

    elex candidate-reporting-units -d "${VIRTUAL_ENV}/src/elex/tests/data/20160301_super_tuesday.json" | csvsql --tables results -i sqlite

.. code:: bash

    2016-04-14 00:51:07,675 (INFO) elex (v2.0.0) : Getting candidate reporting units for election 2016-03-26
    CREATE TABLE results (
      id VARCHAR(23) NOT NULL,
      raceid INTEGER NOT NULL,
      racetype VARCHAR(6) NOT NULL,
      racetypeid VARCHAR(1) NOT NULL,
      ballotorder INTEGER NOT NULL,
      candidateid INTEGER NOT NULL,
      description VARCHAR(32),
      delegatecount INTEGER NOT NULL,
      electiondate DATE NOT NULL,
      fipscode VARCHAR(32),
      first VARCHAR(7),
      incumbent BOOLEAN NOT NULL,
      initialization_data BOOLEAN NOT NULL,
      is_ballot_measure BOOLEAN NOT NULL,
      last VARCHAR(12) NOT NULL,
      lastupdated DATETIME NOT NULL,
      level VARCHAR(32),
      national BOOLEAN NOT NULL,
      officeid VARCHAR(1) NOT NULL,
      officename VARCHAR(9) NOT NULL,
      party VARCHAR(3) NOT NULL,
      polid INTEGER NOT NULL,
      polnum INTEGER NOT NULL,
      precinctsreporting INTEGER NOT NULL,
      precinctsreportingpct FLOAT NOT NULL,
      precinctstotal INTEGER NOT NULL,
      reportingunitid VARCHAR(32),
      reportingunitname VARCHAR(32),
      runoff BOOLEAN NOT NULL,
      seatname VARCHAR(32),
      seatnum VARCHAR(32),
      statename VARCHAR(10) NOT NULL,
      statepostal VARCHAR(2) NOT NULL,
      test BOOLEAN NOT NULL,
      uncontested BOOLEAN NOT NULL,
      votecount INTEGER NOT NULL,
      votepct FLOAT NOT NULL,
      winner BOOLEAN NOT NULL,
      CHECK (incumbent IN (0, 1)),
      CHECK (initialization_data IN (0, 1)),
      CHECK (is_ballot_measure IN (0, 1)),
      CHECK (national IN (0, 1)),
      CHECK (runoff IN (0, 1)),
      CHECK (test IN (0, 1)),
      CHECK (uncontested IN (0, 1)),
      CHECK (winner IN (0, 1))
    );

Insert results with csvkit + sqlite
===================================

This is not a wildly efficient way to get results into a database, but it is lightweight.

.. code:: bash

    elex candidate-reporting-units -d "${VIRTUAL_ENV}/src/elex/tests/data/20160301_super_tuesday.json" | csvsql --tables results --db sqlite:///db.sqlite --insert


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
