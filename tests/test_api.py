#!/usr/bin/env python

import unittest
from elex.parser import api

class APAPITestCase(unittest.TestCase):

    def setUp(self):
        self.races = api.Election.get_races("2015-11-03", omitResults=False, level="ru", test=True)

    def test_number_of_races(self):
        self.assertEqual(len(self.races), 479)

    def test_number_of_candidate(self):
        num_candidates = 0
        for race in self.races:
            num_candidates += len(race.candidates)
        self.assertEqual(num_candidates, 674)

    def test_number_of_reporting_units(self):
        num_reporting_units = 0
        for race in self.races:
            num_reporting_units += len(race.reportingunits)
        self.assertEqual(num_reporting_units, 7183)

    def test_number_of_candidate_results(self):
        num_candidate_results = 0
        for race in self.races:
            for reporting_unit in race.reportingunits:
                num_candidate_results += len(reporting_unit.candidates)
        self.assertEqual(num_candidate_results, 15129)
