import tests


class TestCandidateReportingUnit(tests.ElectionResultsTestCase):

    def test_zero_votes(self):
        cru = [
            c for c in self.candidate_reporting_units
            if c.reportingunitid == '6020'
        ]
        for c in cru:
            self.assertEqual(c.votepct + c.votecount, 0.0)

    def test_number_of_parsed_candidate_reporting_units(self):
        self.assertEqual(len(self.candidate_reporting_units), 505)

    def test_composition_of_candidate_reporting_units_json_first(self):
        ru_dict = self.raw_races['races'][-1]['reportingUnits'][0]
        cru_dict = ru_dict['candidates'][1]
        self.assertEqual(cru_dict['first'], 'Jack')

    def test_composition_of_candidate_reporting_units_json_last(self):
        ru_dict = self.raw_races['races'][-1]['reportingUnits'][0]
        cru_dict = ru_dict['candidates'][1]
        self.assertEqual(cru_dict['last'], 'Conway')

    def test_composition_of_candidate_reporting_units_json_party(self):
        ru_dict = self.raw_races['races'][-1]['reportingUnits'][0]
        cru_dict = ru_dict['candidates'][1]
        self.assertEqual(cru_dict['party'], 'Dem')

    def test_composition_of_candidate_reporting_units_json_candidateid(self):
        ru_dict = self.raw_races['races'][-1]['reportingUnits'][0]
        cru_dict = ru_dict['candidates'][1]
        self.assertEqual(cru_dict['candidateID'], '5266')

    def test_composition_of_candidate_reporting_units_json_polid(self):
        ru_dict = self.raw_races['races'][-1]['reportingUnits'][0]
        cru_dict = ru_dict['candidates'][1]
        self.assertEqual(cru_dict['polID'], '204')

    def test_composition_of_candidate_reporting_units_json_ballotorder(self):
        ru_dict = self.raw_races['races'][-1]['reportingUnits'][0]
        cru_dict = ru_dict['candidates'][1]
        self.assertEqual(cru_dict['ballotOrder'], 1)

    def test_composition_of_candidate_reporting_units_json_polnum(self):
        ru_dict = self.raw_races['races'][-1]['reportingUnits'][0]
        cru_dict = ru_dict['candidates'][1]
        self.assertEqual(cru_dict['polNum'], '19601')

    def test_composition_of_candidate_reporting_units_json_votecount(self):
        ru_dict = self.raw_races['races'][-1]['reportingUnits'][0]
        cru_dict = ru_dict['candidates'][1]
        self.assertEqual(cru_dict['voteCount'], 426944)

    def test_candidate_reporting_unit_object_inflation_name(self):
        cru = self.candidate_reporting_units[0]
        self.assertEqual(type(cru).__name__, 'CandidateReportingUnit')

    def test_candidate_reporting_unit_object_inflation_module(self):
        cru = self.candidate_reporting_units[0]
        self.assertEqual(cru.__module__, 'elex.api.models')

    def test_existence_of_electiondate(self):
        cru = self.candidate_reporting_units[0]
        self.assertTrue(hasattr(cru, 'electiondate'))

    def test_correct_electiondate(self):
        cru = self.candidate_reporting_units[0]
        self.assertEqual('2015-11-03', cru.electiondate)

    def test_candidate_reporting_unit_get_units_construction_raceid(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1]
        self.assertEqual(cru.raceid, '18525')

    def test_candidate_reporting_unit_get_units_construction_first(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1]
        self.assertEqual(cru.first, 'Jack')

    def test_candidate_reporting_unit_get_units_construction_last(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1]
        self.assertEqual(cru.last, 'Conway')

    def test_candidate_reporting_unit_get_units_construction_party(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1]
        self.assertEqual(cru.party, 'Dem')

    def test_candidate_reporting_unit_get_units_construction_candidateid(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1]
        self.assertEqual(cru.candidateid, '5266')

    def test_candidate_reporting_unit_get_units_construction_polid(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1]
        self.assertEqual(cru.polid, '204')

    def test_candidate_reporting_unit_get_units_construction_ballotorder(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1]
        self.assertEqual(cru.ballotorder, 1)

    def test_candidate_reporting_unit_get_units_construction_polnum(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1]
        self.assertEqual(cru.polnum, '19601')

    def test_candidate_reporting_unit_get_units_construction_votecount(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1]
        self.assertEqual(cru.votecount, 504)

    def test_candidate_reporting_unit_get_units_construction_votepct(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1]
        self.assertEqual(cru.votepct, 0.45652173913043476)

    def test_candidate_reporting_unit_get_units_construction_winner(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1]
        self.assertEqual(cru.winner, False)

    def test_candidate_reporting_unit_get_units_construction_incumbent(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1]
        self.assertEqual(cru.incumbent, False)

    def test_candidate_reporting_unit_count(self):
        self.assertEqual(len(self.candidate_reporting_units), 505)

    def test_candidate_reporting_unit_sums_raceid(self):
        candidate_reporting_units = self.candidate_reporting_units[0:2]
        for cru in candidate_reporting_units:
            self.assertEqual(cru.raceid, '7582')

    def test_candidate_reporting_unit_sums_level(self):
        candidate_reporting_units = self.candidate_reporting_units[0:2]
        for cru in candidate_reporting_units:
            self.assertEqual(cru.level, 'state')

    def test_candidate_reporting_unit_sums_reportingunit_pct(self):
        reporting_unit = self.reporting_units[0]
        candidate_reporting_units = self.candidate_reporting_units[0:2]
        self.assertEqual(
            (
                candidate_reporting_units[0].votecount /
                float(reporting_unit.votecount)
            ),
            0.694266390666554
        )

    def test_candidate_reporting_unit_sums_to_reportingunit(self):
        reporting_unit = self.reporting_units[0]
        actual_sums_from_json = 805617 + 354769
        self.assertEqual(reporting_unit.votecount, actual_sums_from_json)

    def test_candidate_reporting_unit_sums_to_candidatereportingunit(self):
        candidate_reporting_units = self.candidate_reporting_units[0:2]
        actual_sums_from_json = 805617 + 354769
        sum_candidate_reporting_units = sum(
            [v.votecount for v in candidate_reporting_units]
        )
        self.assertEqual(sum_candidate_reporting_units, actual_sums_from_json)

    def test_candidate_reporting_unit_sums_reportingunit(self):
        reporting_unit = self.reporting_units[0]
        candidate_reporting_units = self.candidate_reporting_units[0:2]
        sum_candidate_reporting_units = sum(
            [v.votecount for v in candidate_reporting_units]
        )
        self.assertEqual(
            sum_candidate_reporting_units,
            reporting_unit.votecount
        )

    def test_candidate_reporting_unit_serialization_keys_raceid(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1].serialize()
        self.assertEqual(cru['raceid'], '18525')

    def test_candidate_reporting_unit_serialization_keys_first(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1].serialize()
        self.assertEqual(cru['first'], 'Jack')

    def test_candidate_reporting_unit_serialization_keys_last(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1].serialize()
        self.assertEqual(cru['last'], 'Conway')

    def test_candidate_reporting_unit_serialization_keys_party(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1].serialize()
        self.assertEqual(cru['party'], 'Dem')

    def test_candidate_reporting_unit_serialization_keys_candidateid(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1].serialize()
        self.assertEqual(cru['candidateid'], '5266')

    def test_candidate_reporting_unit_serialization_keys_polid(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1].serialize()
        self.assertEqual(cru['polid'], '204')

    def test_candidate_reporting_unit_serialization_keys_ballotorder(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1].serialize()
        self.assertEqual(cru['ballotorder'], 1)

    def test_candidate_reporting_unit_serialization_keys_polnum(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1].serialize()
        self.assertEqual(cru['polnum'], '19601')

    def test_candidate_reporting_unit_serialization_keys_votecount(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1].serialize()
        self.assertEqual(cru['votecount'], 504)

    def test_candidate_reporting_unit_serialization_keys_winner(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1].serialize()
        self.assertEqual(cru['winner'], False)

    def test_candidate_reporting_unit_serialization_keys_incumbent(self):
        cru = self.candidate_reporting_units[(4 * 64) + 1].serialize()
        self.assertEqual(cru['incumbent'], False)

    def test_candidate_reporting_unit_serialization_order(self):
        cru = list(self.candidate_reporting_units[(4 * 64) + 1].serialize())
        self.assertEqual(
            cru,
            [
                'id',
                'raceid',
                'racetype',
                'racetypeid',
                'ballotorder',
                'candidateid',
                'description',
                'delegatecount',
                'electiondate',
                'electtotal',
                'electwon',
                'fipscode',
                'first',
                'incumbent',
                'initialization_data',
                'is_ballot_measure',
                'last',
                'lastupdated',
                'level',
                'national',
                'officeid',
                'officename',
                'party',
                'polid',
                'polnum',
                'precinctsreporting',
                'precinctsreportingpct',
                'precinctstotal',
                'eevp',
                'reportingunitid',
                'reportingunitname',
                'runoff',
                'seatname',
                'seatnum',
                'statename',
                'statepostal',
                'test',
                'resultstype',
                'uncontested',
                'votecount',
                'votepct',
                'winner'
            ]
        )

    def test_unique_ids(self):
        all_ids = list([b.id for b in self.candidate_reporting_units])
        unique_ids = set(all_ids)
        self.assertEqual(len(all_ids), len(unique_ids))
