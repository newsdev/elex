import tests

class TestCandidate(tests.ElectionResultsTestCase):

    def test_number_of_candidates(self):
        self.assertEqual(len(self.candidates), 3)

    def test_candidate_object_inflation(self):
        c = self.candidates[0]
        self.assertEqual(type(c).__name__, 'Candidate')
        self.assertEqual(c.__module__, 'elex.api.api')

    def test_candidate_attributes(self):
        c = self.candidates[2]
        self.assertEqual(c.first, 'Drew')
        self.assertEqual(c.last, 'Curtis')
        self.assertEqual(c.party, 'Ind')
        self.assertEqual(c.candidateid, '5296')
        self.assertEqual(c.polid, '64511')
        self.assertEqual(c.ballotorder, 3)
        self.assertEqual(c.polnum, '20249')
        self.assertEqual(c.unique_id, 'polid-64511')
        self.assertEqual(c.id, c.unique_id)

    def test_candidate_serialization_keys(self):
        c = self.candidates[2].serialize()
        self.assertEqual(c['first'], 'Drew')
        self.assertEqual(c['last'], 'Curtis')
        self.assertEqual(c['party'], 'Ind')
        self.assertEqual(c['candidateid'], '5296')
        self.assertEqual(c['polid'], '64511')
        self.assertEqual(c['ballotorder'], 3)
        self.assertEqual(c['polnum'], '20249')
        self.assertEqual(c['unique_id'], 'polid-64511')
        self.assertEqual(c['unique_id'], c['id'])

    def test_candidate_serialization_order(self):
        c = list(self.candidates[2].serialize())
        self.assertEqual(c, ['id','unique_id','candidateid','ballotorder','first','last','party','polid','polnum'])

    def test_unique_ids(self):
        all_ids = list([b.id for b in self.candidates])
        unique_ids = set(all_ids)

        self.assertEqual(len(all_ids), len(unique_ids))
