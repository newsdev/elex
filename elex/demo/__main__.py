# -*- coding: utf-8 -*-

import datetime

from elex.parser import api
from elex import loader
from elex.loader import postgres

if __name__ == "__main__":
    """
    Load races, reporting units, candidate results, candidates
    and ballot positions into lists of dicts and then bulk insert
    those into the DB using Peewee and psycopg2.
    """


    start = datetime.datetime.now()

    e = api.Election(electiondate='2015-11-03', testresults=False, liveresults=True, is_test=False)
    raw_races = e.get_races(omitResults=False, level="ru", test=False)

    races, reporting_units, candidate_reporting_units = e.get_units(raw_races)
    candidates, ballot_positions = e.get_uniques(candidate_reporting_units)

    print "Parsed %s races." % len(races)
    print "Parsed %s candidates." % len(candidates)
    print "Parsed %s ballot positions." % len(ballot_positions)
    print "Parsed %s reporting units." % len(reporting_units)
    print "Parsed %s candidate reporting units." % len(candidate_reporting_units)

    parse_end = datetime.datetime.now()

    DB_MAPPING = [
        (postgres.Candidate, candidates),
        (postgres.BallotPosition, ballot_positions),
        (postgres.CandidateReportingUnit, candidate_reporting_units),
        (postgres.ReportingUnit, reporting_units),
        (postgres.Race, races)
    ]

    # # Connect to the database.
    # # Drop and recreate tables, as we're bulk-loading.
    loader.ELEX_PG_CONNEX.connect()
    loader.ELEX_PG_CONNEX.drop_tables([m[0] for m in DB_MAPPING], safe=True)
    loader.ELEX_PG_CONNEX.create_tables([m[0] for m in DB_MAPPING], safe=True)

    for obj, obj_list in DB_MAPPING:
        with loader.ELEX_PG_CONNEX.atomic():
            for idx in range(0, len(obj_list), 2000):
                obj.insert_many([o.__dict__ for o in obj_list[idx:idx+2000]]).execute()

    loader.ELEX_PG_CONNEX.close()

    print "Inserted %s races." % len(races)
    print "Inserted %s candidates." % len(candidates)
    print "Inserted %s ballot positions." % len(ballot_positions)
    print "Inserted %s reporting units." % len(reporting_units)
    print "Inserted %s candidate reporting units." % len(candidate_reporting_units)

    end = datetime.datetime.now()

    print "Overall: %s seconds." % float(str(end - start).split(':')[-1])
    print "Parsing: %s seconds." % float(str(parse_end - start).split(':')[-1])
    print "Loading: %s seconds." % float(str(end - parse_end).split(':')[-1])
