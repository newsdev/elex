.. figure:: https://cloud.githubusercontent.com/assets/109988/10737959/635bfb56-7beb-11e5-9ee5-102eb1582718.png
   :alt: 

Requirements
------------

-  Python 2.7
-  pip

Optional requirements:
~~~~~~~~~~~~~~~~~~~~~~

-  PostgreSQL
-  MongoDB

Installation
------------

Install the Python library:

.. code:: bash

    pip install nyt-ap-elections

Set your AP API key:

.. code:: bash

    export AP_API_KEY=<MY_AP_API_KEY>

Additional configuration for demo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure you are running PostgreSQL. Then create your db and user:

.. code:: bash

    createdb elex
    createuser elex

Usage
-----

Demo app
~~~~~~~~

.. code:: bash

    python -m elex.demo

Modules
~~~~~~~

Use the election loader manually from within your project.

.. code:: python

    from elex.parser import api
    from elex import loader
    from elex.loader import postgres

    e = api.Election(electiondate='2015-11-03', testresults=False, liveresults=True, is_test=False)
    raw_races = e.get_races(omitResults=False, level="ru", test=False)

    races, reporting_units, candidate_reporting_units = e.get_units(raw_races)
    candidates, ballot_positions = e.get_uniques(candidate_reporting_units)

    DB_MAPPING = [
        (postgres.Candidate, candidates),
        (postgres.BallotPosition, ballot_positions),
        (postgres.CandidateReportingUnit, candidate_reporting_units),
        (postgres.ReportingUnit, reporting_units),
        (postgres.Race, races)
    ]

    loader.ELEX_PG_CONNEX.connect()
    loader.ELEX_PG_CONNEX.drop_tables([mapping[0] for mapping in DB_MAPPING], safe=True)
    loader.ELEX_PG_CONNEX.create_tables([mapping[0] for mapping in DB_MAPPING], safe=True)

    for obj, obj_list in DB_MAPPING:
        with loader.ELEX_PG_CONNEX.atomic():
            for idx in range(0, len(obj_list), 2000):
                obj.insert_many([o.__dict__ for o in obj_list[idx:idx+2000]]).execute()

    loader.ELEX_PG_CONNEX.close()

Options
-------

Recording
~~~~~~~~~

Flat files
^^^^^^^^^^

Will record timestamped and namespaced files to the
``ELEX_RECORDING_DIR`` before parsing.

.. code:: bash

    export ELEX_RECORDING=flat
    export ELEX_RECORDING_DIR=/tmp

MongoDB
^^^^^^^

Will record a timestamped record to MongoDB, connecting via
``ELEX_RECORDING_MONGO_URL`` and writing to the
``ELEX_RECORDING_MONGO_DB`` database.

.. code:: bash

    export ELEX_RECORDING=mongodb
    export ELEX_RECORDING_MONGO_URL=mongodb://localhost:27017/  # Or your own connection string.
    export ELEX_RECORDING_MONGO_DB=ap_elections_loader

Development
-----------

Run tests
~~~~~~~~~

.. code:: bash

    nosetests
