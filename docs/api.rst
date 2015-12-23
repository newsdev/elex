==========
Python API
==========

Elex provides a Python API that encapsulates Associated Press Election API results as Python
objects.

To use the election loader manually from within your project:

.. code:: python

    from elex.api import api

    election = api.Election(electiondate='2015-11-03', testresults=False, liveresults=True, is_test=False)
    races = election.races

Now you can process or load ``races``.

Models
=========

.. toctree::
    api/election
    api/reportingunit
    api/race
    api/candidate
    api/ballotmeasure
    api/candidatereportingunit
    api/baseobject
    api/elections

Utilities
=========

.. toctree::
    api/utils
    api/maps

