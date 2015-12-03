# -*- coding: utf-8 -*-
"""
This module contains the primary :class:`Election` class, as well as model classes :class:`Candidate`, :class:`BallotMeasure`, :class:`CandidateReportingUnit`, :class:`ReportingUnit`, :class:`Race` model classes, and :class:`APElection` which provides utility methods common to all AP API access.

"""

import datetime
import json

from dateutil import parser as dateutil_parser
from collections import OrderedDict

from elex.api import maps
from elex.api import utils

PCT_PRECISION = 6


class APElection(object):
    """
    Base class for most objects.
    Handy container for methods for first level
    transformation of data and AP connections.
    """

    def set_state_fields_from_reportingunits(self):
        """
        Set state fields.
        """
        if len(self.reportingunits) > 0:
            setattr(self, 'statepostal', self.reportingunits[0].statepostal)
            setattr(self, 'statename', maps.STATE_ABBR[self.statepostal])

    def set_winner_runoff(self):
        """
        Translates winner: "X" or "R" into a booleans on winner and runoff.
        """
        if self.winner == u'X':
            setattr(self, 'winner', True)
            setattr(self, 'runoff', False)
        elif self.winner == u'R':
            setattr(self, 'runoff', True)
            setattr(self, 'winner', True)
        else:
            setattr(self, 'runoff', False)
            setattr(self, 'winner', False)

    def set_reportingunits(self):
        """
        Set reporting units.

        If this race has reportingunits,
        serialize them into objects.
        """
        reportingunits_obj = []
        for r in self.reportingunits:
            reportingunit_dict = dict(r)

            # Don't obliterate good data with possibly empty fields.
            SKIP_FIELDS = ['candidates', 'statepostal', 'statename']

            for k, v in self.__dict__.items():
                if k not in SKIP_FIELDS:
                    reportingunit_dict[k] = v

            obj = ReportingUnit(**reportingunit_dict)

            reportingunits_obj.append(obj)
        setattr(self, 'reportingunits', reportingunits_obj)

    def set_polid(self):
        """
        Set politication id.

        If `polid` is zero, set to `None`.
        """
        if self.polid == "0":
            self.polid = None

    def set_reportingunitids(self):
        """
        Set reporting unit ID.

        Per Tracy / AP developers, if the level is
        "state", the reportingunitid is always 1.
        """
        if not self.reportingunitid:
            if self.level == "state":
                setattr(self, 'reportingunitid', "1")

    def set_candidates(self):
        """
        Set candidates.

        If this thing (race, reportingunit) has candidates,
        serialize them into objects.
        """
        candidate_objs = []
        for c in self.candidates:
            candidate_dict = dict(c)

            for k, v in self.__dict__.items():
                candidate_dict[k] = v

            if hasattr(self, 'officeid'):
                if getattr(self, 'officeid') == 'I':
                    candidate_dict['is_ballot_measure'] = True

            if hasattr(self, 'statepostal'):
                if getattr(self, 'statepostal') != None:
                    candidate_dict['statename'] = maps.STATE_ABBR[getattr(self, 'statepostal')]

            obj = CandidateReportingUnit(**candidate_dict)
            candidate_objs.append(obj)
        setattr(self, 'candidates', sorted(candidate_objs, key=lambda x: x.ballotorder))

    def serialize(self):
        """
        Serialize the object. Should be implemented in all classes that inherit from
        :class:`APElection`.

        Should return an `OrderedDict <https://docs.python.org/2/library/collections.html#ordereddict-objects>`_.
        """
        raise NotImplementedError

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()


class Candidate(APElection):
    """
    Canonical representation of a
    candidate. Should be globally unique
    for this election, across races.
    """
    def __init__(self, **kwargs):
        """
        :param id:
            Global identifier.
        :param unique_id:
            Unique identifier.
        :param candidateid:
            Candidate ID (raw AP).
        :param first:
            First name.
        :param last:
            Last name.
        :param party:
            Party.
        :param polid:
            Politician ID.
        :param polnum:
            Politician number.
        """
        self.id = None
        self.unique_id = None
        self.ballotorder = kwargs.get('ballotorder', None)
        self.candidateid = kwargs.get('candidateid', None)
        self.first = kwargs.get('first', None)
        self.last = kwargs.get('last', None)
        self.party = kwargs.get('party', None)
        self.polid = kwargs.get('polid', None)
        self.polnum = kwargs.get('polnum', None)

        self.set_polid()
        self.set_unique_id()
        self.set_id_field()

    def serialize(self):
        """
        Implements :meth:`APElection.serialize()`.
        """
        return OrderedDict((
            ('id', self.id),
            ('unique_id', self.unique_id),
            ('candidateid', self.candidateid),
            ('ballotorder', self.ballotorder),
            ('first', self.first),
            ('last', self.last),
            ('party', self.party),
            ('polid', self.polid),
            ('polnum', self.polnum),
        ))

    def set_unique_id(self):
        """
        Generate and set unique id.

        Candidate IDs are not globally unique.
        AP National Politian IDs (NPIDs or polid)
        are unique, but only national-level
        candidates have them; everyone else gets '0'.
        The unique key, then, is the NAME of the ID
        we're using and then the ID itself.
        Verified this is globally unique with Tracy.
        """
        if self.polid:
            self.unique_id = 'polid-{0}'.format(self.polid)
        else:
            self.unique_id = 'polnum-{0}'.format(self.polnum)

    def set_id_field(self):
        """
        Set id to `<unique_id>`.
        """
        self.id = self.unique_id


class BallotMeasure(APElection):
    """
    Canonical representation of a ballot measure.

    Ballot measures are similar to :class:`Candidate`s, but represent a position on a ballot such as
    "In favor of" or "Against" for ballot measures such as a referendum.
    """
    def __init__(self, **kwargs):
        """
        :param id:
            Global identifier.
        :param unique_id:
            Unique identifier.
        :param ballotorder:
            Order on ballot (e.g. first, second, etc).
        :param candidateid:
            Candidate idenfitier (raw AP).
        :param description:
            Description.
        :param last:
            ???
        :param polid:
            Politician ID.
        :param polnum:
            Politician number.
        :param seatname:
            Seat name.
        """
        self.id = None
        self.unique_id = None
        self.ballotorder = kwargs.get('ballotorder', None)
        self.candidateid = kwargs.get('candidateid', None)
        self.description = kwargs.get('description', None)
        self.last = kwargs.get('last', None)
        self.polid = kwargs.get('polid', None)
        self.polnum = kwargs.get('polnum', None)
        self.seatname = kwargs.get('seatname', None)

        self.set_polid()
        self.set_unique_id()
        self.set_id_field()

    def serialize(self):
        """
        Implements :meth:`APElection.serialize()`.
        """
        return OrderedDict((
            ('id', self.id),
            ('unique_id', self.unique_id),
            ('candidateid', self.candidateid),
            ('ballotorder', self.ballotorder),
            ('description', self.description),
            ('last', self.last),
            ('polid', self.polid),
            ('polnum', self.polnum),
            ('seatname', self.seatname),
        ))

    def set_unique_id(self):
        """
        Generate and set unique id.

        Candidate IDs are not globally unique.
        AP National Politian IDs (NPIDs or polid)
        are unique, but only national-level
        candidates have them; everyone else gets '0'.
        The unique key, then, is the NAME of the ID
        we're using and then the ID itself.
        Verified this is globally unique with Tracy.
        """
        self.unique_id = self.candidateid

    def set_id_field(self):
        """
        Set id to `<unique_id>`.
        """
        self.id = self.unique_id

class CandidateReportingUnit(APElection):
    """
    Canonical reporesentation of an
    AP candidate. Note: A candidate can 
    be a person OR a ballot measure.
    """
    def __init__(self, **kwargs):
        self.id = None
        self.unique_id = None
        self.first = kwargs.get('first', None)
        self.last = kwargs.get('last', None)
        self.party = kwargs.get('party', None)
        self.candidateid = kwargs.get('candidateID', None)
        self.polid = kwargs.get('polID', None)
        self.ballotorder = kwargs.get('ballotOrder', None)
        self.polnum = kwargs.get('polNum', None)
        self.votecount = kwargs.get('voteCount', 0)
        self.votepct = kwargs.get('votePct', 0.0)
        self.winner = False
        self.runoff = False
        self.is_ballot_measure = kwargs.get('is_ballot_measure', None)
        self.level = kwargs.get('level', None)
        self.reportingunitname = kwargs.get('reportingunitname', None)
        self.reportingunitid = kwargs.get('reportingunitid', None)
        self.fipscode = kwargs.get('fipscode', None)
        self.lastupdated = kwargs.get('lastupdated', None)
        self.precinctsreporting = kwargs.get('precinctsreporting', 0)
        self.precinctstotal = kwargs.get('precinctstotal', 0)
        self.precinctsreportingpct = kwargs.get('precinctsreportingpct', 0.0)
        self.uncontested = kwargs.get('uncontested', False)
        self.test = kwargs.get('test', False)
        self.raceid = kwargs.get('raceid', None)
        self.statepostal = kwargs.get('statepostal', None)
        self.statename = kwargs.get('statename', None)
        self.racetype = kwargs.get('racetype', None)
        self.racetypeid = kwargs.get('racetypeid', None)
        self.officeid = kwargs.get('officeid', None)
        self.officename = kwargs.get('officename', None)
        self.seatname = kwargs.get('seatname', None)
        self.description = kwargs.get('description', None)
        self.seatnum = kwargs.get('seatnum', None)
        self.initialization_data = kwargs.get('initialization_data', None)
        self.national = kwargs.get('national', False)
        self.incumbent = kwargs.get('incumbent', False)

        self.set_winner_runoff()
        self.set_polid()
        self.set_unique_id()
        self.set_id_field()

    def set_id_field(self):
        """
        Set id to `<raceid>-<uniqueid>-<reportingunitid>`.
        """
        self.id = "%s-%s-%s" % (self.raceid, self.unique_id, self.reportingunitid)

    def set_unique_id(self):
        """
        Generate and set unique id.

        Candidate IDs are not globally unique.
        AP National Politian IDs (NPIDs or polid)
        are unique, but only national-level
        candidates have them; everyone else gets '0'.
        The unique key, then, is the NAME of the ID
        we're using and then the ID itself.
        Verified this is globally unique with Tracy.
        """
        if not self.is_ballot_measure:
            if self.polid:
                self.unique_id = 'polid-{0}'.format(self.polid)
            else:
                self.unique_id = 'polnum-{0}'.format(self.polnum)
        else:
            self.unique_id = self.candidateid

    def serialize(self):
        """
        Implements :meth:`APElection.serialize()`.
        """
        return OrderedDict((
            ('id', self.id),
            ('unique_id', self.unique_id),
            ('raceid', self.raceid),
            ('racetype', self.racetype),
            ('racetypeid', self.racetypeid),
            ('ballotorder', self.ballotorder),
            ('candidateid', self.candidateid),
            ('description', self.description),
            ('fipscode', self.fipscode),
            ('first', self.first),
            ('incumbent', self.incumbent),
            ('initialization_data', self.initialization_data),
            ('is_ballot_measure', self.is_ballot_measure),
            ('last', self.last),
            ('lastupdated', self.lastupdated),
            ('level', self.level),
            ('national', self.national),
            ('officeid', self.officeid),
            ('officename', self.officename),
            ('party', self.party),
            ('polid', self.polid),
            ('polnum', self.polnum),
            ('precinctsreporting', self.precinctsreporting),
            ('precinctsreportingpct', self.precinctsreportingpct),
            ('precinctstotal', self.precinctstotal),
            ('reportingunitid', self.reportingunitid),
            ('reportingunitname', self.reportingunitname),
            ('runoff', self.runoff),
            ('seatname', self.seatname),
            ('seatnum', self.seatnum),
            ('statename', self.statename),
            ('statepostal', self.statepostal),
            ('test', self.test),
            ('uncontested', self.uncontested),
            ('votecount', self.votecount),
            ('votepct', round(self.votepct, PCT_PRECISION)),
            ('winner', self.winner),
        ))


    def __unicode__(self):
        if self.is_ballot_measure:
            payload = "%s" % self.party
        else:
            payload = "%s %s (%s)" % (self.first, self.last, self.party)
        if self.winner:
            payload += ' (w)'
        return payload


class ReportingUnit(APElection):
    """
    Canonical representation of a single
    level of reporting.
    """
    def __init__(self, **kwargs):
        self.statepostal = kwargs.get('statePostal', None)
        self.statename = kwargs.get('stateName', None)
        self.level = kwargs.get('level', None)
        self.reportingunitname = kwargs.get('reportingunitName', None)
        self.reportingunitid = kwargs.get('reportingunitID', None)
        self.fipscode = kwargs.get('fipsCode', None)
        self.lastupdated = kwargs.get('lastUpdated', None)
        self.precinctsreporting = kwargs.get('precinctsReporting', 0)
        self.precinctstotal = kwargs.get('precinctsTotal', 0)
        self.precinctsreportingpct = kwargs.get('precinctsReportingPct', 0.0)
        self.uncontested = kwargs.get('uncontested', False)
        self.test = kwargs.get('test', False)
        self.raceid = kwargs.get('raceid', None)
        self.racetype = kwargs.get('racetype', None)
        self.racetypeid = kwargs.get('racetypeid', None)
        self.officeid = kwargs.get('officeid', None)
        self.officename = kwargs.get('officename', None)
        self.seatname = kwargs.get('seatname', None)
        self.description = kwargs.get('description', None)
        self.seatnum = kwargs.get('seatnum', None)
        self.initialization_data = kwargs.get('initialization_data', False)
        self.national = kwargs.get('national', False)
        self.candidates = kwargs.get('candidates', [])
        self.votecount = kwargs.get('votecount', 0)

        self.set_level()
        self.pad_fipscode()
        self.set_reportingunitids()
        self.set_candidates()
        self.set_candidate_votepct()
        self.set_id_field()
        self.set_votecount()

    def __unicode__(self):
        if self.reportingunitname:
            return "%s %s (%s %% reporting)" % (self.statepostal, self.reportingunitname, self.precinctsreportingpct)
        return "%s %s (%s %% reporting)" % (self.statepostal, self.level, self.precinctsreportingpct)

    def pad_fipscode(self):
        if self.fipscode:
            self.fipscode = self.fipscode.zfill(5)

    def set_level(self):
        """
        New England states report at the township level.
        Every other state reports at the county level.
        So, change the level from 'subunit' to the 
        actual level name, either 'state' or 'township'.
        """
        if self.statepostal in maps.FIPS_TO_STATE.keys():
            if self.level == 'subunit':
                self.level = 'township'
        if self.level == 'subunit':
            self.level = 'county'

    def set_id_field(self):
        """
        Set id to `<reportingunitid>`.
        """
        self.id = self.reportingunitid

    def set_votecount(self):
        """
        Set vote count.
        """
        if not self.uncontested:
            for c in self.candidates:

                # This would have broken if c.level != 'subunit' because we are now
                # annotating with the actual subunit name, e.g., state, county or township.
                self.votecount = sum([c.votecount for c in self.candidates if c.level == "state"])
        else:
            self.votecount = None

    def set_candidate_votepct(self):
        """
        Set vote percentage for each candidate.
        """
        if not self.uncontested:
            for c in self.candidates:
                if c.level != 'subunit':
                    try:
                        c.votepct = float(c.votecount) / float(self.votecount)
                    except ZeroDivisionError:
                        pass

    def serialize(self):
        """
        Implements :meth:`APElection.serialize()`.
        """
        return OrderedDict((
            ('id', self.id),
            ('reportingunitid', self.reportingunitid),
            ('reportingunitname', self.reportingunitname),
            ('description', self.description),
            ('fipscode', self.fipscode),
            ('initialization_data', self.initialization_data),
            ('lastupdated', self.lastupdated),
            ('lastupdated', self.lastupdated),
            ('level', self.level),
            ('national', self.national),
            ('officeid', self.officeid),
            ('officename', self.officename),
            ('precinctsreporting', self.precinctsreporting),
            ('precinctsreportingpct', self.precinctsreportingpct),
            ('precinctstotal', self.precinctstotal),
            ('raceid', self.raceid),
            ('racetype', self.racetype),
            ('racetypeid', self.racetypeid),
            ('seatname', self.seatname),
            ('seatnum', self.seatnum),
            ('statename', self.statename),
            ('statename', self.statename),
            ('statepostal', self.statepostal),
            ('statepostal', self.statepostal),
            ('test', self.test),
            ('uncontested', self.uncontested),
            ('votecount', self.votecount),
        ))


class Race(APElection):
    """
    Canonical representation of a single
    race, which is a seat in a political geography
    within a certain election.
    """
    def __init__(self, **kwargs):
        self.statepostal = kwargs.get('statePostal', None)
        self.statename = kwargs.get('stateName', None)
        self.test = kwargs.get('test', False)
        self.raceid = kwargs.get('raceID', None)
        self.racetype = kwargs.get('raceType', None)
        self.racetypeid = kwargs.get('raceTypeID', None)
        self.officeid = kwargs.get('officeID', None)
        self.officename = kwargs.get('officeName', None)
        self.party = kwargs.get('party', None)
        self.seatname = kwargs.get('seatName', None)
        self.description = kwargs.get('description', None)
        self.seatnum = kwargs.get('seatNum', None)
        self.uncontested = kwargs.get('uncontested', False)
        self.lastupdated = kwargs.get('lastUpdated', None)
        self.initialization_data = kwargs.get('initialization_data', False)
        self.national = kwargs.get('national', False)
        self.candidates = kwargs.get('candidates', [])
        self.reportingunits = kwargs.get('reportingUnits', [])

        self.set_id_field()

        if self.initialization_data:
            self.set_candidates()
        else:
            self.set_reportingunits()
            self.set_state_fields_from_reportingunits()
            self.set_new_england_counties()

    def set_new_england_counties(self):
        """
        Create new CandidateReportingUnits for each New England county that
        rolls up vote counts and precinct counts / pcts from each
        township under that county.
        """

        if self.statepostal in maps.FIPS_TO_STATE.keys():
            results = {}
            for ru in [r for r in self.reportingunits if r.level == 'township']:

                # This should loop over reporting units.
                # It should create a new reporting unit for each county.
                # It should store all the keys/values for the reporting unit.
                # It should create a list called candidates in that new reporting unit.
                # That list should be filled with candidate reporting unit objects.
                # Those candidate reporting unit objects should sum the townships.
                # The reporting unit should also sum the townships.
                # Also it should be fast.

                if not results.get(ru.fipscode, None):
                    results[ru.fipscode] = dict(ru.__dict__)
                    results[ru.fipscode]['level'] = 'county'
                    results[ru.fipscode]['reportingunitid'] = None
                    results[ru.fipscode]['reportingunitname'] =  maps.FIPS_TO_STATE[ru.statepostal][ru.fipscode]
                    results[ru.fipscode]['candidates'] = {}

                else:
                    for c in ru.candidates:
                        if not results[ru.fipscode]['candidates'].get(c.unique_id, None):
                            results[ru.fipscode]['candidates'][c.unique_id] = dict(c.__dict__)
                            results[ru.fipscode]['candidates'][c.unique_id]['level'] = 'county'
                            results[ru.fipscode]['candidates'][c.unique_id]['reportingunitid'] = None
                            results[ru.fipscode]['candidates'][c.unique_id]['reportingunitname'] =  maps.FIPS_TO_STATE[ru.statepostal][ru.fipscode]
                        else:
                            results[ru.fipscode]['candidates'][c.unique_id]['votecount'] += c.votecount
                            results[ru.fipscode]['candidates'][c.unique_id]['precinctstotal'] += c.precinctstotal
                            results[ru.fipscode]['candidates'][c.unique_id]['precinctsreporting'] += c.precinctsreporting
                            try:
                                results[ru.fipscode]['candidates'][c.unique_id]['precinctsreportingpct'] = float(results[ru.fipscode]['candidates'][c.unique_id]['precinctsreporting']) / float(results[ru.fipscode]['candidates'][c.unique_id]['precinctstotal'])
                            except ZeroDivisionError:
                                results[ru.fipscode]['candidates'][c.unique_id]['precinctsreportingpct'] = 0.0

            for ru in results.values():
                cands = list([dict(c) for c in ru['candidates'].values()])
                del ru['candidates']
                ru['candidates'] = [c for c in cands]
                r = ReportingUnit(**ru)
                self.reportingunits.append(r)

    def set_id_field(self):
        """
        Set id to `<raceid>`.
        """
        self.id = self.raceid

    def serialize(self):
        """
        Implements :meth:`APElection.serialize()`.
        """
        return OrderedDict((
            ('id', self.id),
            ('raceid', self.raceid),
            ('racetype', self.racetype),
            ('racetypeid', self.racetypeid),
            ('description', self.description),
            ('initialization_data', self.initialization_data),
            ('lastupdated', self.lastupdated),
            ('national', self.national),
            ('officeid', self.officeid),
            ('officename', self.officename),
            ('party', self.party),
            ('seatname', self.seatname),
            ('seatnum', self.seatnum),
            ('statename', self.statename),
            ('statepostal', self.statepostal),
            ('test', self.test),
            ('uncontested', self.uncontested)
        ))

    def __unicode__(self):
        return "%s %s" % (self.racetype, self.officename)


class Election(APElection):
    """
    Canonical representation of an election on
    a single date.
    """
    def __init__(self, **kwargs):
        """
        :param electiondate: The date of the election.
        :param datafile: A cached data file.
        """
        self.id = None

        self.testresults = kwargs.get('testresults', False)
        self.liveresults = kwargs.get('liveresults', False)
        self.electiondate = kwargs.get('electiondate', None)

        self.parsed_json = kwargs.get('parsed_json', None)
        self.next_request = kwargs.get('next_request', None)
        self.datafile = kwargs.get('datafile', None)

        self.set_id_field()

    def __unicode__(self):
        return self.electiondate

    def set_id_field(self):
        """
        Set id to `<electiondate>`.
        """
        self.id = self.electiondate

    @classmethod
    def get_elections(cls, datafile=None):
        """
        Get election data from API or cached file.

        :param datafile:
            If datafile is specified, use instead of making an API call.
        """
        if not datafile:
            elections = list(utils.api_request('/')['elections'])
        else:
            with open(datafile) as f:
                elections = list(json.load(f)['elections'])

        # Developer API expects to give lowercase kwargs to an Election
        # object, but initializing from the API / file will have camelCase 
        # kwargs instead. So, for just this object, lowercase the kwargs.
        payload = []
        for e in elections:
            init_dict = {}
            for k,v in e.items():
                init_dict[k.lower()] = v
            payload.append(Election(**init_dict))

        return payload

    @classmethod
    def get_next_election(cls, datafile=None, electiondate=None):
        """
        Get next election. By default, will be relative to the current date.

        :param datafile:
            If datafile is specified, use instead of making an API call.
        :param electiondate:
            If electiondate is specified, gets the next election after the specified date.
        """
        if not electiondate:
            today = datetime.datetime.now()
        else:
            today = dateutil_parser.parse(electiondate)

        next_election = None
        lowest_diff = None
        for e in Election.get_elections(datafile=datafile):
            diff = (dateutil_parser.parse(e.electiondate) - today).days
            if diff > 0:
                if not lowest_diff and not next_election:
                    next_election = e
                    lowest_diff = diff
                elif lowest_diff and next_election:
                    if diff < lowest_diff:
                        next_election = e
                        lowest_diff = diff
        return next_election

    def get(self, path, **params):
        """
        Farms out request to api_request.
        Could possibly handle choosing which
        parser backend to use -- API-only right now.
        Also the entry point for recording, which
        is set via environment variable.

        :param path:
            API url path.
        :param **params:
            A dict of optional parameters to be included in API request.
        """
        return utils.api_request(path, **params)

    def get_uniques(self, candidate_reporting_units):
        """
        Parses out unique candidates and ballot measures
        from a list of CandidateReportingUnit objects.
        """
        unique_candidates = {}
        unique_ballot_measures = {}

        for c in candidate_reporting_units:
            if c.is_ballot_measure:
                if not unique_ballot_measures.get(c.candidateid, None):
                    unique_ballot_measures[c.candidateid] = BallotMeasure(
                                                                last=c.last,
                                                                candidateid=c.candidateid,
                                                                polid=c.polid,
                                                                ballotorder=c.ballotorder,
                                                                polnum=c.polnum,
                                                                seatname=c.seatname,
                                                                description=c.description)
            else:
                if not unique_candidates.get(c.candidateid, None):
                    unique_candidates[c.candidateid] = Candidate(
                                                                first=c.first,
                                                                last=c.last,
                                                                candidateid=c.candidateid,
                                                                polid=c.polid,
                                                                ballotorder=c.ballotorder,
                                                                polnum=c.polnum,
                                                                party=c.party)

        candidates = [v for v in unique_candidates.values()]
        ballot_measures = [v for v in unique_ballot_measures.values()]
        return candidates, ballot_measures 

    def get_raw_races(self, **params):
        """
        Convenience method for fetching races by election date.
        Accepts an AP formatting date string, e.g., YYYY-MM-DD.
        Accepts any number of URL params as kwargs.

        If datafile passed to constructor, the file will be used instead of making an HTTP request.

        :param **params:
            A dict of additional parameters to pass to API. Ignored if `datafile` was passed to the
            constructor.
        """
        if self.datafile:
            with open(self.datafile, 'r') as readfile:
                payload = dict(json.loads(readfile.read()))
        else:
            payload = self.get('/%s' % self.electiondate, **params)

        return payload

    def get_race_objects(self, parsed_json):
        """
        Get parsed race objects.

        :param parsed_json:
            Dict of parsed JSON.
        """
        if parsed_json['races'][0].get('candidates', None):
            payload = []
            for r in parsed_json['races']:
                r['initialization_data'] = True
                payload.append(Race(**r))
            return payload
        return [Race(**r) for r in parsed_json['races']]

    def get_units(self, raw_races):
        """
        Parses out races, reporting_units,
        and candidate_reporting_units in a
        single loop over the raw race JSON.

        :param raw_races:
            Raw race JSON.
        """
        races = []
        reporting_units = []
        candidate_reporting_units = []
        for race in raw_races:
            if not race.initialization_data:
                for unit in race.reportingunits:
                    for candidate in unit.candidates:
                        candidate_reporting_units.append(candidate)
                    del unit.candidates
                    reporting_units.append(unit)
                del race.candidates
                del race.reportingunits
                races.append(race)
            else:
                for candidate in race.candidates:
                    candidate_reporting_units.append(candidate)
                del race.candidates
                del race.reportingunits
                races.append(race)
        return races, reporting_units, candidate_reporting_units

    def serialize(self):
        """
        Implements :meth:`APElection.serialize()`.
        """
        return OrderedDict((
            ('id', self.id),
            ('electiondate', self.electiondate),
            ('liveresults', self.liveresults),
            ('testresults', self.testresults)
        ))

    @property
    def races(self):
        """
        Return list of race objects.
        """
        raw_races = self.get_raw_races(
            omitResults=True,
            level="ru",
            test=self.testresults
        )
        race_objs = self.get_race_objects(raw_races)
        races, reporting_units, candidate_reporting_units = self.get_units(race_objs)
        return races

    @property
    def reporting_units(self):
        """
        Return list of reporting unit objects.
        """
        raw_races = self.get_raw_races(
            omitResults=False,
            level="ru",
            test=self.testresults
        )
        race_objs = self.get_race_objects(raw_races)
        races, reporting_units, candidate_reporting_units = self.get_units(race_objs)
        return reporting_units

    @property
    def candidate_reporting_units(self):
        """
        Return list of candidate reporting unit objects.
        """
        raw_races = self.get_raw_races(
            omitResults=True,
            level="ru",
            test=self.testresults
        )
        race_objs = self.get_race_objects(raw_races)
        races, reporting_units, candidate_reporting_units = self.get_units(race_objs)
        return candidate_reporting_units

    @property
    def results(self):
        """
        Return list of candidate reporting unit objects with results.
        """
        raw_races = self.get_raw_races(
            omitResults=False,
            level="ru",
            test=self.testresults
        )
        race_objs = self.get_race_objects(raw_races)
        races, reporting_units, candidate_reporting_units = self.get_units(race_objs)
        return candidate_reporting_units

    @property
    def candidates(self):
        """
        Return list of candidate objects with results.
        """
        raw_races = self.get_raw_races(
            omitResults=True,
            level="ru",
            test=self.testresults
        )
        race_objs = self.get_race_objects(raw_races)
        races, reporting_units, candidate_reporting_units = self.get_units(race_objs)
        candidates, ballot_measures = self.get_uniques(candidate_reporting_units)
        return candidates

    @property
    def ballot_measures(self):
        """
        Return list of ballot measure objects with results.
        """
        raw_races = self.get_raw_races(
            omitResults=True,
            level="ru",
            test=self.testresults
        )
        race_objs = self.get_race_objects(raw_races)
        races, reporting_units, candidate_reporting_units = self.get_units(race_objs)
        candidates, ballot_measures = self.get_uniques(candidate_reporting_units)
        return ballot_measures
