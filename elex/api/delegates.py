# -*- coding: utf-8 -*-
"""
This module contains the primary :class:`DelegateLoad` class for handling a single load of AP delegate counts and methods necessary to obtain them.
"""

import json
import os

import requests

from elex.api import utils


class CandidateDelegateReport(utils.UnicodeMixin):
    """
    'level': 'state',
    'party_total': 4762,
    'superdelegates_count': 0,
    'last': u'Steinberg',
    'state': u'SD',
    'candidateid': u'11291',
    'party_need': 2382,
    'party': u'Dem',
    'delegates_count': 0
    """
    def __init__(self, **kwargs):
        self.level = kwargs.get('level', None)
        self.party_total = kwargs.get('party_total', None)
        self.superdelegates_count = kwargs.get('superdelegates_count', None)
        self.last = kwargs.get('last', None)
        self.state = kwargs.get('state', None)
        self.candidateid = kwargs.get('candidateid', None)
        self.party_need = kwargs.get('party_need', None)
        self.party = kwargs.get('party', None)
        self.delegates_count = kwargs.get('delegates_count', None)
        self.id = self.candidateid

    def serialize(self):
        """
        Implements :meth:`APElection.serialize()`.
        """
        return OrderedDict((
            ('level', self.level),
            ('party_total', self.party_total),
            ('superdelegates_count', self.superdelegates_count),
            ('last', self.last),
            ('state', self.state),
            ('candidateid', self.candidateid),
            ('party_need', self.party_need),
            ('party', self.party),
            ('delegates_count', self.delegates_count),
            ('id', self.candidateid)
        ))

    def __str__(self):
        return "%s - %s" % (self.last, self.state)

class DelegateReport(utils.UnicodeMixin):
    """
    Base class for a single load of AP delegate counts.
    """
    candidates = None
    raw_super_delegates = None
    raw_sum_delegates = None

    def __init__(self, **kwargs):
        self.candidates = {}
        self.load_raw_data()
        self.parse_super()
        self.parse_sum()
        self.output_candidates()

    def output_candidates(self):
        """
        Transforms our multi-layered dict of candidates / states
        into a single list of candidates at each reporting level.
        """
        candidates = []
        for _, c in self.candidates.items():
            for __, cd in c.items():
                candidates.append(CandidateDelegateReport(**cd))
        self.candidates = list(candidates)

    def parse_sum(self):
        """
        Parses the delsum JSON produced by the AP.
        """
        for _, c in self.candidates.items():
            for __, cd in c.items():
                for party in self.raw_sum_delegates:
                    if cd['party'] == party['pId']:
                        c['delegates_committed'] = party['dChosen']
                        c['delegates_uncommitted'] = party['dToBeChosen']

    def parse_super(self):
        """
        Parses the delsuper JSON produced by the AP.
        """
        for party in self.raw_super_delegates:
            for state in party['State']:
                for candidate in state['Cand']:
                    if not self.candidates.get(candidate['cId'], None):
                        self.candidates[candidate['cId']] = {}
                    if not self.candidates[candidate['cId']].get(state['sId'], None):
                        self.candidates[candidate['cId']][state['sId']] = {}

                    self.candidates[candidate['cId']][state['sId']]['superdelegates_count'] = int(candidate['sdTot'])
                    self.candidates[candidate['cId']][state['sId']]['party'] = party['pId']
                    self.candidates[candidate['cId']][state['sId']]['party_need'] = int(party['dNeed'])
                    self.candidates[candidate['cId']][state['sId']]['party_total'] = int(party['dVotes'])
                    self.candidates[candidate['cId']][state['sId']]['state'] = state['sId']
                    self.candidates[candidate['cId']][state['sId']]['level'] = 'state'
                    if state['sId'] == "US":
                        self.candidates[candidate['cId']][state['sId']]['level'] = 'nation'
                    self.candidates[candidate['cId']][state['sId']]['candidateid'] = candidate['cId']
                    self.candidates[candidate['cId']][state['sId']]['last'] = candidate['cName']
                    self.candidates[candidate['cId']][state['sId']]['delegates_count'] = int(candidate['dTot'])

    def load_raw_data(self):
        """
        Gets underlying data lists we need for parsing.
        """
        self.raw_sum_delegates = self.get_ap_report('2db35295d17f41328b21ae1f58572bc7', 'delSum')
        self.raw_super_delegates = self.get_ap_report('6b3608587a78409698af0d3cd4748b30', 'delSuper')

    def get_ap_report(self, report_number, key, params={}):
        """
        Given a report number and a key for indexing, returns a list
        of delegate counts by party. Makes a request from the AP
        using requests. Formats that request with env vars.
        """
        base_url = os.environ.get('AP_API_BASE_URL', 'http://api.ap.org/v2/reports')
        params['apikey'] = os.environ.get('AP_API_KEY', None)
        params['format'] = 'json'
        r = requests.get(base_url + '/' + report_number, params=params)
        return dict(json.loads(r.content))[key]['del']