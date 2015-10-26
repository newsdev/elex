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

    from elex.parser import ap

    # Show all elections available.
    # Note: Some elections may be in the past.
    elections = ap.Election.get_elections()

    # Get the next election.
    election = ap.Election.get_next_election()

Races, Candidates and results
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    from elex.parser import ap

    races = ap.Election.get_races('2015-10-24', omitResults=False, level="reportingUnit")

    for race in races:
        print race

        for reporting_unit in race.reportingunits:
            print "  %s" % reporting_unit

            for candidate in reporting_unit.candidates:
                print "    %s" % candidate
