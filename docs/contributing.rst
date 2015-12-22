============
Contributing
============

How To Contribute
=================

Contributors should use the following roadmap to guide them through the process of submitting a contribution:

#. Fork the project on `Github <https://github.com/newsdev/elex>`_.
#. Install a development version of the code with ``pip install -e git+git@github.com:<YOUR_GITHUB_USER>/elex#egg=elex`` 
#. Check out the `issue tracker <https://github.com/newsdev/elex/issues>`_ and pick out a task or create a new issue 
#. Leave a comment on the ticket so that others know you're working on it.
#. Write tests for any new features you add. Add to the tests in the ``tests`` directory or follow the format of files like ``tests/test_election.py``.
#. Write the code, taking care to include well-crafted docstrings and generally following the format of the existing code.
#. Make sure all tests are passing by running ``nose2 tests``
#. Write documentation by adding to one of the files in ``docs`` or adding your own.
#. Submit a pull request on Github.

You got this!

Performance profiling
=====================

To get detailed information about performance, run the tests with the --profile flag:

.. code:: bash

    nose2 tests --profile

Authors
=======

.. include:: ../AUTHORS.rst
