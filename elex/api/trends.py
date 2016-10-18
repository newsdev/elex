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

    def __init__(self, trend_file=None):
        if not self.office_code or not self.api_report_id:
            raise NotImplementedError
        self.load_raw_data(self.office_code, trend_file)
        self.parties = []
        self.output_parties()

    def load_raw_data(self, office_code, trend_file=None):
        """
        Gets underlying data lists we need for parsing.
        """
        if trend_file:
            self.raw_data = self.get_ap_file(trend_file)
        else:
            self.raw_data = self.get_ap_report(office_code)

    def get_ap_file(self, path):
        """
        Get raw data file.
        """
        with open(path, 'r') as readfile:
            data = json.load(readfile)
            return data['trendtable']

    def get_ap_report(self, key, params={}):
        """
        Given a report number and a key for indexing, returns a list
        of delegate counts by party. Makes a request from the AP
        using requests. Formats that request with env vars.
        """
        reports = utils.get_reports(params=params)
        report_id = self.get_report_id(reports, key)
        if report_id:
            r = utils.api_request('/reports/{0}'.format(report_id), **params)
            return r.json()['trendtable']

    def get_report_id(self, reports, key):
        """
        Takes a delSuper or delSum as the argument and returns
        organization-specific report ID.
        """
        for report in reports:
            if (
                key == self.office_code and
                report.get('title') == self.api_report_id
            ):
                id = report.get('id').rsplit('/', 1)[-1]
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
                leading=self._parse_trend('Won', party['trend']),
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


class USSenateTrendReport(BaseTrendReport):
    """
    A trend report on the U.S. Senate.
    """
    office_code = 's'
    api_report_id = 'Trend / s / US'


class USHouseTrendReport(BaseTrendReport):
    """
    A trend report on U.S. House.
    """
    office_code = 'h'
    api_report_id = 'Trend / h / US'
