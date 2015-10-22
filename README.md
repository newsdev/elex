![](https://cloud.githubusercontent.com/assets/109988/10567244/25ec282e-75cc-11e5-9d9a-fdeba61828a6.png)

## Usage
### Demo app
```
python -m elex.demo
```

### Modules
Use the election loader manually from within your project.

#### Elections
```
from elex.parser import ap

# Show all elections available.
# Note: Some elections may be in the past.
elections = ap.Election.get_elections()

# Get the next election.
election = ap.Election.get_next_election()
```

#### Races and Candidates
```
from elex.parser import ap

races = ap.Election.get_races('2012-03-13', omitResults=True)

for race in races:
    print race

    for candidate in race.candidates:
        print "  %s" % candidate
```