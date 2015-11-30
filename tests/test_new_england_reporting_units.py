from elex.parser import maps
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

    def test_new_england_rollup(self):
        """
        New England states should create county-level rollups.
        One way to test this: FIPS codes should be unique in the
        ReportingUnits. If any FIPS code shows up multiple times,
        we're looking at a New England state.
        """

        self.assertEqual(len(self.races), 2)

        florida_results = [r for r in self.reporting_units if r.raceid == '10005']
        maine_results = [r for r in self.reporting_units if r.raceid == '20978']

        self.assertEqual(len(florida_results), 50)
        self.assertEqual(len(maine_results), 50)
