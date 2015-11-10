![](https://cloud.githubusercontent.com/assets/109988/10737959/635bfb56-7beb-11e5-9ee5-102eb1582718.png)

## Requirements

* Python 2.7
* pip

### Optional requirements:

* PostgreSQL
* MongoDB

## Installation

Install the Python library:

```bash
pip install nyt-ap-elections
```

Set your AP API key:

```bash
export AP_API_KEY=<MY_AP_API_KEY>
```

## Usage

### Command line utility

This tool is primarily designed for use on the command line using standard *NIX operations like pipes and output redirection.

To write a stream of races in CSV format to your terminal, run:

```bash
elex init-races '11-03-2015'
```

To write this data to a file:

```bash
elex init-races '11-03-2015' > races.csv
```

To pipe it into PostgreSQL:

```bash
elex init-races '11-03-2015' | psql elections -c "COPY races FROM stdin DELIMITER ',' CSV HEADER;"```
```

Output could also be piped to tools like sed, awk, or csvkit.


### Demo app

See the [NPR Visuals Demo Loader](https://github.com/nprapps/ap-election-loader).

### Modules
Use the election loader manually from within your project.

```python
from elex.parser import api
from elex import loader
from elex.loader import postgres

e = api.Election(electiondate='2015-11-03', testresults=False, liveresults=True, is_test=False)
raw_races = e.get_races(omitResults=False, level="ru", test=False)

races, reporting_units, candidate_reporting_units = e.get_units(raw_races)
candidates, ballot_positions = e.get_uniques(candidate_reporting_units)

DB_MAPPING = [
    (postgres.Candidate, candidates),
    (postgres.BallotPosition, ballot_positions),
    (postgres.CandidateReportingUnit, candidate_reporting_units),
    (postgres.ReportingUnit, reporting_units),
    (postgres.Race, races)
]

loader.ELEX_PG_CONNEX.connect()
loader.ELEX_PG_CONNEX.drop_tables([mapping[0] for mapping in DB_MAPPING], safe=True)
loader.ELEX_PG_CONNEX.create_tables([mapping[0] for mapping in DB_MAPPING], safe=True)

for obj, obj_list in DB_MAPPING:
    with loader.ELEX_PG_CONNEX.atomic():
        for idx in range(0, len(obj_list), 2000):
            obj.insert_many([o.__dict__ for o in obj_list[idx:idx+2000]]).execute()

loader.ELEX_PG_CONNEX.close()
```

## Options
### Recording
#### Flat files
Will record timestamped and namespaced files to the `ELEX_RECORDING_DIR` before parsing.

```bash
export ELEX_RECORDING=flat
export ELEX_RECORDING_DIR=/tmp
```

#### MongoDB
Will record a timestamped record to MongoDB, connecting via `ELEX_RECORDING_MONGO_URL` and writing to the `ELEX_RECORDING_MONGO_DB` database.

```bash
export ELEX_RECORDING=mongodb
export ELEX_RECORDING_MONGO_URL=mongodb://localhost:27017/  # Or your own connection string.
export ELEX_RECORDING_MONGO_DB=ap_elections_loader
```

## Development
### Run tests
```bash
nosetests
```