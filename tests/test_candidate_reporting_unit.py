import tests

class TestCandidateReportingUnit(tests.ElectionResultsTestCase):

    def test_number_of_parsed_candidate_reporting_units(self):
        self.assertEqual(len(self.candidate_reporting_units), 612)

    def test_composition_of_candidate_reporting_units_json(self):
        cru_dict = self.raw_races['races'][1]['reportingUnits'][0]['candidates'][0]
        self.assertEqual(cru_dict['first'], 'Phil')
        self.assertEqual(cru_dict['last'], 'Bryant')
        self.assertEqual(cru_dict['party'], 'GOP')
        self.assertEqual(cru_dict['incumbent'], True)
        self.assertEqual(cru_dict['candidateID'], '31345')
        self.assertEqual(cru_dict['polID'], '27207')
        self.assertEqual(cru_dict['ballotOrder'], 1)
        self.assertEqual(cru_dict['polNum'], '25514')
        self.assertEqual(cru_dict['voteCount'], 472197)
        self.assertEqual(cru_dict['winner'], 'X')

    def test_candidate_reporting_unit_object_inflation(self):
        cru = self.candidate_reporting_units[0]
        self.assertEqual(type(cru).__name__, 'CandidateReportingUnit')
        self.assertEqual(cru.__module__, 'elex.parser.api')

    def test_candidate_reporting_unit_get_units_construction(self):
        cru = self.candidate_reporting_units[0]
        self.assertEqual(cru.first, 'Jack')
        self.assertEqual(cru.last, 'Conway')
        self.assertEqual(cru.party, 'Dem')
        self.assertEqual(cru.candidateid, '5266')
        self.assertEqual(cru.polid, '204')
        self.assertEqual(cru.ballotorder, 1)
        self.assertEqual(cru.polnum, '19601')
        self.assertEqual(cru.votecount, 426944)
        self.assertEqual(cru.winner, False)
        self.assertEqual(cru.incumbent, False)

    def test_candidate_reporting_unit_sums(self):
        # Grab the KY governor's race.
        race = self.races[0]

        # Grab the reporting unit associated with this race.
        reporting_unit = self.reporting_units[0]

        # Grab the three candidate reporting units associated with
        # this reporting unit.
        candidate_reporting_units = self.candidate_reporting_units[0:3]

        # Hand-added for additional (in)accuracy.
        actual_sums_from_json = 511771 + 426944 + 35629
        sum_candidate_reporting_units = sum([v.votecount for v in candidate_reporting_units])

        # Make sure we got the right race / reporting unit / candidate reporting units.
        # Thankfully, we denormalized the race fields all the way down!
        for cru in candidate_reporting_units:
            self.assertEqual(cru.raceid, '18525')
            self.assertEqual(cru.level, 'state')

        # The highest-level reporting unit votecount and the sum of votes from the
        # candidate reporting units within that reporting unit should be equal.
        self.assertEqual(reporting_unit.votecount, actual_sums_from_json)
        self.assertEqual(sum_candidate_reporting_units, actual_sums_from_json)
        self.assertEqual(sum_candidate_reporting_units, reporting_unit.votecount)