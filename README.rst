.. figure:: https://cloud.githubusercontent.com/assets/109988/10737959/635bfb56-7beb-11e5-9ee5-102eb1582718.png
   :alt: 

Usage
-----

Demo app
~~~~~~~~

.. code:: bash

    python -m elex.demo

Modules
~~~~~~~

Use the election loader manually from within your project.

Elections
^^^^^^^^^

.. code:: python

    from elex.parser import api

    # Show all elections available.
    # Note: Some elections may be in the past.
    elections = api.Election.get_elections()

    # Get the next election.
    election = api.Election.get_next_election()

Races, Candidates and results
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from elex.parser import api

    candidates = []
    reportingunits = []
    races = []

    for race in api.Election.get_races('2015-10-24', omitResults=False, level="ru"):
        races.append(race)
        for reporting_unit in race.reportingunits:
            reportingunits.append(reporting_unit)
            candidates += [c for c in reporting_unit.candidates]

    print "Parsed %s candidates." % len(candidates)
    print "Parsed %s reporting units." % len(reportingunits)
    print "Parsed %s races." % len(races)

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
