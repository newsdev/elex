======================
Command line interface
======================

------------------
Commands and flags
------------------

::

    commands:

      ballot-measures
        Get ballot measures

      candidate-reporting-units
        Get candidate reporting units (without results)

      candidates
        Get candidates

      clear-cache
        Clear the elex response cache

      delegates
        Get all delegate reports

      elections
        Get list of available elections

      governor-trends
        Get governor trend report

      house-trends
        Get US House trend report

      next-election
        Get the next election (if date is specified, will be relative to that date, otherwise will use today's date)

      races
        Get races

      reporting-units
        Get reporting units

      results
        Get results

      senate-trends
        Get US Senate trend report

    positional arguments:
      date                  Election date (e.g. "2015-11-03"; most common date
                            formats accepted).

    optional arguments:
      -h, --help            show this help message and exit
      --debug               toggle debug output
      --quiet               suppress all output
      -o {json,csv}         output format (default: csv)
      -t, --test            Use testing API calls
      -n, --not-live        Do not use live data API calls
      -d DATA_FILE, --data-file DATA_FILE
                            Specify data file instead of making HTTP request when
                            using election commands like `elex results` and `elex
                            races`.
      --delegate-sum-file DELEGATE_SUM_FILE
                            Specify delegate sum report file instead of making
                            HTTP request when using `elex delegates`
      --delegate-super-file DELEGATE_SUPER_FILE
                            Specify delegate super report file instead of making
                            HTTP request when using `elex delegates`
      --trend-file TREND_FILE
                            Specify trend file instead of making HTTP request when
                            when using `elex [gov/house/senate]-trends`
      --format-json         Pretty print JSON when using `-o json`.
      -v, --version         show program's version number and exit
      --results-level RESULTS_LEVEL
                            Specify reporting level for results
      --raceids RACEIDS     Specify raceids to parse
      --set-zero-counts     Override results with zeros; omits the winner
                            indicator.Sets the vote, delegate, and reporting
                            precinct counts to zero.
      --national-only       Limit results to national-level results only.
      --local-only          Limit results to local-level results only.
      --with-timestamp      Append a `timestamp` column to each row of data output
                            with current system timestamp.
      --batch-name BATCH_NAME
                            Specify a value for a `batchname` column to append to
                            each row.

-----------------
Command reference
-----------------

.. autoclass:: elex.cli.app.ElexBaseController
    :members:
