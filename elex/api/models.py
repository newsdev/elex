# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import ujson as json
import datetime
from elex.api import maps
from elex.api import utils
from collections import OrderedDict
from dateutil import parser as dateutil_parser

PCT_PRECISION = 6


class APElection(utils.UnicodeMixin):
    """
    Base class for most objects.

    Includes handy methods for transformation of data and AP connections
    """
    def set_state_fields_from_reportingunits(self):
        """
        Set state fields.
        """
        if len(self.reportingunits) > 0:
            self.statepostal = str(self.reportingunits[-1].statepostal)
            self.statename = str(maps.STATE_ABBR[self.statepostal])

    def set_reportingunits(self):
        """
        Set reporting units.

        If this race has reportingunits,
        serialize them into objects.
        """
        reportingunits_obj = []

        for r in self.reportingunits:

            # Don't obliterate good data with possibly empty fields.
            SKIP_FIELDS = ['candidates', 'statepostal', 'statename']

            for k, v in self.__dict__.items():
                if k not in SKIP_FIELDS:
                    r[k] = v

            obj = ReportingUnit(**r)

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
                # Adds the statepostal to make these reportinunitids unique even for
                # national elections. See #0278.
                setattr(self, 'reportingunitid', 'state-%s-1' % self.statepostal)
        else:
            """
            Fixes #226 reportingunitids recycled across levels.
            """
            setattr(self, 'reportingunitid', '%s-%s' % (
                self.level, self.reportingunitid))

    def set_candidates(self):
        """
        Set candidates.

        If this thing (race, reportingunit) has candidates,
        serialize them into objects.
        """
        candidate_objs = []
        for c in self.candidates:

            for k, v in self.__dict__.items():
                if k != 'votecount':
                    c.setdefault(k, v)

            c['is_ballot_measure'] = False
            if hasattr(self, 'officeid') and getattr(self, 'officeid') == 'I':
                c['is_ballot_measure'] = True

            if getattr(self, 'statepostal', None) is not None:
                statename = maps.STATE_ABBR[self.statepostal]
                c['statename'] = statename

            obj = CandidateReportingUnit(**c)
            candidate_objs.append(obj)

        self.candidates = candidate_objs

    def serialize(self):
        """
        Serialize the object. Should be implemented in all classes that
        inherit from :class:`APElection`.

        Should return an OrderedDict.
        """
        raise NotImplementedError


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
        AP National Politician IDs (NPIDs or polid)
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

    Ballot measures are similar to :class:`Candidate` objects, but represent a
    position on a ballot such as "In favor of" or "Against" for ballot
    measures such as a referendum.
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
        self.electiondate = kwargs.get('electiondate', None)
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
            ('candidateid', self.candidateid),
            ('ballotorder', self.ballotorder),
            ('description', self.description),
            ('electiondate', self.electiondate),
            ('last', self.last),
            ('polid', self.polid),
            ('polnum', self.polnum),
            ('seatname', self.seatname),
        ))

    def set_unique_id(self):
        """
        Generate and set unique id.

        Candidate IDs are not globally unique.
        AP National Politician IDs (NPIDs or polid)
        are unique, but only national-level
        candidates have them; everyone else gets '0'.
        The unique key, then, is the NAME of the ID
        we're using and then the ID itself.
        Verified this is globally unique with Tracy.
        """
        self.unique_id = "%s-%s" % (self.electiondate, self.candidateid)

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
        self.electiondate = kwargs.get('electiondate', None)
        self.first = kwargs.get('first', None)
        self.last = kwargs.get('last', None)
        self.party = kwargs.get('party', None)

        self.candidateid = kwargs.get('candidateID', None)
        if kwargs.get('candidateid', None):
            self.candidateid = kwargs['candidateid']

        self.polid = kwargs.get('polID', None)
        if kwargs.get('polid', None):
            self.polid = kwargs['polid']

        self.ballotorder = kwargs.get('ballotOrder', None)
        if kwargs.get('ballotorder', None):
            self.ballotorder = kwargs['ballotorder']

        self.polnum = kwargs.get('polNum', None)
        if kwargs.get('polnum', None):
            self.polnum = kwargs['polnum']

        self.votecount = kwargs.get('voteCount', 0)
        if kwargs.get('votecount', None):
            self.votecount = kwargs['votecount']

        self.votepct = kwargs.get('votePct', 0.0)
        if kwargs.get('votepct', None):
            self.votepct = kwargs['votepct']

        self.delegatecount = kwargs.get('delegateCount', 0)
        if kwargs.get('delegatecount', None):
            self.delegatecount = kwargs['delegatecount']

        self.winner = kwargs.get('winner', False) == 'X'
        self.runoff = kwargs.get('winner', False) == 'R'
        self.is_ballot_measure = kwargs.get('is_ballot_measure', None)
        self.level = kwargs.get('level', None)
        self.reportingunitname = kwargs.get('reportingunitname', None)
        self.reportingunitid = kwargs.get('reportingunitid', None)
        self.fipscode = kwargs.get('fipscode', None)
        self.lastupdated = kwargs.get('lastupdated', None)
        self.precinctsreporting = kwargs.get('precinctsreporting', 0)
        self.precinctstotal = kwargs.get('precinctstotal', 0)
        self.precinctsreportingpct = kwargs.get('precinctsreportingpct', 0.0)
        self.eevp = kwargs.get('eevp', None)
        self.uncontested = kwargs.get('uncontested', False)
        self.test = kwargs.get('test', False)
        self.resultstype = kwargs.get('resultstype', None)
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
        self.electtotal = kwargs.get('electtotal', 0)
        self.electwon = kwargs.get('electWon', 0)

        self.set_polid()
        self.set_unique_id()
        self.set_id_field()

    def set_id_field(self):
        """
        Set id to `<raceid>-<uniqueid>-<reportingunitid>`.
        """
        self.id = "%s-%s-%s" % (
            self.raceid,
            self.unique_id,
            self.reportingunitid
        )

    def set_unique_id(self):
        """
        Generate and set unique id.

        Candidate IDs are not globally unique.
        AP National Politician IDs (NPIDs or polid)
        are unique, but only national-level
        candidates have them; everyone else gets '0'.
        The unique key, then, is the NAME of the ID
        we're using and then the ID itself.
        Verified this is globally unique with Tracy Lewis.
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
            ('raceid', self.raceid),
            ('racetype', self.racetype),
            ('racetypeid', self.racetypeid),
            ('ballotorder', self.ballotorder),
            ('candidateid', self.candidateid),
            ('description', self.description),
            ('delegatecount', self.delegatecount),
            ('electiondate', self.electiondate),
            ('electtotal', self.electtotal),
            ('electwon', self.electwon),
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
            ('eevp', self.eevp),
            ('reportingunitid', self.reportingunitid),
            ('reportingunitname', self.reportingunitname),
            ('runoff', self.runoff),
            ('seatname', self.seatname),
            ('seatnum', self.seatnum),
            ('statename', self.statename),
            ('statepostal', self.statepostal),
            ('test', self.test),
            ('resultstype', self.resultstype),
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
        return "{}".format(payload)


class ReportingUnit(APElection):
    """
    Canonical representation of a single
    level of reporting.
    """
    def __init__(self, **kwargs):
        self.electiondate = kwargs.get('electiondate', None)

        self.statepostal = kwargs.get('statePostal', None)
        if kwargs.get('statepostal', None):
            self.statepostal = kwargs['statepostal']

        self.statename = kwargs.get('stateName', None)
        if kwargs.get('statename', None):
            self.statename = kwargs['statename']

        self.level = kwargs.get('level', None)

        self.reportingunitname = kwargs.get('reportingunitName', None)
        if kwargs.get('reportingunitname', None):
            self.reportingunitname = kwargs['reportingunitname']

        self.reportingunitid = kwargs.get('reportingunitID', None)
        if kwargs.get('reportingunitid', None):
            self.reportingunitid = kwargs['reportingunitid']

        self.fipscode = kwargs.get('fipsCode', None)
        if kwargs.get('fipscode', None):
            self.fipscode = kwargs['fipscode']

        self.lastupdated = kwargs.get('lastUpdated', None)
        if kwargs.get('lastupdated', None):
            self.lastupdated = kwargs['lastupdated']

        self.precinctsreporting = kwargs.get('precinctsReporting', 0)
        if kwargs.get('precinctsreporting', None):
            self.precinctsreporting = kwargs['precinctsreporting']

        self.precinctstotal = kwargs.get('precinctsTotal', 0)
        if kwargs.get('precinctstotal', None):
            self.precinctstotal = kwargs['precinctstotal']

        self.precinctsreportingpct = kwargs.get('precinctsReportingPct', 0.0)\
            * 0.01

        self.eevp = kwargs.get('eevp', None)

        if kwargs.get('precinctsreportingpct', None):
            self.precinctsreportingpct = kwargs['precinctsreportingpct']

        self.uncontested = kwargs.get('uncontested', False)
        self.test = kwargs.get('test', False)
        self.resultstype = kwargs.get('resultstype', None)
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
        self.electtotal = kwargs.get('electTotal', 0)

        self.set_level()
        self.pad_fipscode()
        self.set_reportingunitids()
        self.set_candidates()
        self.set_votecount()
        self.set_candidate_votepct()
        self.set_id_field()

    def __unicode__(self):
        template = "%s %s (%s %% reporting)"
        if self.reportingunitname:
            return template % (
                self.statepostal,
                self.reportingunitname,
                self.precinctsreportingpct
            )
        return template % (
            self.statepostal,
            self.level,
            self.precinctsreportingpct
        )

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
                self.votecount = sum([c.votecount for c in self.candidates])
        else:
            self.votecount = None

    def set_candidate_votepct(self):
        """
        Set vote percentage for each candidate.
        """
        if not self.uncontested:
            for c in self.candidates:
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
            ('electiondate', self.electiondate),
            ('electtotal', self.electtotal),
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
            ('eevp', self.eevp),
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
            ('resultstype', self.resultstype),
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
        self.electiondate = kwargs.get('electiondate', None)
        self.statepostal = kwargs.get('statePostal', None)
        self.statename = kwargs.get('stateName', None)
        self.test = kwargs.get('test', False)
        self.resultstype = kwargs.get('resultsType', None)
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
        self.is_ballot_measure = False

        self.set_id_field()

        if self.initialization_data:
            self.set_candidates()
        else:
            self.set_reportingunits()
            self.set_state_fields_from_reportingunits()
            self.set_new_england_counties()

    def set_new_england_counties(self):
        if self.statepostal in maps.FIPS_TO_STATE.keys():

            counties = {}

            for c in maps.FIPS_TO_STATE[self.statepostal].keys():
                try:
                    counties[c] = dict([
                        r.__dict__ for
                        r in self.reportingunits if
                        r.level == 'township' and
                        "Mail Ballots C.D." not in r.reportingunitname and
                        r.fipscode == c
                    ][0])

                    # Set some basic information we know about the county.
                    counties[c]['level'] = 'county'
                    counties[c]['statepostal'] = self.statepostal
                    counties[c]['candidates'] = {}
                    counties[c]['reportingunitname'] =\
                        maps.FIPS_TO_STATE[self.statepostal][c]
                    counties[c]['reportingunitid'] = "%s-%s" % (
                        self.statepostal,
                        c
                    )

                    reporting_units = [
                        r for
                        r in self.reportingunits if
                        r.level == 'township' and
                        "Mail Ballots C.D." not in r.reportingunitname and
                        r.fipscode == c
                    ]

                    # Declaratively sum the precincts / votes for this county.
                    counties[c]['precinctstotal'] = sum([
                        r.precinctstotal for
                        r in reporting_units if
                        r.level == 'township' and
                        "Mail Ballots C.D." not in r.reportingunitname and
                        r.fipscode == c
                    ])
                    counties[c]['precinctsreporting'] = sum([
                        r.precinctsreporting for
                        r in reporting_units if
                        r.level == 'township' and
                        "Mail Ballots C.D." not in r.reportingunitname and
                        r.fipscode == c
                    ])

                    pcts_tot = float(counties[c]['precinctstotal'])
                    pcts_rep = float(counties[c]['precinctsreporting'])

                    try:
                        counties[c]['precinctsreportingpct'] = pcts_rep / pcts_tot
                    except ZeroDivisionError:
                        counties[c]['precinctsreportingpct'] = 0.0

                    counties[c]['votecount'] = sum([
                        int(r.votecount or 0) for
                        r in reporting_units if
                        r.level == 'township' and
                        "Mail Ballots C.D." not in r.reportingunitname and
                        r.fipscode == c
                    ])

                    for r in reporting_units:

                        # Set up candidates for each county.
                        for cru in r.candidates:
                            if not counties[c]['candidates'].get(cru.unique_id, None):
                                d = dict(cru.__dict__)
                                d['level'] = 'county'
                                d['reportingunitid'] = "%s-%s" % (
                                    self.statepostal,
                                    c
                                )
                                fips_dict = maps.FIPS_TO_STATE[self.statepostal]
                                d['reportingunitname'] = fips_dict[c]
                                counties[c]['candidates'][cru.unique_id] = d

                            else:
                                d = counties[c]['candidates'][cru.unique_id]
                                d['votecount'] += cru.votecount
                                d['precinctstotal'] += cru.precinctstotal
                                d['precinctsreporting'] += cru.precinctsreporting

                                try:
                                    d['precinctsreportingpct'] = (
                                        float(d['precinctsreporting']) /
                                        float(d['precinctstotal'])
                                    )

                                except ZeroDivisionError:
                                    d['precinctsreportingpct'] = 0.0

                except IndexError:
                    """
                    This is the ME bug from the ME primary.
                    """
                    pass

            try:
                for ru in counties.values():
                    ru['candidates'] = ru['candidates'].values()
                    ru['statename'] = str(maps.STATE_ABBR[ru['statepostal']])
                    r = ReportingUnit(**ru)
                    self.reportingunits.append(r)

            except AttributeError:
                """
                Sometimes, the dict is empty because we have no townships to
                roll up into counties. Issue #228.
                """
                pass

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
            ('electiondate', self.electiondate),
            ('initialization_data', self.initialization_data),
            ('is_ballot_measure', self.is_ballot_measure),
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
            ('resultstype', self.resultstype),
            ('uncontested', self.uncontested)
        ))

    def __unicode__(self):
        if self.racetype:
            return "%s %s" % (self.racetype, self.officename)
        return "%s" % self.officename


class Elections():
    """
    Holds a collection of election objects
    """

    def get_elections(self, datafile=None):
        """
        Get election data from API or cached file.

        :param datafile:
            If datafile is specified, use instead of making an API call.
        """
        if not datafile:
            elections = list(utils.api_request('/elections').json().get('elections'))
        else:
            with open(datafile) as f:
                elections = list(json.load(f).get('elections'))

        # Developer API expects to give lowercase kwargs to an Election
        # object, but initializing from the API / file will have camelCase
        # kwargs instead. So, for just this object, lowercase the kwargs.
        payload = []
        for e in elections:
            init_dict = OrderedDict()
            for k, v in e.items():
                init_dict[k.lower()] = v
            payload.append(Election(**init_dict))

        return payload

    def get_next_election(self, datafile=None, electiondate=None):
        """
        Get next election. By default, will be relative to the current date.

        :param datafile:
            If datafile is specified, use instead of making an API call.
        :param electiondate:
            If electiondate is specified, gets the next election
            after the specified date.
        """
        if not electiondate:
            today = datetime.datetime.now()
        else:
            today = dateutil_parser.parse(electiondate)

        next_election = None
        lowest_diff = None
        for e in self.get_elections(datafile=datafile):
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


class Election(APElection):
    """
    Canonical representation of an election on
    a single date.
    """
    def __init__(self, **kwargs):
        """
        :param electiondate:
            The date of the election.
        :param datafile:
            A cached data file.
        """
        self.id = None

        self.testresults = kwargs.get('testresults', False)
        self.liveresults = kwargs.get('liveresults', False)
        self.resultstype = kwargs.get('resultstype')
        self.electiondate = kwargs.get('electiondate', None)
        self.national = kwargs.get('national', None)
        self.api_key = kwargs.get('api_key', None)

        self.parsed_json = kwargs.get('parsed_json', None)
        self.next_request = kwargs.get('next_request', None)
        self.datafile = kwargs.get('datafile', None)
        self.resultslevel = kwargs.get('resultslevel', 'ru')
        self.setzerocounts = kwargs.get('setzerocounts', False)

        self.raceids = kwargs.get('raceids', [])
        self.officeids = kwargs.get('officeids', None)

        self.set_id_field()

        self._response = None

    def __unicode__(self):
        return "{}".format(self.electiondate)

    def set_id_field(self):
        """
        Set id to `<electiondate>`.
        """
        self.id = self.electiondate

    def get(self, path, **params):
        """
        Farms out request to api_request.
        Could possibly handle choosing which
        parser backend to use -- API-only right now.
        Also the entry point for recording, which
        is set via environment variable.

        :param path:
            API url path.
        :param \**params:
            A dict of optional parameters to be included in API request.
        """
        self._response = utils.api_request('/elections/{0}'.format(path), **params)
        return self._response.json()

    def get_uniques(self, candidate_reporting_units):
        """
        Parses out unique candidates and ballot measures
        from a list of CandidateReportingUnit objects.
        """
        unique_candidates = OrderedDict()
        unique_ballot_measures = OrderedDict()

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
                        description=c.description,
                        electiondate=self.electiondate
                    )
            else:
                if not unique_candidates.get(c.candidateid, None):
                    unique_candidates[c.candidateid] = Candidate(
                        first=c.first,
                        last=c.last,
                        candidateid=c.candidateid,
                        polid=c.polid,
                        ballotorder=c.ballotorder,
                        polnum=c.polnum,
                        party=c.party
                    )

        candidates = [v for v in unique_candidates.values()]
        ballot_measures = [v for v in unique_ballot_measures.values()]
        return candidates, ballot_measures

    def get_raw_races(self, **params):
        """
        Convenience method for fetching races by election date.
        Accepts an AP formatting date string, e.g., YYYY-MM-DD.
        Accepts any number of URL params as kwargs.

        If datafile passed to constructor, the file will be used instead of
        making an HTTP request.

        :param \**params:
            A dict of additional parameters to pass to API.
            Ignored if `datafile` was passed to the constructor.
        """
        if self.datafile:
            with open(self.datafile, 'r') as readfile:
                payload = json.loads(readfile.read())
                self.electiondate = payload.get('electionDate')
                return payload
        else:
            payload = self.get(self.electiondate, **params)
            return payload

    def get_race_objects(self, parsed_json):
        """
        Get parsed race objects.

        :param parsed_json:
            Dict of parsed AP election JSON.
        """
        if len(parsed_json['races']) > 0:
            if parsed_json['races'][0].get('candidates', None):
                payload = []
                for r in parsed_json['races']:
                    if len(self.raceids) > 0 and r['raceID'] in self.raceids:
                        r['initialization_data'] = True
                        payload.append(Race(**r))
                    else:
                        r['initialization_data'] = True
                        payload.append(Race(**r))
                return payload
            if len(self.raceids) > 0:
                return [Race(**r) for r in parsed_json['races'] if r['raceID'] in self.raceids]
            else:
                return [Race(**r) for r in parsed_json['races']]
        else:
            return []

    def get_units(self, race_objs):
        """
        Parses out races, reporting_units,
        and candidate_reporting_units in a
        single loop over the race objects.

        :param race_objs:
            A list of top-level Race objects.
        """
        races = []
        reporting_units = []
        candidate_reporting_units = []
        for race in race_objs:
            race.electiondate = self.electiondate
            if not race.initialization_data:
                for unit in race.reportingunits:
                    unit.electiondate = self.electiondate
                    for candidate in unit.candidates:
                        if candidate.is_ballot_measure:
                            race.is_ballot_measure = True
                        candidate.electiondate = self.electiondate
                        candidate_reporting_units.append(candidate)
                    del unit.candidates
                    reporting_units.append(unit)
                del race.candidates
                del race.reportingunits
                races.append(race)
            else:
                for candidate in race.candidates:
                    if candidate.is_ballot_measure:
                        race.is_ballot_measure = True
                    candidate.electiondate = self.electiondate
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
            ('testresults', self.testresults),
            ('resultstype', self.resultstype)
        ))

    @property
    def races(self):
        """
        Return list of race objects.
        """
        raw_races = self.get_raw_races(
            omitResults=True,
            level="ru",
            resultstype=self.resultstype,
            national=self.national,
            officeID=self.officeids,
            apiKey=self.api_key
        )

        race_objs = self.get_race_objects(raw_races)
        races, reporting_units, candidate_reporting_units = self.get_units(
            race_objs
        )
        return races

    @property
    def reporting_units(self):
        """
        Return list of reporting unit objects.
        """
        raw_races = self.get_raw_races(
            omitResults=False,
            level="ru",
            resultstype=self.resultstype,
            national=self.national,
            officeID=self.officeids,
            apiKey=self.api_key
        )
        race_objs = self.get_race_objects(raw_races)
        races, reporting_units, candidate_reporting_units = self.get_units(
            race_objs
        )
        return reporting_units

    @property
    def candidate_reporting_units(self):
        """
        Return list of candidate reporting unit objects.
        """
        raw_races = self.get_raw_races(
            omitResults=True,
            level="ru",
            test=self.testresults,
            national=self.national,
            officeID=self.officeids,
            apiKey=self.api_key
        )
        race_objs = self.get_race_objects(raw_races)
        races, reporting_units, candidate_reporting_units = self.get_units(
            race_objs
        )
        return candidate_reporting_units

    @property
    def results(self):
        """
        Return list of candidate reporting unit objects with results.
        """
        raw_races = self.get_raw_races(
            omitResults=False,
            level=self.resultslevel,
            setzerocounts=self.setzerocounts,
            resultstype=self.resultstype,
            national=self.national,
            officeID=self.officeids,
            apiKey=self.api_key
        )
        race_objs = self.get_race_objects(raw_races)
        races, reporting_units, candidate_reporting_units = self.get_units(
            race_objs
        )
        return candidate_reporting_units

    @property
    def candidates(self):
        """
        Return list of candidate objects with results.
        """
        raw_races = self.get_raw_races(
            omitResults=True,
            level="ru",
            resultstype=self.resultstype,
            national=self.national,
            officeID=self.officeids,
            apiKey=self.api_key
        )
        race_objs = self.get_race_objects(raw_races)
        races, reporting_units, candidate_reporting_units = self.get_units(
            race_objs
        )
        candidates, ballot_measures = self.get_uniques(
            candidate_reporting_units
        )
        return candidates

    @property
    def ballot_measures(self):
        """
        Return list of ballot measure objects with results.
        """
        raw_races = self.get_raw_races(
            omitResults=True,
            level="ru",
            resultstype=self.resultstype,
            national=self.national,
            apiKey=self.api_key
        )
        race_objs = self.get_race_objects(raw_races)
        races, reporting_units, candidate_reporting_units = self.get_units(
            race_objs
        )
        candidates, ballot_measures = self.get_uniques(
            candidate_reporting_units
        )
        return ballot_measures
