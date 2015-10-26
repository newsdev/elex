# -*- coding: utf-8 -*-

import datetime
import json
import os

from dateutil import parser

import elex
from elex.parser import utils


class BaseObject(object):
    """
    Base class for most objects.
    Handy container for methods for first level
    transformation of data and AP connections.
    """

    def set_state_fields_from_reportingunits(self):
        if len(self.reportingunits) > 0:
            self.statepostal = self.reportingunits[0].statepostal
            self.statename = self.reportingunits[0].statename

    def set_winner(self):
        """
        Translates winner: "X" into a boolean.
        """
        if self.winner == u"X":
            self.winner = True
        else:
            self.winner = False

    def set_reportingunits(self):
        """
        If this race has reportingunits,
        serialize them into objects.
        """
        reportingunits_obj = []
        for r in self.reportingunits:

            # Denormalize some data.
            for attr in ['raceid']:
                if hasattr(self, attr):
                    r[attr] = getattr(self, attr)

            reportingunits_obj.append(ReportingUnit(**r))
        setattr(self, 'reportingunits', reportingunits_obj)

    def set_candidates(self):
        """
        If this thing (race, reportingunit) has candidates,
        serialize them into objects.
        """
        candidate_objs = []
        for c in self.candidates:
            candidate_dict = dict(c)

            # Decide if this is a ballot position or a _real_ candidate.
            if hasattr(self, 'officeid'):
                if self.officeid == u"I":
                    candidate_dict['is_ballot_position'] = True

            # Denormalize some data.
            for attr in ['raceid', 'statepostal', 'statename', 'reportingunitid']:
                if hasattr(self, attr):
                    candidate_dict[attr] = getattr(self, attr)

            candidate_objs.append(Candidate(**candidate_dict))
        setattr(self, 'candidates', sorted(candidate_objs, key=lambda x: x.ballotorder))

    def set_dates(self, date_fields):
        for field in date_fields:
            try:
                setattr(self, field + '_parsed', parser.parse(getattr(self, field)))
            except AttributeError:
                pass

    def set_fields(self, **kwargs):
        fieldnames = self.__dict__.keys()
        for k,v in kwargs.items():
            k = k.lower().strip()
            try:
                v = unicode(v.decode('utf-8'))
            except AttributeError:
                pass
            if k in fieldnames:
                setattr(self, k, v)

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()

    @classmethod
    def get(cls, path, **params):
        """
        Farms out request to api_request.
        Could possibly handle choosing which
        parser backend to use -- API-only right now.
        Also the entry point for recording, which
        is set via environment variable.
        """
        payload = utils.api_request(path, **params)
        if os.environ.get('ELEX_RECORDING', None):
            utils.write_recording(payload)
        return payload


class Candidate(BaseObject):
    """
    Canonical reporesentation of an
    AP candidate. Note: A candidate can 
    be a person OR a ballot position.
    """
    def __init__(self, **kwargs):
        self.raceid = None
        self.statepostal = None
        self.statename = None
        self.reportingunitid = None
        self.first = None
        self.last = None
        self.party = None
        self.candidateid = None
        self.polid = None
        self.ballotorder = None
        self.polnum = None
        self.votecount = 0
        self.winner = False
        self.is_ballot_position = False

        self.set_fields(**kwargs)
        self.set_winner()

    def __unicode__(self):
        if self.is_ballot_position:
            payload = "%s" % self.party
        else:
            payload = "%s %s (%s)" % (self.first, self.last, self.party)
        if self.winner:
            payload += '✓'.decode('utf-8')
        return payload


class ReportingUnit(BaseObject):
    """
    Canonical representation of a single
    level of reporting. Can be 
    """
    def __init__(self, **kwargs):
        self.raceid = None
        self.statepostal = None
        self.statename = None
        self.level = None
        self.reportingunitname = None
        self.reportingunitid = None
        self.fipscode = None
        self.lastupdated = None
        self.precinctsreporting = 0
        self.precinctsyotal = 0
        self.precinctsreportingpct = 0.0
        self.candidates = []

        self.set_fields(**kwargs)
        self.set_dates(['lastupdated'])
        self.set_candidates()

    def __unicode__(self):
        if self.reportingunitname:
            return "%s %s (%s %% reporting)" % (self.statepostal, self.reportingunitname, self.precinctsreportingpct)
        return "%s %s (%s %% reporting)" % (self.statepostal, self.level, self.precinctsreportingpct)


class Race(BaseObject):
    """
    Canonical representation of a single
    race, which is a seat in a political geography
    within a certain election.
    """
    def __init__(self, **kwargs):
        self.test = False
        self.raceid = None
        self.statepostal = None
        self.statename = None
        self.raceType = None
        self.racetypeid = None
        self.officeid = None
        self.officename = None
        self.party = None
        self.seatname = None
        self.seatnum = None
        self.uncontested = False
        self.lastupdated = None
        self.candidates = []
        self.reportingunits = []

        self.initialization_data = False

        self.set_fields(**kwargs)
        self.set_dates(['lastupdated'])

        if self.initialization_data:
            self.set_candidates()
        else:
            self.set_reportingunits()
            self.set_state_fields_from_reportingunits()

    def __unicode__(self):
        name = self.officename
        if self.statepostal:
            name = "%s %s" % (self.statepostal, self.officename)
            if self.seatname:
                name += " %s" % self.seatname
        return name


class Election(BaseObject):
    """
    Canonical representation of an election on
    a single date.
    """
    def __init__(self, **kwargs):
        self.testresults = False
        self.liveresults = False
        self.electiondate = None
        self.is_test = False

        self.set_fields(**kwargs)
        self.set_dates(['electiondate'])

    def __unicode__(self):
        if self.is_test:
            return "TEST: %s" % self.electiondate
        else:
            return self.electiondate

    @classmethod
    def get_elections(cls):
        return [Election(**election) for election in list(Election.get('/')['elections'])]

    @classmethod
    def get_next_election(cls):
        today = datetime.datetime.now()
        next_election = None
        lowest_diff = None
        for e in Election.get_elections():
            diff = (e.electiondate_parsed - today).days
            if diff > 0:
                if not lowest_diff and not next_election:
                    next_election = e
                    lowest_diff = diff
                elif lowest_diff and next_election:
                    if diff < lowest_diff:
                        next_election = e
                        lowest_diff = diff
        return next_election

    @classmethod
    def get_races(cls, date_string, **kwargs):
        """
        Convenience method for fetching races by election date.
        Accepts an AP formatting date string, e.g., YYYY-MM-DD.
        Accepts any number of URL params as kwargs.
        """

        # With `omitResults=True`, the API will return initialization data.
        if kwargs.get('omitResults', None):
            payload = []
            for r in Election.get('/%s' % date_string, **kwargs)['races']:
                r['initialization_data'] = True
                race = Race(**r)
                payload.append(race)
            return payload
        return [Race(**r) for r in Election.get('/%s' % date_string, **kwargs)['races']]
