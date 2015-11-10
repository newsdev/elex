import tests

class TestBallotPosition(tests.ElectionResultsTestCase):

    def test_number_of_ballot_position_objects(self):
        self.assertEqual(len(self.ballot_positions), 8)

    def test_ballot_position_inflation(self):
        bp = self.ballot_positions[0]
        self.assertEqual(type(bp).__name__, 'BallotPosition')
        self.assertEqual(bp.__module__, 'elex.parser.api')