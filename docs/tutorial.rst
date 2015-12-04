========
Tutorial
========

Command Line Interface
----------------------

This tool is primarily designed for use on the command line using
standard \*NIX operations like pipes and output redirection.

To write a stream of races in CSV format to your terminal, run:

.. code:: bash

    elex races '11-03-2015'

To write this data to a file:

.. code:: bash

    elex races '11-03-2015' > races.csv

To pipe it into PostgreSQL:

.. code:: bash

    elex races 11-03-2015 | psql elections -c "COPY races FROM stdin DELIMITER ',' CSV HEADER;"```

To get JSON output:

.. code:: bash

    elex races 11-03-2015 -o json

Output can be piped to tools like sed, awk, jq, or csvkit for further processing.

Python Modules
---------------

Perhaps you'd like to use Python objects in your application. This is how you would call the Elex modules directly without using the command line tool.

.. code:: python

    from elex.parser import api

    # Setup and call the AP API.
    e = api.Election(electiondate='2015-11-03', datafile=None, testresults=False, liveresults=True, is_test=False)
    raw_races = e.get_raw_races()
    race_objs = e.get_race_objects(raw_races)

    # Get lists of Python objects for each of the core models.
    ballot_measures = e.ballot_measures
    candidate_reporting_units = e.candidate_reporting_units
    candidates = e.candidates
    races = e.races
    reporting_units = e.reporting_units
    results = e.results
