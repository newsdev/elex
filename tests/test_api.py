#!/usr/bin/env python

import unittest
from elex.parser import api

class APAPITestCase(unittest.TestCase):

    def setUp(self):
        self.races = api.Election.get_races("2015-11-03", omitResults=False, level="ru", test=True)

    def test_number_of_races(self):
        self.assertEqual(len(self.races), 479)

    def test_number_of_candidates(self):
        num_candidates = 0
        for race in self.races:
            num_candidates += len(race.candidates)
        self.assertEqual(num_candidates, 674)

#    def test_number_of_ballot_positions(self):
#        self.assertEqual(len(self.ballot_positions), 48)
