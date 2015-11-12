import json
import unittest

from elex.parser import api


class ElectionResultsTestCase(unittest.TestCase):
    data_url = 'tests/data/20151103_national.json'

    def setUp(self, **kwargs):
        e = api.Election(electiondate='2015-11-03', datafile=self.data_url, testresults=False, liveresults=True, is_test=False)
        self.raw_races = e.get_raw_races()
        self.race_objs = e.get_race_objects(self.raw_races)
        self.ballot_positions = e.ballot_positions
        self.candidate_reporting_units = e.candidate_reporting_units
        self.candidates = e.candidates
        self.races = e.races
        self.reporting_units = e.reporting_units

    def tearDown(self):
        self.raw_races = None
        self.race_objs = None
        self.ballot_positions = None
        self.candidate_reporting_units = None
        self.candidates = None
        self.races = None
        self.reporting_units = None
