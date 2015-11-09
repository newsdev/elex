import json
import unittest

from elex.parser import api

class TestRaceResults(unittest.TestCase):
    def setUp(self):
        with open('tests/data/20151103_national.json', 'r') as readfile:
            self.raw_races = dict(json.loads(readfile.read()))

        e = api.Election(electiondate='2015-11-03', testresults=False, liveresults=True, is_test=False)
        self.race_objs = e.get_race_objects(self.raw_races)
        self.races, self.reporting_units, self.candidate_reporting_units = e.get_units(self.race_objs)

    def tearDown(self):
        self.races = None
        self.reporting_units = None
        self.candidate_reporting_units = None

    def test_number_of_raw_races(self):
        self.assertEqual(len(self.raw_races['races']), 2)

    def test_number_of_parsed_races(self):
        self.assertEqual(len(self.race_objs), 2)

    def test_number_of_get_units_races(self):
        self.assertEqual(len(self.races), 2)

    def test_composition_of_race_json(self):
        race_dict = self.raw_races['races'][0]
        self.assertEqual(race_dict['officeName'], 'Governor')
        self.assertEqual(race_dict['officeID'], 'G')
        self.assertEqual(race_dict['raceID'], '18525')
        self.assertEqual(race_dict['raceType'], 'General')
        self.assertEqual(race_dict['national'], True)
        self.assertEqual(race_dict['officeName'], 'Governor')
        self.assertEqual(race_dict['raceTypeID'], 'G')

    def test_race_object_inflation(self):
        race = self.race_objs[0]
        self.assertEqual(type(race).__name__, 'Race')
        self.assertEqual(race.__module__, 'elex.parser.api')

    def test_race_attribute_construction(self):
        race = self.race_objs[0]
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

class TestRaceInitialization(unittest.TestCase):
    def setUp(self):
        with open('tests/data/20151103_national_initialization.json') as readfile:
            self.raw_races = dict(json.loads(readfile.read()))

        e = api.Election(electiondate='2015-11-03', testresults=False, liveresults=True, is_test=False)
        self.race_objs = e.get_race_objects(self.raw_races)
        self.races, self.reporting_units, self.candidate_reporting_units = e.get_units(self.race_objs)

    def tearDown(self):
        self.races = None
        self.reporting_units = None
        self.candidate_reporting_units = None

    def test_json_shape(self):
        self.assertTrue(self.raw_races['races'][0].get('candidates', None))

    def test_initialization_data(self):
        self.assertTrue(self.races[0].initialization_data)

    def test_initialization_data_number_of_races(self):
        self.assertEqual(len(self.races), 2)
        self.assertEqual(len(self.reporting_units), 0)
        self.assertEqual(len(self.candidate_reporting_units), 20)