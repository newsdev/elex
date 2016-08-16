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


class TestMassRollupBug(tests.ElectionResultsTestCase):
    """
    Adding up all of the level "township" should equal
    the totals for "county" but that's not true for
    Nantucket county, MA and the townships in fips 25019.
    """
    data_url = 'tests/data/20160301_super_tuesday.json'

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


class TestElectionDateSuperTuesday(tests.ElectionResultsTestCase):
    """
    When using data files, election date should be automatically inferred.
    """
    data_url = 'tests/data/20160301_super_tuesday.json'

    def test_supertuesday_electiondate(self):
        self.assertEqual(self.election.electiondate, '2016-03-01')


class TestElectionDate2015(tests.ElectionResultsTestCase):
    """
    When using data files, election date should be automatically inferred.
    """
    data_url = 'tests/data/20151103_national.json'

    def test_2015_electiondate(self):
        self.assertEqual(self.election.electiondate, '2015-11-03')
