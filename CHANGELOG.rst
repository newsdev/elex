1.2.0 - Feb. 25, 2016
----------------------
Many bugfixes and some new fields / id schemes that might break implementations that rely on stable field names / orders.

* Fixes an issue with requests defaulting to national-only (#229, #230).
* Solves an issue with 3/5 and 3/6 Maine results not including townships (#228).
* Supports a :code:`set-zero-counts` argument to the CLI to return zeroed-out data (#227).
* Includes a :code:`delegatecount` field on :code:`CandidateReportingUnit` to store data from district-level results (#225).
* Supports a :code:`results-level` argument to the CLI to return district-level data. (#223)
* Solves an issue with :code:`reportingunitid` not being unique acrosss different result levels (#226).
* Adds an :code:`electiondate` field on :code:`BallotMeasure` to guarantee uniqueness (#210).
* Makes a composite id for :code:`BallotMeasure` that includes :code:`electiondate` (#210).

1.1.0 - Feb. 2, 2016
--------------------

Documentation and dependency fixes.

* Elex can now be run in the same virtualenv as `csvkit <http://csvkit.readthedocs.org/>`_ (#206).
* Links and copyright notice in documentation updated.
* Added section about virtualenvs to install guide, courtesy of Ryan Pitts.
* Add better tests for AP request quota (#203).

1.0.0 - Jan. 25, 2016
---------------------

The 1.0.x release is named for `Martha Ellis Gellhorn <https://en.wikipedia.org/wiki/Martha_Gellhorn>`_, one of the greatest war correspondents of the 20th century.

* Delegate counts (#138, #194). Delegate counts can be accessed with :code:`elex delegates`.
* Rename :code:`elex.api.api` to :code:`elex.api.models` and allow model objects to be imported with statements like :code:`from elex.api import Election` (#146). Python modules directly calling Elex will need to update their import statements accordingly.
* Fix duplicate IDs (#176).
* Handle incorrect null/none values in some cases (#173, #174, #175).
* Expand contributing / developer guide (#151).
* Add recipe for filtering with jq and uploading to s3 in a single command (#131).

0.2.0 -  Dec. 24, 2015
----------------------

* Tag git versions (#170).
* Fix elections command (#167).
* Use correct state code for county level results (#164).
* Use tox to test multiple Python versions (#153).
* Allow API url to be specified in environment variable (#144).
* Don't sort results for performance and stability (#136).
* Capture and log full API request URL in command line debugging mode (#134).
* Python 3 compatibility (#99).

0.1.2 - Dec. 21, 2015
---------------------

* Fix missing vote percent in results (#152).

0.1.1 - Dec. 10, 2015
-----------------------

* Add Travis CI support (#101).
* Fix packaging.

0.1.0 - Dec. 10, 2015
---------------------

First major release.

* Decided on `elex` for name (#59).
* Initial tests (#70, #107).
* First draft of docs (#18).
* Set up http://elex.readthedocs.org/ (#60).
* Handle New England states (townships and counties) (#123).
* Remove date parsing (#115) and dynamic field setter (#117) to improve performance.

0.0.0 - 0.0.42
--------------

Initial Python API and concept created by Jeremy Bowers; initial command line interface created by David Eads.

