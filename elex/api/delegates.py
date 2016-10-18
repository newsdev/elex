# -*- coding: utf-8 -*-
"""
This module contains the primary :class:`DelegateLoad` class for handling a
single load of AP delegate counts and methods necessary to obtain them.
"""
import ujson as json

from elex.api import utils
from collections import OrderedDict


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
    'delegates_count': 0,
    'id': u'SD-11291',
    'd1': -1,
    'd7': 8,
    'd30': 10
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
        self.id = "%s-%s" % (self.state, self.candidateid)
        self.d1 = int(kwargs.get('d1', None).replace(',', ''))
        self.d7 = int(kwargs.get('d7', None).replace(',', ''))
        self.d30 = int(kwargs.get('d30', None).replace(',', ''))

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
            ('id', self.id),
            ('d1', self.d1),
            ('d7', self.d7),
            ('d30', self.d30)
        ))

    def __unicode__(self):
        return "%s - %s" % (self.last, self.state)


class DelegateReport(utils.UnicodeMixin):
    """
    Base class for a single load of AP delegate counts.
    d = DelegateReport()
    [z.__dict__ for z in d.candidates]
    """

    def __init__(self, **kwargs):
        self.reports = None
        self.candidate_objects = []
        self.candidates = {}
        self.load_raw_data(
            delsuper_datafile=kwargs.get('delsuper_datafile', None),
            delsum_datafile=kwargs.get('delsum_datafile', None))
        self.parse_super()
        self.parse_sum()
        self.output_candidates()

    def output_candidates(self):
        """
        Transforms our multi-layered dict of candidates / states
        into a single list of candidates at each reporting level.
        """
        for c in self.candidates.values():
            for cd in c.values():
                try:
                    self.candidate_objects.append(
                        CandidateDelegateReport(**cd)
                    )
                except TypeError:
                    pass

    def parse_sum(self):
        """
        Parses the delsum JSON produced by the AP.
        """
        for c in self.candidates.values():

            c['delegates_committed'] = None
            c['delegates_uncommitted'] = None
            for cd in c.values():
                for party in self.raw_sum_delegates:

                    for candidate in party['Cand']:
                        try:
                            if cd['candidateid']:
                                if cd['candidateid'] == candidate['cId']:
                                    cd['d1'] = candidate['d1']
                                    cd['d7'] = candidate['d7']
                                    cd['d30'] = candidate['d30']
                        except TypeError:
                            pass

                    try:
                        if cd['party'] and cd['party'] == party['pId']:
                            c['delegates_committed'] = party['dChosen']
                            c['delegates_uncommitted'] = party['dToBeChosen']
                    except TypeError:
                        pass

    def parse_super(self):
        """
        Parses the delsuper JSON produced by the AP.
        """
        for party in self.raw_super_delegates:
            for state in party['State']:
                for candidate in state['Cand']:
                    if not self.candidates.get(candidate['cId'], None):
                        self.candidates[candidate['cId']] = {}
                    if not self.candidates[candidate['cId']].get(
                        state['sId'],
                        None
                    ):
                        self.candidates[candidate['cId']][state['sId']] = {}
                    d = {
                        'superdelegates_count': int(candidate['sdTot']),
                        'party': party['pId'],
                        'party_need': int(party['dNeed']),
                        'party_total': int(party['dVotes']),
                        'state': state['sId'],
                        'candidateid': candidate['cId'],
                        'last': candidate['cName'],
                        'delegates_count': int(candidate['dTot'])
                    }
                    if state['sId'] == 'US':
                        d['level'] = 'nation'
                    else:
                        d['level'] = 'state'
                    self.candidates[candidate['cId']][state['sId']].update(d)

    def load_raw_data(self, delsuper_datafile, delsum_datafile):
        """
        Gets underlying data lists we need for parsing.
        """
        if delsum_datafile:
            self.raw_sum_delegates = self.get_ap_file(
                delsum_datafile,
                'delSum'
            )
        else:
            self.raw_sum_delegates = self.get_ap_report('delSum')

        if delsuper_datafile:
            self.raw_super_delegates = self.get_ap_file(
                delsuper_datafile,
                'delSuper'
            )
        else:
            self.raw_super_delegates = self.get_ap_report('delSuper')

    def get_ap_file(self, path, key):
        """
        Get raw data file.
        """
        with open(path, 'r') as readfile:
            data = json.load(readfile)
            return data[key]['del']

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
            return r.json()[key]['del']

        return None

    def get_report_id(self, reports, key):
        """
        Takes a delSuper or delSum as the argument and returns
        organization-specific report ID.
        """

        for report in reports:
            if (
                key == 'delSum' and
                report.get('title') == 'Delegates / delsum'
            ) or (
                key == 'delSuper' and
                report.get('title') == 'Delegates / delsuper'
            ):
                id = report.get('id').rsplit('/', 1)[-1]
                return id

        return None
