import tests


class TestDelegateReports(tests.TrendReportTestCase):
    """
    @TODO Not very sufficient tests
    """

    def test_us_governor_net_winners(self):
        trend = self.governor_trends.parties[0]
        self.assertEqual(trend.net_winners, '-2')

    def test_us_governor_gop_won(self):
        trend = self.governor_trends.parties[1]
        self.assertEqual(trend.won, '4')
