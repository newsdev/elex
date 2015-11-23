========
Tutorial
========

This tool is primarily designed for use on the command line using
standard \*NIX operations like pipes and output redirection.

To write a stream of races in CSV format to your terminal, run:

.. code:: bash

    elex init-races '11-03-2015'

To write this data to a file:

.. code:: bash

    elex init-races '11-03-2015' > races.csv

To pipe it into PostgreSQL:

.. code:: bash

    elex init-races '11-03-2015' | psql elections -c "COPY races FROM stdin DELIMITER ',' CSV HEADER;"```

Output could also be piped to tools like sed, awk, or csvkit.
