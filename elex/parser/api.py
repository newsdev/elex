import datetime
import json

from dateutil import parser

import elex
from elex.parser import utils


class BaseObject(object):
    """
    Base class for most objects.
    Handy container for methods for first level
    transformation of data and AP connections.
    """

    def set_winner(self):
        """
        Translates winner: "X" into a boolean.
        """
        self.winner = False
        if self.winner == "X":
            self.winner = True

    def set_reportingunits(self):
        """
        If this race has reportingunits,
        serialize them into objects.
        """
        setattr(self, 'reportingunits', [ReportingUnit(**r) for r in self.reportingunits])

    def set_candidates(self):
        """
        If this thing (race, reportingunit) has candidates,
        serialize them into objects.
        """
        candidate_objs = []
        for c in self.candidates:
            candidate_dict = dict(c)
            if hasattr(self, 'officeid'):
                if self.officeid == u"I":
                    candidate_dict['is_ballot_position'] = True
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
        return utils.api_request(path, **params)


class Candidate(BaseObject):
    """
    Canonical reporesentation of an
    AP candidate. Note: A candidate can 
    be a person OR a ballot position.
    """
    def __init__(self, **kwargs):
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
            return "%s" % self.party
        else:
            return "%s %s (%s)" % (self.first, self.last, self.party)


class ReportingUnit(BaseObject):
    """
    Canonical representation of a single
    level of reporting. Can be 
    """
    def __init__(self, **kwargs):
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

        self.electiondate_parsed = None
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
