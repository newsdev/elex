import tests


class TestCandidate(tests.ElectionPreResultsTestCase):

    def test_number_of_candidates(self):
        self.assertEqual(len(self.candidates), 5)

    def test_candidate_attributes_party(self):
        c = self.candidates[0]
        self.assertEqual(c.party, 'Dem')
