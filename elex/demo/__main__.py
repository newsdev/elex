# -*- coding: utf-8 -*-

import datetime
from sets import Set

from elex.parser import api
from elex import loader
from elex.loader import postgres

if __name__ == "__main__":
    start = datetime.datetime.now()

    candidate_results = []
    reportingunits = []
    races = []

    # Load races, reporting units and candidates into lists.
    for race in api.Election.get_races('2015-10-24', omitResults=False, level="ru"):
        for reporting_unit in race.reportingunits:
            reportingunits.append(reporting_unit)
            candidate_results += [c for c in reporting_unit.candidates]
            del reporting_unit.candidates
        del race.candidates
        del race.reportingunits
        races.append(race)

    candidates = {}
    for c in candidate_results:
        c_dict = {"first": c.first, "last": c.last, "candidateid": c.candidateid, "polid": c.polid, "ballotorder": c.ballotorder, "polnum": c.polnum, "party": c.party}
        if not candidates.get(c.candidateid, None):
            candidates[c.candidateid] = c_dict

    candidates = [postgres.Candidate(**v) for v in candidates.values()]

    print "Parsed %s candidate results." % len(candidate_results)
    print "Parsed %s candidates." % len(candidates)
    print "Parsed %s reporting units." % len(reportingunits)
    print "Parsed %s races.\n" % len(races)

    parse_end = datetime.datetime.now()

    # Connect to the database.
    # Drop and recreate tables, as we're bulk-loading.
    loader.ELEX_PG_CONNEX.connect()
    loader.ELEX_PG_CONNEX.drop_tables([postgres.Candidate, postgres.CandidateResults, postgres.Race, postgres.ReportingUnit], safe=True)
    loader.ELEX_PG_CONNEX.create_tables([postgres.Candidate, postgres.CandidateResults, postgres.Race, postgres.ReportingUnit], safe=True)

    # Do the bulk loads with atomic transactions.
    with loader.ELEX_PG_CONNEX.atomic():
        for idx in range(0, len(candidates), 1000):
            postgres.Candidate.insert_many([c.__dict__['_data'] for c in candidates[idx:idx+1000]]).execute()

    with loader.ELEX_PG_CONNEX.atomic():
        for idx in range(0, len(candidate_results), 1000):
            postgres.CandidateResults.insert_many([c.__dict__ for c in candidate_results[idx:idx+1000]]).execute()

    with loader.ELEX_PG_CONNEX.atomic():
        for idx in range(0, len(reportingunits), 1000):
            postgres.ReportingUnit.insert_many([c.__dict__ for c in reportingunits[idx:idx+1000]]).execute()

    with loader.ELEX_PG_CONNEX.atomic():
        for idx in range(0, len(races), 1000):
            postgres.Race.insert_many([c.__dict__ for c in races[idx:idx+1000]]).execute()

    print "Inserted %s candidate results." % len(candidate_results)
    print "Inserted %s candidates." % len(candidates)
    print "Inserted %s reporting units." % len(reportingunits)
    print "Inserted %s races.\n" % len(races)

    end = datetime.datetime.now()

    print "Overall: %s seconds." % float(str(end - start).split(':')[-1])
    print "  Parsing: %s seconds." % float(str(parse_end - start).split(':')[-1])
    print "  Loading: %s seconds." % float(str(end - parse_end).split(':')[-1])