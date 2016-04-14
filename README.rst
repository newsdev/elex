.. image:: https://travis-ci.org/newsdev/elex.png
    :target: https://travis-ci.org/newsdev/elex
    :alt: Build status

.. image:: https://img.shields.io/pypi/dw/elex.svg
    :target: https://pypi.python.org/pypi/elex
    :alt: PyPI downloads

.. image:: https://img.shields.io/pypi/v/elex.svg
    :target: https://pypi.python.org/pypi/elex
    :alt: Version

.. image:: https://img.shields.io/pypi/l/elex.svg
    :target: https://github.com/newsdev/elex/blob/master/LICENSE
    :alt: License

.. image:: https://img.shields.io/pypi/pyversions/elex.svg
    :target: https://pypi.python.org/pypi/elex
    :alt: Support Python versions

Get database-ready election results from the Associated Press Election API v2.0.

Elex is designed to be fast, friendly, and largely agnostic to stack/language/database choice. Basic usage is
as simple as:

.. code:: bash

    elex results 2016-03-01 > results.csv

Important links
----------------

* Documentation: http://elex.readthedocs.org/
* Repository: https://github.com/newsdev/elex/
* Issues: https://github.com/newsdev/elex/issues
* Roadmap: https://github.com/newsdev/elex/milestones


Disclaimer
-----------

Elex was developed by The New York Times and NPR and not in concert with the Associated Press. Though we plan on using Elex for the 2016 cycle, there is no guarantee that this software will work for you. If you're thinking about using Elex, check out the `license <https://github.com/newsdev/elex/blob/master/LICENSE>`_ and contact the authors.


Elex projects and implementations
=================================

**NPR**


* `NPR loader <https://github.com/nprapps/ap-election-loader>`_: A simple reference data loader for PostgreSQL.

**New York Times**

* `New York Times Elex loader <https://github.com/newsdev/elex-loader>`_: A more sophisticated data loader for PostgreSQL.
* `New York Times AP Deja Vu <https://github.com/newsdev/ap-deja-vu>`_: A webservice to replay JSON captured during an election.
* `New York Times Elex admin <https://github.com/newsdev/elex-admin>`_: An admin interface for Elex data loaded with the New York Times loader written in Flask.

**Experimental**

* `node-elex-admin <https://github.com/eads/node-elex-admin>`_: Incomplete node-based admin interface.
* `elex-webVideoTextCrawler <https://github.com/OpenNewsLabs/elex-webVideoTextCrawler>`_:  Convert Elex data into HTML5 text track for live video streaming.

News
====

* `Introducing Elex, A Tool To Make Election Coverage Better For Everyone <https://source.opennews.org/en-US/articles/introducing-elex-tool-make-election-coverage-bette/>`_, Jeremy Bowers and David Eads, Source
* `NPR and The New York Times teamed up to make election reporting faster <http://www.poynter.org/news/mediawire/388642/npr-and-the-new-york-times-teamed-up-to-make-election-reporting-faster/>`_, Benjamin Mullin, Poynter

Using the FTP system?
=====================

Use the Los Angeles Times' `python-elections <https://github.com/datadesk/python-elections>`_ library.

The New York Times has `a sample implementation <https://github.com/newsdev/elex-ftp-loader>`_ that demonstrates how you might integrate the FTP loader with your Elex-based system.
