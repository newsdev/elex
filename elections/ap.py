import datetime
import json

import elections
from elections import utils


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
        return [Election(**election) for election in list(Election.get('/').json()['elections'])]

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
