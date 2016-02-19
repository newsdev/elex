import tests


class TestElection(tests.ElectionDistrictResultsTestCase):

    def test_results_level(self):
        self.assertEqual(self.resultslevel, 'district')

    def test_number_of_parsed_races(self):
        self.assertEqual(len(self.race_objs), 2)

    def test_number_of_get_units_races(self):
        self.assertEqual(len(self.races), 2)

    def test_composition_of_race_json_national(self):
        race_dict = self.raw_races['races'][-1]
        self.assertEqual(race_dict['national'], True)

    def test_composition_of_race_json_officeid(self):
        race_dict = self.raw_races['races'][-1]
        self.assertEqual(race_dict['officeID'], 'P')

    def test_composition_of_race_json_officename(self):
        race_dict = self.raw_races['races'][-1]
        self.assertEqual(race_dict['officeName'], 'President')

    def test_composition_of_race_json_raceid(self):
        race_dict = self.raw_races['races'][-1]
        self.assertEqual(race_dict['raceID'], '16957')

    def test_composition_of_race_json_racetype(self):
        race_dict = self.raw_races['races'][-1]
        self.assertEqual(race_dict['raceType'], 'Caucus')

    def test_composition_of_race_json_racetypeid(self):
        race_dict = self.raw_races['races'][-1]
        self.assertEqual(race_dict['raceTypeID'], 'S')

    def test_race_object_inflation_name(self):
        race = self.race_objs[0]
        self.assertEqual(type(race).__name__, 'Race')

    def test_race_object_inflation_module(self):
        race = self.race_objs[0]
        self.assertEqual(race.__module__, 'elex.api.models')

    def test_race_attribute_construction_officeid(self):
        race = self.race_objs[-1]
        self.assertEqual(race.officeid, 'P')

    def test_race_attribute_construction_statepostal(self):
        race = self.race_objs[-1]
        self.assertEqual(race.statepostal, 'IA')

    def test_race_attribute_construction_raceid(self):
        race = self.race_objs[-1]
        self.assertEqual(race.raceid, '16957')

    def test_race_attribute_construction_general(self):
        race = self.race_objs[-1]
        self.assertEqual(race.racetype, 'Caucus')

    def test_race_attribute_construction_national(self):
        race = self.race_objs[-1]
        self.assertEqual(race.national, True)

    def test_race_attribute_construction_officename(self):
        race = self.race_objs[-1]
        self.assertEqual(race.officename, 'President')

    def test_race_attribute_construction_racetypeid(self):
        race = self.race_objs[-1]
        self.assertEqual(race.racetypeid, 'S')

    def test_race_get_units_construction_officeid(self):
        race = self.races[-1]
        self.assertEqual(race.officeid, 'P')

    def test_race_get_units_construction_statepostal(self):
        race = self.races[-1]
        self.assertEqual(race.statepostal, 'IA')

    def test_race_get_units_construction_raceid(self):
        race = self.races[-1]
        self.assertEqual(race.raceid, '16957')

    def test_race_get_units_construction_racetype(self):
        race = self.races[-1]
        self.assertEqual(race.racetype, 'Caucus')

    def test_race_get_units_construction_national(self):
        race = self.races[-1]
        self.assertEqual(race.national, True)

    def test_race_get_units_construction_officename(self):
        race = self.races[-1]
        self.assertEqual(race.officename, 'President')

    def test_race_get_units_construction_racetypeid(self):
        race = self.races[-1]
        self.assertEqual(race.racetypeid, 'S')

    def test_existence_of_electiondate(self):
        race = self.races[-1]
        self.assertTrue(hasattr(race, 'electiondate'))

    def test_correct_electiondate(self):
        race = self.races[-1]
        self.assertEqual('2016-02-01', race.electiondate)
