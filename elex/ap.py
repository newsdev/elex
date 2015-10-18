import datetime
import json

import elex
from elex import utils


class Candidate(utils.BaseObject):

    def __init__(self, **kwargs):
        self.first = None
        self.last = None
        self.party = None
        self.candidateid = None
        self.polid = None
        self.ballotorder = None
        self.polNum = None

        self.is_ballot_position = False

        self.set_fields(**kwargs)

    def __unicode__(self):
        if self.is_ballot_position:
            return "%s" % self.party
        else:
            return "%s %s (%s)" % (self.first, self.last, self.party)


class Race(utils.BaseObject):

    def __init__(self, **kwargs):
        self.raceid = None
        self.statepostal = None
        self.racetypeid = None
        self.officeid = None
        self.officename = None
        self.party = None
        self.seatname = None
        self.seatnum = None
        self.uncontested = False
        self.lastupdated = None
        self.candidates = []

        self.set_fields(**kwargs)
        self.set_dates(['lastupdated'])
        self.set_candidates()

    def __unicode__(self):
        name = "%s %s" % (self.statepostal, self.officename)
        if self.seatname:
            name += " %s" % self.seatname
        return name

    def set_candidates(self):
        candidate_objs = []
        for c in self.candidates:
            candidate_dict = dict(c)
            if self.officename in [u"Proposition"]:
                candidate_dict['is_ballot_position'] = True
            candidate_objs.append(Candidate(**candidate_dict))
        setattr(self, 'candidates', sorted(candidate_objs, key=lambda x: x.ballotorder))


class Election(utils.BaseObject):

    def __init__(self, **kwargs):
        self.testresults = False
        self.liveresults = False
        self.electiondate = None

        self.electiondate_parsed = None
        self.is_test = False

        self.set_fields(**kwargs)
        self.set_dates(['electiondate'])
        self.set_is_test()

    def __unicode__(self):
        if self.is_test:
            return "TEST: %s" % self.electiondate
        else:
            return self.electiondate

    def set_is_test(self):
        """
        Why do they have two flags here?
        Can something be both test/live or neither test/live?
        """
        if self.testresults == False and self.liveresults == True:
            setattr(self, 'is_test', False)
        else:
            setattr(self, 'is_test', True)

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

    def get_races(self):
        return [Race(**r) for r in Election.get('/%s' % self.electiondate)['races']]
