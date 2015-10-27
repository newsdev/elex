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
    from elex import loader
    from elex.loader import postgres

    candidates = []
    reportingunits = []
    races = []

    # Load races, reporting units and candidates into a database.

for race in api.Election.get\_races('2015-10-24', omitResults=False,
level="ru"): for reporting\_unit in race.reportingunits:
reportingunits.append(reporting\_unit) candidates += [c for c in
reporting\_unit.candidates] del reporting\_unit.candidates del
race.candidates del race.reportingunits races.append(race)

print "Parsed %s candidates." % len(candidates) print "Parsed %s
reporting units." % len(reportingunits) print "Parsed %s
races.:raw-latex:`\n`" % len(races)

Connect to the database.
========================

Drop and recreate tables, as we're bulk-loading.
================================================

loader.ELEX\_PG\_CONNEX.connect()
loader.ELEX\_PG\_CONNEX.drop\_tables([postgres.Candidate, postgres.Race,
postgres.ReportingUnit], safe=True)
loader.ELEX\_PG\_CONNEX.create\_tables([postgres.Candidate,
postgres.Race, postgres.ReportingUnit], safe=True)

Do the bulk loads with atomic transactions.
===========================================

with loader.ELEX\_PG\_CONNEX.atomic(): for idx in range(0,
len(candidates), 1000): postgres.Candidate.insert\_many([c.\ **dict**
for c in candidates[idx:idx+1000]]).execute()

with loader.ELEX\_PG\_CONNEX.atomic(): for idx in range(0,
len(reportingunits), 1000):
postgres.ReportingUnit.insert\_many([c.\ **dict** for c in
reportingunits[idx:idx+1000]]).execute()

with loader.ELEX\_PG\_CONNEX.atomic(): for idx in range(0, len(races),
1000): postgres.Race.insert\_many([c.\ **dict** for c in
races[idx:idx+1000]]).execute()

print "Inserted %s candidates." % len(candidates) print "Inserted %s
reporting units." % len(reportingunits) print "Inserted %s races." %
len(races) \`\`\`

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
