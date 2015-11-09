import json
import unittest

from elex.parser import api

class TestRaceParsing(unittest.TestCase):
    def setUp(self):
        with open('tests/data/test_data.json', 'r') as readfile:
            self.raw_races = list(json.loads(readfile.read())['races'])
        e = api.Election(electiondate='2015-11-03', testresults=False, liveresults=True, is_test=False)
        self.parsed_races = [api.Race(**r) for r in self.raw_races]
        self.races, self.reporting_units, self.candidate_reporting_units = e.get_units(self.parsed_races)

    def tearDown(self):
        self.races = None
        self.reporting_units = None
        self.candidate_reporting_units = None

    def test_number_of_raw_races(self):
        self.assertEqual(len(self.raw_races), 2)

    def test_number_of_parsed_races(self):
        self.assertEqual(len(self.parsed_races), 2)

    def test_number_of_get_units_races(self):
        self.assertEqual(len(self.races), 2)

    def test_composition_of_race_json(self):
        race_dict = self.raw_races[0]
        self.assertEqual(race_dict['officeName'], 'Governor')
        self.assertEqual(race_dict['officeID'], 'G')
        self.assertEqual(race_dict['raceID'], '18525')
        self.assertEqual(race_dict['raceType'], 'General')
        self.assertEqual(race_dict['national'], True)
        self.assertEqual(race_dict['officeName'], 'Governor')
        self.assertEqual(race_dict['raceTypeID'], 'G')

    def test_race_object_inflation(self):
        race = self.parsed_races[0]
        self.assertEqual(type(race).__name__, 'Race')
        self.assertEqual(race.__module__, 'elex.parser.api')

    def test_race_attribute_construction(self):
        race = self.parsed_races[0]
        self.assertEqual(race.officeid, 'G')
        self.assertEqual(race.statepostal, 'KY')
        self.assertEqual(race.raceid, '18525')
        self.assertEqual(race.racetype, 'General')
        self.assertEqual(race.national, True)
        self.assertEqual(race.officename, 'Governor')
        self.assertEqual(race.racetypeid, 'G')

    def test_race_get_units_construction(self):
        race = self.races[0]
        self.assertEqual(race.officeid, 'G')
        self.assertEqual(race.statepostal, 'KY')
        self.assertEqual(race.raceid, '18525')
        self.assertEqual(race.racetype, 'General')
        self.assertEqual(race.national, True)
        self.assertEqual(race.officename, 'Governor')
        self.assertEqual(race.racetypeid, 'G')