============
Contributing
============

We welcome contributions of all sizes. You got this!

Find a task
===========

1. Check out the `issue tracker <https://github.com/newsdev/elex/issues>`_ and pick out a task or create a new issue 

2. Leave a comment on the ticket so that others know you're working on it.

Install Elex development environment
====================================

1. Fork the project on `Github <https://github.com/newsdev/elex>`_.

2. Install a development version of the code with:

.. code:: bash

  mkvirtualenv elex-dev
  pip install -e git+git@github.com:<YOUR_GITHUB_USER>/elex#egg=elex``

3. Install developer dependencies for tests and docs:

.. code:: bash

  pip install Sphinx==1.3.1
  pip install nose2==0.5.0
  pip install tox==2.3.1

Now you can run the following commands when you want to activate your enviroment and
cd to the source directory.

.. code:: bash

  workon elex-dev
  cd ${VIRTUAL_ENV}/src/elex

Running tests
=============

Edit or write the code or docs, taking care to include well=crafted docstrings and generally following the format of the existing code.

Write tests for any new features you add. Add to the tests in the ``tests`` directory or follow the format of files like ``tests/test_election.py``.

Make sure all tests are passing in your environment by running the nose2 tests.

.. code:: bash

   nose2 tests

If you have Python 2.7, 3.5, and pypy installed, run can run :code:`tox` to test in multiple environments.

Writing docs
============

Write documentation by adding to one of the files in :code:`docs` or adding your own.

To build a local preview, run:

.. code:: bash

  make -C docs html

The documentation is built in :code:`docs/_build/html`. Use Python's simple HTTP server to view it.

.. code:: bash

  cd docs/_build/html
  python -m http.server

Python 2.7 users should use :code:`SimpleHTTPServer` instead of :code:`http.server`.


Submitting code
===============

Submit a pull request on Github.

Testing performance
===================

To get detailed information about performance, run the tests with the ==profile flag:

.. code:: bash

    nose2 tests --profile

Testing API request limit
=========================

You can test the API request limit, but only by setting an environment variable. Use with extreme
care.

.. code:: bash

    AP_RUN_QUOTA_TEST=1 nose2 tests.test_ap_quota

Authors
=======

.. include:: ../AUTHORS.rst
