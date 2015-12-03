import tests

class TestBallotPosition(tests.ElectionResultsTestCase):

    def test_number_of_ballot_measure_objects(self):
        self.assertEqual(len(self.ballot_measures), 8)

    def test_ballot_measure_inflation(self):
        bp = self.ballot_measures[0]
        self.assertEqual(type(bp).__name__, 'BallotMeasure')
        self.assertEqual(bp.__module__, 'elex.parser.api')

    def test_ballot_measure_attributes(self):
        c = self.ballot_measures[0]
        self.assertEqual(c.last, "Yes")
        self.assertFalse(hasattr(c, 'first'))
        self.assertEqual(c.unique_id, "polid-2")

    def test_ballot_measure_serialization_keys(self):
        c = self.ballot_measures[0].serialize()
        self.assertEqual(c['last'], "Yes")
        self.assertEqual(c['unique_id'], "polid-2")

    def test_ballot_measure_serialization_order(self):
        c = list(self.ballot_measures[0].serialize())
        self.assertEqual(c, ['id','unique_id','candidateid','ballotorder','description','last','polid','polnum','seatname'])