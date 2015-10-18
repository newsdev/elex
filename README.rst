.. figure:: https://cloud.githubusercontent.com/assets/109988/10567244/25ec282e-75cc-11e5-9d9a-fdeba61828a6.png
   :alt: 

Usage
=====

Demo app
--------

::

    python -m elections.demo

Modules
-------

Use the election loader manually from within your project.

Elections
~~~~~~~~~

::

    from elections import ap

    # Show all elections available.
    # Note: Some elections may be in the past.
    elections = ap.Election.get_elections()

    # Get the next election.
    election = ap.Election.get_next_election()

Races and Candidates
~~~~~~~~~~~~~~~~~~~~

::

    from elections import ap

    election = ap.Election.get_next_election()
    races = election.get_races()

    for race in races:
        print race

        for candidate in race.candidates:
            print candidate
