from elex.api import maps
import tests

class TestCandidate(tests.ElectionResultsTestCase):
    """
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
        self.results = e.results
    """
    data_url = 'tests/data/20121106_me_fl_senate.json'
    NE_STATES = maps.FIPS_TO_STATE.keys()

    def test_number_of_races(self):
        self.assertEqual(len(self.races), 2)

    def test_results_parsing(self):
        florida_results = [r for r in self.reporting_units if r.raceid == '10005']
        maine_results = [r for r in self.reporting_units if r.raceid == '20978']

        self.assertEqual(len(florida_results), 68)
        self.assertEqual(len(maine_results), 516)

    def test_florida_townships(self):
        florida_results = [r for r in self.reporting_units if r.raceid == '10005']
        florida_townships = [r for r in florida_results if r.level == 'township']

        self.assertEqual(len(florida_townships), 0)

    def test_florida_counties(self):
        florida_results = [r for r in self.reporting_units if r.raceid == '10005']
        florida_counties = [r for r in florida_results if r.level == 'county']

        # One result will be for the state.
        self.assertEqual(len(florida_counties), len(florida_results) - 1)

    def test_maine_townships(self):
        maine_results = [r for r in self.reporting_units if r.raceid == '20978']
        maine_townships = [r for r in maine_results if r.level == 'township' ]
        count_maine_counties = len(maps.FIPS_TO_STATE['ME'].keys())
        count_maine_results_minus_state = len(maine_results) - 1

        self.assertEqual(len(maine_townships), count_maine_results_minus_state - count_maine_counties)

    def test_maine_counties(self):
        maine_results = [r for r in self.reporting_units if r.raceid == '20978']
        maine_counties = [r for r in maine_results if r.level == 'county']
        count_maine_counties = len(maps.FIPS_TO_STATE['ME'].keys())

        self.assertEqual(len(maine_counties), count_maine_counties)