import json
import unittest

from elex.parser import api

class ElectionResultsTestCase(unittest.TestCase):
    data_url = 'tests/data/20151103_national.json'

    def setUp(self, **kwargs):
        with open(self.data_url, 'r') as readfile:
            self.raw_races = dict(json.loads(readfile.read()))
        e = api.Election(electiondate='2015-11-03', testresults=False, liveresults=True, is_test=False)
        self.race_objs = e.get_race_objects(self.raw_races)
        self.races, self.reporting_units, self.candidate_reporting_units = e.get_units(self.race_objs)
        self.candidates, self.ballot_positions = e.get_uniques(self.candidate_reporting_units)

    def tearDown(self):
        self.races = None
        self.reporting_units = None
        self.candidate_reporting_units = None
        self.candidates = None
        self.ballot_positions = None