import tests


class TestRaceIdParsing(tests.ElectionResultsParseIdsTestCase):

    def test_raceid_parsing(self):
        self.assertEqual(len(self.races), 1)


class TestRaceResults(tests.ElectionResultsTestCase):

    def test_raceid_parsing(self):
        self.assertEqual(len(self.races), 5)

    def test_race_is_ballot_measure(self):
        crus = [r.raceid for r in self.candidate_reporting_units
                if r.is_ballot_measure]
        ballot_measure_races = [r for r in self.races
                                if r.raceid in crus]
        for r in ballot_measure_races:
            self.assertEqual(r.is_ballot_measure, True)

    def test_number_of_raw_races(self):
        self.assertEqual(len(self.raw_races['races']), 5)

    def test_number_of_parsed_races(self):
        self.assertEqual(len(self.race_objs), 5)

    def test_number_of_get_units_races(self):
        self.assertEqual(len(self.races), 5)

    def test_composition_of_race_json_national(self):
        race_dict = self.raw_races['races'][-1]
        self.assertEqual(race_dict['national'], True)

    def test_composition_of_race_json_officeid(self):
        race_dict = self.raw_races['races'][-1]
        self.assertEqual(race_dict['officeID'], 'G')

    def test_composition_of_race_json_officename(self):
        race_dict = self.raw_races['races'][-1]
        self.assertEqual(race_dict['officeName'], 'Governor')

    def test_composition_of_race_json_raceid(self):
        race_dict = self.raw_races['races'][-1]
        self.assertEqual(race_dict['raceID'], '18525')

    def test_composition_of_race_json_racetype(self):
        race_dict = self.raw_races['races'][-1]
        self.assertEqual(race_dict['raceType'], 'General')

    def test_composition_of_race_json_racetypeid(self):
        race_dict = self.raw_races['races'][-1]
        self.assertEqual(race_dict['raceTypeID'], 'G')

    def test_race_object_inflation_name(self):
        race = self.race_objs[0]
        self.assertEqual(type(race).__name__, 'Race')

    def test_race_object_inflation_module(self):
        race = self.race_objs[0]
        self.assertEqual(race.__module__, 'elex.api.models')

    def test_race_attribute_construction_officeid(self):
        race = self.race_objs[-1]
        self.assertEqual(race.officeid, 'G')

    def test_race_attribute_construction_statepostal(self):
        race = self.race_objs[-1]
        self.assertEqual(race.statepostal, 'KY')

    def test_race_attribute_construction_raceid(self):
        race = self.race_objs[-1]
        self.assertEqual(race.raceid, '18525')

    def test_race_attribute_construction_general(self):
        race = self.race_objs[-1]
        self.assertEqual(race.racetype, 'General')

    def test_race_attribute_construction_national(self):
        race = self.race_objs[-1]
        self.assertEqual(race.national, True)

    def test_race_attribute_construction_officename(self):
        race = self.race_objs[-1]
        self.assertEqual(race.officename, 'Governor')

    def test_race_attribute_construction_racetypeid(self):
        race = self.race_objs[-1]
        self.assertEqual(race.racetypeid, 'G')

    def test_race_get_units_construction_officeid(self):
        race = self.races[-1]
        self.assertEqual(race.officeid, 'G')

    def test_race_get_units_construction_statepostal(self):
        race = self.races[-1]
        self.assertEqual(race.statepostal, 'KY')

    def test_race_get_units_construction_raceid(self):
        race = self.races[-1]
        self.assertEqual(race.raceid, '18525')

    def test_race_get_units_construction_racetype(self):
        race = self.races[-1]
        self.assertEqual(race.racetype, 'General')

    def test_race_get_units_construction_national(self):
        race = self.races[-1]
        self.assertEqual(race.national, True)

    def test_race_get_units_construction_officename(self):
        race = self.races[-1]
        self.assertEqual(race.officename, 'Governor')

    def test_race_get_units_construction_racetypeid(self):
        race = self.races[-1]
        self.assertEqual(race.racetypeid, 'G')

    def test_existence_of_electiondate(self):
        race = self.races[-1]
        self.assertTrue(hasattr(race, 'electiondate'))

    def test_correct_electiondate(self):
        race = self.races[-1]
        self.assertEqual('2015-11-03', race.electiondate)

    def test_results_level(self):
        self.assertEqual(self.resultslevel, 'ru')


class TestRaceInitialization(tests.ElectionResultsTestCase):
    data_url = 'tests/data/20151103_national_initialization.json'

    def test_json_shape(self):
        self.assertTrue(self.raw_races['races'][0].get('candidates', None))

    def test_initialization_data(self):
        self.assertTrue(self.races[0].initialization_data)

    def test_initialization_data_number_of_races(self):
        self.assertEqual(len(self.races), 2)

    def test_initialization_data_number_of_reportingunits(self):
        self.assertEqual(len(self.reporting_units), 0)

    def test_initialization_data_number_of_candidate_reportingunits(self):
        self.assertEqual(len(self.candidate_reporting_units), 6)
