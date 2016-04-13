import tests


class TestCandidate(tests.ElectionResultsTestCase):

    def test_number_of_candidates(self):
        self.assertEqual(len(self.candidates), 3)

    def test_candidate_object_inflation_name(self):
        c = self.candidates[0]
        self.assertEqual(type(c).__name__, 'Candidate')

    def test_candidate_object_inflation_module(self):
        c = self.candidates[0]
        self.assertEqual(c.__module__, 'elex.api.models')

    def test_candidate_attributes_first(self):
        c = self.candidates[0]
        self.assertEqual(c.first, 'Matt')

    def test_candidate_attributes_last(self):
        c = self.candidates[0]
        self.assertEqual(c.last, 'Bevin')

    def test_candidate_attributes_party(self):
        c = self.candidates[0]
        self.assertEqual(c.party, 'GOP')

    def test_candidate_attributes_candidateid(self):
        c = self.candidates[0]
        self.assertEqual(c.candidateid, '5295')

    def test_candidate_attributes_polid(self):
        c = self.candidates[0]
        self.assertEqual(c.polid, '63424')

    def test_candidate_attributes_ballotorder(self):
        c = self.candidates[0]
        self.assertEqual(c.ballotorder, 2)

    def test_candidate_attributes_polnum(self):
        c = self.candidates[0]
        self.assertEqual(c.polnum, '20103')

    def test_candidate_attributes_id(self):
        c = self.candidates[0]
        self.assertEqual(c.id, 'polid-63424')

    def test_candidate_serialization_keys_first(self):
        c = self.candidates[0].serialize()
        self.assertEqual(c['first'], 'Matt')

    def test_candidate_serialization_keys_last(self):
        c = self.candidates[0].serialize()
        self.assertEqual(c['last'], 'Bevin')

    def test_candidate_serialization_keys_party(self):
        c = self.candidates[0].serialize()
        self.assertEqual(c['party'], 'GOP')

    def test_candidate_serialization_keys_candidateid(self):
        c = self.candidates[0].serialize()
        self.assertEqual(c['candidateid'], '5295')

    def test_candidate_serialization_keys_polid(self):
        c = self.candidates[0].serialize()
        self.assertEqual(c['polid'], '63424')

    def test_candidate_serialization_keys_ballotorder(self):
        c = self.candidates[0].serialize()
        self.assertEqual(c['ballotorder'], 2)

    def test_candidate_serialization_keys_polnum(self):
        c = self.candidates[0].serialize()
        self.assertEqual(c['polnum'], '20103')

    def test_candidate_serialization_keys_uniqueid(self):
        c = self.candidates[0].serialize()
        self.assertEqual(c['id'], 'polid-63424')

    def test_candidate_serialization_order(self):
        c = list(self.candidates[0].serialize())
        self.assertEqual(
            c,
            [
                'id', 'candidateid', 'ballotorder', 'first',
                'last', 'party', 'polid', 'polnum'
            ]
        )

    def test_unique_ids(self):
        all_ids = list([b.id for b in self.candidates])
        unique_ids = set(all_ids)
        self.assertEqual(len(all_ids), len(unique_ids))
