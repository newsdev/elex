#!/usr/bin/env python

import unittest
from elex.parser import api

class APAPITestCase(unittest.TestCase):

    def setUp(self):
        self.races = api.Election.get_races("2015-11-03", omitResults=False, level="ru", test=True)

    def test_number_of_races(self):
        self.assertEqual(len(self.races), 479)

