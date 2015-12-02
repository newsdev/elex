========
Tutorial
========

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
