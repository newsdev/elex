======================
Command line interface
======================

::

  commands:

    ballot-positions
      Get ballot positions (also known as ballot issues)

    candidate-reporting-units
      Get candidate reporting units (without results)

    candidates
      Get candidates

    elections
      Get list of available elections

    next-election
      Get the next election (if date is specified, will be relative to that date, otherwise will use today's date)

    races
      Get races

    reporting-units
      Get reporting units

    results
      Get results

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
                          Specify data file instead of making HTTP request
    --format-json         Pretty print JSON (only when using -o json)
    -v, --version         show program's version number and exit
