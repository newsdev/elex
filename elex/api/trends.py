# -*- coding: utf-8 -*-
"""
Balance of power "trend" reports that summarize by party the national count of governors, senators and House members.
"""
from __future__ import unicode_literals

import ujson as json

from elex.api import utils
from collections import OrderedDict


class TrendParty(utils.UnicodeMixin):
    """
    The status of a political party recorded in a trend report.
    """
    def __init__(self, **kwargs):
        self.party = kwargs.get("party", None)
        self.office = kwargs.get("office", None)

        self.won = kwargs.get("won", None)
        self.leading = kwargs.get("leading", None)
        self.holdovers = kwargs.get("holdovers", None)
        self.winning_trend = kwargs.get("winning_trend", None)
        self.current = kwargs.get("current", None)
        self.insufficient_vote = kwargs.get("insufficient_vote", None)

        self.net_winners = kwargs.get("net_winners", None)
        self.net_leaders = kwargs.get("net_leaders", None)

    def serialize(self):
        """
        Implements :meth:`APElection.serialize()`.
        """
        return OrderedDict((
            ('party', self.party),
            ('office', self.office),
            ('won', self.won),
            ('leading', self.leading),
            ('holdovers', self.holdovers),
            ('winning_trend', self.winning_trend),
            ('current', self.current),
            ('insufficient_vote', self.insufficient_vote),
            ('net_winners', self.net_winners),
            ('net_leaders', self.net_leaders),
        ))

    def __unicode__(self):
        return "%s - %s" % (self.office, self.party)


class BaseTrendReport(utils.UnicodeMixin):
    """
    A base class for retrieving trend reports from the AP API.
    """
    office_code = None
    api_report_id = 'Trend / g / US'

    def __init__(self, *args, **kwargs):
        if not self.office_code or not self.api_report_id:
            raise NotImplementedError

        if len(args):
            # Shim to support former method signature.
            defaults['trendfile'] = args[0] if len(args) > 0 else None
            defaults['testresults'] = args[1] if len(args) > 1 else False

        self.testresults = kwargs.get('testresults', defaults['testresults'])

        self.electiondate = kwargs.get('electiondate', None)
        self.api_key = kwargs.get('api_key', None)
        self.trendfile = kwargs.get('trend_file', defaults['trendfile'])

        self.load_raw_data()

        if self.raw_data is None:
            # Should we raise an error here, rather than creating an object
            # that contains no actual results?
            self.parties = None
        else:
            self.parties = []
            self.output_parties()

    def format_api_request_params(self):
        params = {}

        if self.api_key is not None:
            params['apiKey'] = self.api_key

        return params

    def load_raw_data(self):
        """
        Gets underlying data lists we need for parsing.
        """
        if self.trendfile:
            self.raw_data = self.get_ap_file()
        else:
            self.raw_data = self.get_ap_report(
                params={
                    'test': self.testresults,
                    **self.format_api_request_params(),
                }
            )

    def get_ap_file(self):
        """
        Get raw data file.
        """
        with open(self.trendfile, 'r') as readfile:
            data = json.load(readfile)
            return data['trendtable']

    def get_ap_report(self, params={}):
        """
        Given a report number, returns a list of counts by party.
        Makes a request from the AP using requests. Formats that request
        with env vars.
        """
        reports = utils.get_reports(params=params)
        report_id = self.get_report_id(reports)
        if report_id:
            r = utils.api_request(
                '/reports/{0}'.format(report_id),
                **self.format_api_request_params()
            )
            return r.json()['trendtable']

    def get_report_id(self, reports):
        """
        Takes a delSuper or delSum as the argument and returns
        organization-specific report ID.
        """
        matching_reports = [
            report for report in reports if report.get('title') in [
                self.api_report_id,
                self.api_test_report_id
            ]
        ]

        if self.electiondate:  # Can also use the explicit 'if is not none'.
            matching_reports = [
                report for report in matching_reports
                if report.get('electionDate') == self.electiondate
            ]

        if matching_reports:
            id = matching_reports[0].get('id').rsplit('/', 1)[-1]
            return id

        return None

    def output_parties(self):
        """
        Parse the raw data on political parties returned by the API, converts them into objects
        and assigns them to the object's ``parties`` attribute.
        """
        for party in self.raw_data['party']:
            obj = TrendParty(
                party=party['title'],
                office=self.raw_data['office'],
                won=self._parse_trend('Won', party['trend']),
                leading=self._parse_trend('Leading', party['trend']),
                holdovers=self._parse_trend('Holdovers', party['trend']),
                winning_trend=self._parse_trend('Winning Trend', party['trend']),
                current=self._parse_trend('Current', party['trend']),
                insufficient_vote=self._parse_trend('InsufficientVote', party['trend']),
                net_winners=self._parse_trend('Winners', party['NetChange']['trend']),
                net_leaders=self._parse_trend('Leaders', party['NetChange']['trend']),
            )
            self.parties.append(obj)

    def _parse_trend(self, key, trend_list):
        """
        Parses and returns the specified value from a list of trend dictionaries.

        The source AP data, which should be passed in as ``trend_list``, looks like this:

            [
             {u'Won': u'0'},
             {u'Leading': u'0'},
             {u'Holdovers': u'1'},
             {u'Winning Trend': u'1'},
             {u'Current': u'1'},
             {u'InsufficientVote': u'0'}
            ]

        Submit one of the keys listed there (i.e. Won or Leading) and its value will be returned.

            self._parse_trend('Won', trend_list)
        """
        return next(d for d in trend_list if key in d)[key]

    def __unicode__(self):
        return self.office_code


class USGovernorTrendReport(BaseTrendReport):
    """
    A trend report on U.S. governors.
    """
    office_code = 'g'
    api_report_id = 'Trend / g / US'
    api_test_report_id = 'Trend / g / test / US'


class USSenateTrendReport(BaseTrendReport):
    """
    A trend report on the U.S. Senate.
    """
    office_code = 's'
    api_report_id = 'Trend / s / US'
    api_test_report_id = 'Trend / s / test / US'


class USHouseTrendReport(BaseTrendReport):
    """
    A trend report on U.S. House.
    """
    office_code = 'h'
    api_report_id = 'Trend / h / US'
    api_test_report_id = 'Trend / h / test / US'
