try:
    set
except NameError:
    from sets import Set as set

from elex.api import maps
import tests


class TestPrecinctsReportingPctFloat(tests.ElectionResultsTestCase):
    data_url = 'tests/data/20160301_super_tuesday.json'

    def test_precincts_reporting_pct_less_than_one_point_oh(self):
        results = [r for r in self.results]
        for r in results:
            percent = float(r.precinctsreporting) / float(r.precinctstotal)
            self.assertEqual(
                "%.4f" % r.precinctsreportingpct,
                "%.4f" % percent
            )
            self.assertLessEqual(r.precinctsreportingpct, 1.00)
            self.assertGreaterEqual(r.precinctsreportingpct, 0.00)

    def test_supertuesday_electiondate(self):
        self.assertEqual(self.election.electiondate, '2016-03-01')

    def test_number_of_counties(self):
        """
        According to bug #236, we should be 1 county short.
        """
        mass_results = [
            r for r in self.results if
            r.raceid == '24547' and
            r.level == 'county' and
            r.last == 'Trump'
        ]
        self.assertEqual(len(mass_results), len(maps.FIPS_TO_STATE['MA']))


class TestGeneralElectionEdgeCases(tests.ElectionResultsTestCase):
    data_url = 'tests/data/20121106_ak_prez.json'

    """
    There should be 51 unique state reportingunit ids, not 1.
    """
    def test_general_stateids(self):
        state_results = [r.reportingunitid for r in self.reporting_units if r.level == 'state']
        unique_state_results = list(set(state_results))
        self.assertEqual(len(state_results), len(unique_state_results))

    """
    There should be some fields for electoral votes.
    """
    def test_electwon_exists_cru(self):
        r = [r for r in self.results if r.officeid == 'P' and r.level == 'state'][0]
        self.assertTrue(hasattr(r, 'electwon'))
        self.assertTrue(hasattr(r, 'electtotal'))

    def test_electtotal_exists_ru(self):
        r = [r for r in self.reporting_units if r.officeid == 'P' and r.level == 'state'][0]
        self.assertTrue(hasattr(r, 'electtotal'))

    """
    Romney won all 3 of AK's electoral votes in 2012.
    """
    def test_electwon_is_set(self):
        r = [r for r in self.results if r.officeid == 'P' and r.level == 'state' and r.last == 'Romney' and r.statepostal == 'AK'][0]
        self.assertEqual(r.electwon, 3)

    def test_electtotal_is_set(self):
        r = [r for r in self.results if r.officeid == 'P' and r.level == 'state' and r.last == 'Romney' and r.statepostal == 'AK'][0]
        self.assertEqual(r.electtotal, 3)
