.. figure:: https://cloud.githubusercontent.com/assets/109988/10567244/25ec282e-75cc-11e5-9d9a-fdeba61828a6.png
   :alt: 

Usage
-----

Demo app
~~~~~~~~

::

    python -m elex.demo

Modules
~~~~~~~

Use the election loader manually from within your project.

Elections
^^^^^^^^^

::

    from elex.parser import api

    # Show all elections available.
    # Note: Some elections may be in the past.
    elections = api.Election.get_elections()

    # Get the next election.
    election = api.Election.get_next_election()

Races, Candidates and results
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    from elex.parser import api

    races = api.Election.get_races('2015-10-24', omitResults=False, level="ru")

    for race in races:
        print race

        for reporting_unit in race.reportingunits:
            print "  %s" % reporting_unit

            for candidate in reporting_unit.candidates:
                print "    %s" % candidate

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
