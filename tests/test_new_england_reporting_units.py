try:
    set
except NameError:
    from sets import Set as set

from elex.api import maps
import tests


class TestConnecticutRollups(tests.ElectionResultsTestCase):
    """
    Connecticut townships not rolling up properly.
    """

    data_url = 'tests/data/20160426_ct_rollups.json'

    def test_ct_has_candidates(self):
        self.assertNotEqual(len(self.candidate_reporting_units), 0)

    def test_ct_has_all_counties(self):
        ct_counties = set()
        raw_counties = [
            r for r in self.reporting_units if
            r.statepostal == "CT" and
            r.level == "county"
        ]
        for c in raw_counties:
            ct_counties.add(c.reportingunitname)

        ct_mapped_counties = set(maps.FIPS_TO_STATE['CT'].keys())

        self.assertEqual(len(ct_counties), len(ct_mapped_counties))

    def test_ct_counties_match_townships(self):
        ct_counties = [
            r for r in self.reporting_units if
            r.statepostal == "CT" and
            r.level == "county"
        ]

        for county in ct_counties:
            races = set([
                r.raceid for r in self.reporting_units if
                r.statepostal == "CT" and
                r.level == "township" and
                r.fipscode == county.fipscode
            ])
            for race in races:
                townships = [
                    r.precinctstotal for r in self.reporting_units if
                    r.statepostal == "CT" and
                    r.level == "township" and
                    r.fipscode == county.fipscode and
                    r.raceid == race
                ]
                self.assertEqual(county.precinctstotal, sum(townships))


class TestRhodeIslandEdgeCageReportingUnits(tests.ElectionResultsTestCase):
    """
    Mail ballots listed as townships. Breaks rollups for RI.
    """
    data_url = 'tests/data/20160426-ri_mail_ballots.json'

    def test_existence_of_mail_ballots(self):
        ri_results = [
            r for r in self.reporting_units if
            r.statepostal == "RI"
        ]
        mail_ballots = []
        for z in ri_results:
            try:
                if "C.D." in z.reportingunitname:
                    mail_ballots.append(z)
            except TypeError:
                pass
        self.assertTrue(len(mail_ballots) > 0)

    def test_mail_ballots_are_townships(self):
        ri_results = [
            r for r in self.reporting_units if
            r.statepostal == "RI"
        ]
        for z in ri_results:
            try:
                if "C.D." in z.reportingunitname:
                    self.assertTrue(z.level, "Township")

            except TypeError:
                pass


class TestMaineEdgeCaseReportingUnits(tests.ElectionResultsTestCase):
    """
    Should get two reporting units from this Maine file: One is the
    state level, the other is a level 'subunit' which is actually
    the state level data as well. #228.
    """
    data_url = 'tests/data/20160305_me_no_townships.json'
    NE_STATES = maps.FIPS_TO_STATE.keys()

    def test_number_of_reporting_units(self):
        maine_results = [
            r for r in self.reporting_units if r.raceid == '20852'
        ]
        self.assertEqual(len(maine_results), 2)

    def test_one_state_level_unit(self):
        maine_results = [
            r for r in self.reporting_units if r.raceid == '20852'
        ]
        maine_state_level_units = [
            r for r in maine_results if r.level == 'state'
        ]
        self.assertEqual(len(maine_state_level_units), 1)

    def test_one_subunit(self):
        maine_results = [
            r for r in self.reporting_units if r.raceid == '20852'
        ]
        maine_subunits = [
            r for r in maine_results if r.level == 'state'
        ]
        self.assertEqual(len(maine_subunits), 1)


class TestNewEnglandReportingUnits(tests.ElectionResultsTestCase):
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

    def test_maine_county_votepcts_are_correct(self):
        """
        From ticket 220.
        """
        maine_results = [
            r for r in self.results if r.raceid == '20978'
        ]
        county_results = [
            r for r in maine_results if r.level == 'county'
        ]
        cumberland_results = [
            r for r in county_results if r.fipscode == '23005'
        ]
        self.assertNotEqual(
            cumberland_results[0].votepct,
            cumberland_results[1].votepct
        )

    def test_maine_county_votecounts_are_correct(self):
        """
        From ticket 220.
        """
        maine_results = [
            r for r in self.results if r.raceid == '20978'
        ]
        county_results = [
            r for r in maine_results if r.level == 'county'
        ]
        cumberland_results = [
            r for r in county_results if r.fipscode == '23005'
        ]
        self.assertNotEqual(
            cumberland_results[0].votecount,
            cumberland_results[1].votecount
        )

    def test_maine_counties_have_votecouts(self):
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
