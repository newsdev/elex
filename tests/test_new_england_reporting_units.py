from elex.api import maps
import tests


class TestCandidate(tests.ElectionResultsTestCase):
    data_url = 'tests/data/20121106_me_fl_senate.json'
    NE_STATES = maps.FIPS_TO_STATE.keys()

    def test_number_of_races(self):
        self.assertEqual(len(self.races), 2)

    def test_results_parsing_florida(self):
        florida_results = [
            r for r in self.reporting_units if r.raceid == '10005'
        ]
        self.assertEqual(len(florida_results), 68)

    def test_results_parsing_maine(self):
        maine_results = [
            r for r in self.reporting_units if r.raceid == '20978'
        ]
        self.assertEqual(len(maine_results), 516)

    def test_florida_townships(self):
        florida_results = [
            r for r in self.reporting_units if r.raceid == '10005'
        ]
        florida_townships = [
            r for r in florida_results if r.level == 'township'
        ]
        self.assertEqual(len(florida_townships), 0)

    def test_florida_counties(self):
        florida_results = [
            r for r in self.reporting_units if r.raceid == '10005'
        ]
        florida_counties = [r for r in florida_results if r.level == 'county']
        self.assertEqual(len(florida_counties), len(florida_results) - 1)

    def test_maine_townships(self):
        maine_results = [
            r for r in self.reporting_units if r.raceid == '20978'
        ]
        maine_townships = [r for r in maine_results if r.level == 'township']
        count_maine_counties = len(maps.FIPS_TO_STATE['ME'].keys())
        count_maine_results_minus_state = len(maine_results) - 1
        self.assertEqual(
            len(maine_townships),
            count_maine_results_minus_state - count_maine_counties
        )

    def test_maine_counties(self):
        maine_results = [
            r for r in self.reporting_units if r.raceid == '20978'
        ]
        maine_counties = [
            r for r in maine_results if r.level == 'county'
        ]
        count_maine_counties = len(maps.FIPS_TO_STATE['ME'].keys())
        self.assertEqual(len(maine_counties), count_maine_counties)

    def test_maine_counties_have_statepostal(self):
        maine_results = [
            r for r in self.reporting_units if r.raceid == '20978'
        ]
        maine_counties = [r for r in maine_results if r.level == 'county']
        for c in maine_counties:
            self.assertEqual(c.statepostal, 'ME')

    def test_maine_counties_have_statename(self):
        maine_results = [
            r for r in self.reporting_units if r.raceid == '20978'
        ]
        maine_counties = [r for r in maine_results if r.level == 'county']
        for c in maine_counties:
            self.assertEqual(c.statename, 'Maine')

    def test_main_counties_have_votecouts(self):
        """
        From ticket 0179.
        Vote count is camelcased.
        """
        maine_results = [
            r for r in self.reporting_units if r.raceid == '20978'
        ]
        maine_counties = [r for r in maine_results if r.level == 'county']
        for c in maine_counties:
            self.assertFalse(c.votecount == 0)
