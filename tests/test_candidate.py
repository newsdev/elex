import tests

class TestCandidate(tests.ElectionResultsTestCase):

    def test_number_of_candidates(self):
        self.assertEqual(len(self.candidates), 3)

    def test_candidate_object_inflation(self):
        c = self.candidates[0]
        self.assertEqual(type(c).__name__, 'Candidate')
        self.assertEqual(c.__module__, 'elex.parser.api')

    def test_candidate_attributes(self):
        c = self.candidates[2]
        self.assertEqual(c.first, 'Matt')
        self.assertEqual(c.last, 'Bevin')
        self.assertEqual(c.party, "GOP")
        self.assertEqual(c.candidateid, "5295")
        self.assertEqual(c.polid, "63424")
        self.assertEqual(c.ballotorder, 2)
        self.assertEqual(c.polnum, "20103")
        self.assertEqual(c.unique_id, "polid-63424")

    def test_ballot_position_attributes(self):
        c = self.ballot_positions[0]
        self.assertEqual(c.last, "Yes")
        self.assertFalse(hasattr(c, 'first'))
        self.assertEqual(c.unique_id, "polid-2")