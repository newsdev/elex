import unittest

from elex.api import Election, DelegateReport, USGovernorTrendReport, USHouseTrendReport, USSenateTrendReport, utils
from time import sleep

API_MESSAGE = "We require that you export AP_API_KEY in your environment in order to test AP connectivity."


class DelegateReportTestCase(unittest.TestCase):
    delsuper_datafile = 'tests/data/20160118_delsuper.json'
    delsum_datafile = 'tests/data/20160118_delsum.json'

    def setUp(self, **kwargs):
        d = DelegateReport(
            delsuper_datafile=self.delsuper_datafile,
            delsum_datafile=self.delsum_datafile
        )
        self.delegate_reports = d.candidate_objects


class TrendReportTestCase(unittest.TestCase):
    governor_file = 'tests/data/20160818_gov_trends.json'
    house_file = 'tests/data/20160818_house_trends.json'
    senate_file = 'tests/data/20160818_senate_trends.json'

    def setUp(self, **kwargs):
        self.governor_trends = USGovernorTrendReport(self.governor_file)
        self.house_trends = USHouseTrendReport(self.house_file)
        self.senate_trends = USSenateTrendReport(self.senate_file)


class ElectionResultsParseIdsTestCase(unittest.TestCase):
    data_url = 'tests/data/20151103_national.json'

    def setUp(self, **kwargs):
        e = Election(
            datafile=self.data_url,
            testresults=False,
            liveresults=True,
            is_test=False,
            raceids=['7583']
        )
        self.election = e
        self.resultslevel = e.resultslevel
        self.raw_races = e.get_raw_races()
        self.race_objs = e.get_race_objects(self.raw_races)
        self.ballot_measures = e.ballot_measures
        self.candidate_reporting_units = e.candidate_reporting_units
        self.candidates = e.candidates
        self.races = e.races
        self.reporting_units = e.reporting_units
        self.results = e.results


class ElectionResultsTestCase(unittest.TestCase):
    data_url = 'tests/data/20151103_national.json'

    def setUp(self, **kwargs):
        e = Election(
            datafile=self.data_url,
            testresults=False,
            liveresults=True,
            is_test=False
        )
        self.election = e
        self.resultslevel = e.resultslevel
        self.raw_races = e.get_raw_races()
        self.race_objs = e.get_race_objects(self.raw_races)
        self.ballot_measures = e.ballot_measures
        self.candidate_reporting_units = e.candidate_reporting_units
        self.candidates = e.candidates
        self.races = e.races
        self.reporting_units = e.reporting_units
        self.results = e.results


class ElectionPreResultsTestCase(ElectionResultsTestCase):
    data_url = 'tests/data/20161100_national_pre_results.json'


class ElectionDistrictResultsTestCase(unittest.TestCase):
    data_url = 'tests/data/20160201_district_results.json'

    def setUp(self, **kwargs):
        e = Election(
            electiondate='2016-02-01',
            datafile=self.data_url,
            testresults=False,
            liveresults=True,
            is_test=False,
            resultslevel='district'
        )
        self.resultslevel = e.resultslevel
        self.raw_races = e.get_raw_races()
        self.race_objs = e.get_race_objects(self.raw_races)
        self.ballot_measures = e.ballot_measures
        self.candidate_reporting_units = e.candidate_reporting_units
        self.candidates = e.candidates
        self.races = e.races
        self.reporting_units = e.reporting_units
        self.results = e.results


class NetworkTestCase(unittest.TestCase):
    def api_request(self, *args, **kwargs):
        response = utils.api_request(*args, **kwargs)
        sleep(10)
        return response
