import json
import tests
from elex.api import USHouseTrendReport


try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


TREND_REPORT_DATA_FILES = {
    '5913efb0d26041c29db4e5e9de4f23d4': '20161210_gov_trends.json',
    '54d6adeb12c14c948f84598cbccb6f84': '20161210_house_trends.json',
    'f5afcfd0b6fe4dfc9a937e46939b7fde': '20161210_senate_trends.json',

    'cf1f265d59e84fc8878bea929483d5f5': '20161108_house_trends.json',
    'c31e3ee20ddd4854803f196a4f3a2321': '20161108_gov_trends.json',
    '9f8b8120732844a8853dd84ad13b8735': '20161108_senate_trends.json',

    '7f9736cbb85643be900677f08f0880fb': '20121106_gov_trends.json',
    '79a6d01ce88f4efca7bf954d3c98d1ef': '20121106_house_trends.json',
    '2831ab7043e24c68875d213cd5bf1d3e': '20121106_senate_trends.json',
}


class MockedResponse(object):
    def __init__(self, status=200, json_body={}):
        self.ok = True if status == 200 else False

        self.json_body = json_body

    def json(self):
        return self.json_body


def patched_api_request(url, **params):
    """"""
    if (url != '/reports'):
        report_id = url.lstrip('/reports/')
        report_filepath = 'tests/data/%s' % TREND_REPORT_DATA_FILES[report_id]

        with open(report_filepath, 'r') as report_file:
            report_json = json.load(report_file)

        return MockedResponse(json_body=report_json)

    report_list_filepath = 'tests/data/00000000_trend_report_list.json'

    with open(report_list_filepath, 'r') as report_list_file:
        report_list = json.load(report_list_file)

    return MockedResponse(json_body=report_list)


def compare_trend_reports(control_report, observed_report):
        """
        Compare two trend reports' serialized dicts.
        """
        control_parties = {_.party: _ for _ in control_report}
        observed_parties = {_.party: _ for _ in observed_report}

        report_facets_match = []

        for party_slug, control_party_obj in control_parties.items():
            control_party = control_party_obj.serialize()
            observed_party = observed_parties[party_slug].serialize()

            for trend_facet in control_party.keys():
                report_facets_match.append(
                    control_party[trend_facet] == observed_party[trend_facet]
                )

        return all(report_facets_match)


class TestBalanceOfPowerReports(tests.TrendReportTestCase):
    """
    @TODO Not very sufficient tests
    """
    def test_us_governor_net_winners(self):
        trend = self.governor_trends.parties[0]
        self.assertEqual(trend.net_winners, '-2')

    def test_us_governor_dem_won(self):
        trend = self.governor_trends.parties[0]
        self.assertEqual(trend.won, '6')

    def test_us_governor_dem_leading(self):
        trend = self.governor_trends.parties[0]
        self.assertEqual(trend.leading, '0')

    def test_us_governor_gop_won(self):
        trend = self.governor_trends.parties[1]
        self.assertEqual(trend.won, '4')

    def test_us_governor_gop_leading(self):
        trend = self.governor_trends.parties[1]
        self.assertEqual(trend.leading, '0')

    def test_us_governor_other_won(self):
        trend = self.governor_trends.parties[2]
        self.assertEqual(trend.won, '0')

    def test_us_governor_other_leading(self):
        trend = self.governor_trends.parties[2]
        self.assertEqual(trend.leading, '0')

    @patch('elex.api.utils.api_request', side_effect=patched_api_request)
    def test_unset_date_gets_latest_matching_report(self, patched_fn):
        control_trend_file = 'tests/data/20161210_house_trends.json'
        control_trend = USHouseTrendReport(control_trend_file).parties

        observed_trend = USHouseTrendReport().parties

        self.assertTrue(compare_trend_reports(control_trend, observed_trend))

    @patch('elex.api.utils.api_request', side_effect=patched_api_request)
    def test_set_date_gets_correct_report(self, patched_fn):
        control_trend_file = 'tests/data/20121106_house_trends.json'
        control_trend = USHouseTrendReport(control_trend_file).parties

        mismatch_trend_file = 'tests/data/20161210_house_trends.json'
        mismatch_trend = USHouseTrendReport(mismatch_trend_file).parties

        observed_trend = USHouseTrendReport(electiondate='2012-11-06').parties

        self.assertTrue(compare_trend_reports(control_trend, observed_trend))

        self.assertFalse(compare_trend_reports(mismatch_trend, observed_trend))
