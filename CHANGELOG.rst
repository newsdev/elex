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

