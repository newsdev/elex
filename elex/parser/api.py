# -*- coding: utf-8 -*-

import datetime
import json

from collections import OrderedDict
from dateutil import parser
from elex.parser import utils

PCT_PRECISION = 6
STATE_ABBR = { 'AL': 'Alabama', 'AK': 'Alaska', 'AS': 'America Samoa', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District of Columbia', 'FM': 'Micronesia1', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MH': 'Islands1', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PW': 'Palau', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VI': 'Virgin Island', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}


class BaseObject(object):
    """
    Base class for most objects.
    Handy container for methods for first level
    transformation of data and AP connections.
    """

    def set_state_fields_from_reportingunits(self):
        if len(self.reportingunits) > 0:
            setattr(self, 'statepostal', self.reportingunits[0].statepostal)
            setattr(self, 'statename', STATE_ABBR[self.statepostal])

    def set_winner(self):
        """
        Translates winner: "X" into a boolean.
        """
        if self.winner == u"X":
            setattr(self, 'winner', True)
        else:
            setattr(self, 'winner', False)

    def set_reportingunits(self):
        """
        If this race has reportingunits,
        serialize them into objects.
        """
        reportingunits_obj = []
        for r in self.reportingunits:
            reportingunit_dict = dict(r)

            SKIP_FIELDS = ['candidates', 'statepostal', 'statename']

            for k, v in self.__dict__.items():
                if k not in SKIP_FIELDS:
                    reportingunit_dict[k] = v

            obj = ReportingUnit(**reportingunit_dict)

            reportingunits_obj.append(obj)
        setattr(self, 'reportingunits', reportingunits_obj)

    def set_polid(self):
        if self.polid == "0":
            self.polid = None

    def set_unique_id(self):
        """
        Candidate IDs are not globally unique.
        AP National Politian IDs (NPIDs or polid)
        are unique, but only national-level
        candidates have them; everyone else gets '0'.
        The unique key, then, is the NAME of the ID
        we're using and then the ID itself.
        Verified this is globally unique with Tracy.
        """
        if self.polid:
            self.unique_id = 'polid-%s' % self.polid
        else:
            self.unique_id = 'polnum-%s' % self.polnum

    def set_reportingunitids(self):
        """
        Per Tracy / AP developers, if the level is
        "state", the reportingunitid is always 1.
        """
        if not self.reportingunitid:
            if self.level == "state":
                setattr(self, 'reportingunitid', "1")

    def set_candidates(self):
        """
        If this thing (race, reportingunit) has candidates,
        serialize them into objects.
        """
        candidate_objs = []
        for c in self.candidates:
            candidate_dict = dict(c)

            if hasattr(self, 'officeid'):
                if getattr(self, 'officeid') == u'I':
                    candidate_dict['is_ballot_position'] = True

            for k, v in self.__dict__.items():
                candidate_dict[k] = v

            if hasattr(self, 'statepostal'):
                if getattr(self, 'statepostal') != None:
                    candidate_dict['statename'] = STATE_ABBR[getattr(self, 'statepostal')]
            obj = CandidateReportingUnit(**candidate_dict)
            candidate_objs.append(obj)
        setattr(self, 'candidates', sorted(candidate_objs, key=lambda x: x.ballotorder))

    def set_dates(self, date_fields):
        for field in date_fields:
            try:
                setattr(self, field + '_parsed', parser.parse(getattr(self, field)))
            except AttributeError:
                pass

    def set_fields(self, **kwargs):
        fieldnames = self.__dict__.keys()
        for k, v in kwargs.items():
            k = k.lower().strip()
            try:
                v = unicode(v.decode('utf-8'))
            except AttributeError:
                pass
            if k in fieldnames:
                setattr(self, k, v)

    def serialize(self):
        raise NotImplementedError

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()


class Candidate(BaseObject):
    """
    Canonical representation of a
    candidate. Should be globally unique
    for this election, across races.
    """
    def __init__(self, **kwargs):
        self.id = None
        self.ballotorder = None
        self.candidateid = None
        self.first = None
        self.last = None
        self.party = None
        self.polid = None
        self.polnum = None
        self.unique_id = None

        self.set_fields(**kwargs)
        self.set_polid()
        self.set_unique_id()
        self.set_id_field()

    def serialize(self):
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

    def set_id_field(self):
        self.id = self.unique_id

class BallotPosition(BaseObject):
    """
    Canonical representation of a ballot
    position.
    """
    def __init__(self, **kwargs):
        self.id = None
        self.ballotorder = None
        self.candidateid = None
        self.description = None
        self.last = None
        self.polid = None
        self.polnum = None
        self.seatname = None
        self.unique_id = None

        self.set_fields(**kwargs)
        self.set_polid()
        self.set_unique_id()
        self.set_id_field()

    def serialize(self):
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

    def set_id_field(self):
        self.id = self.unique_id

class CandidateReportingUnit(BaseObject):
    """
    Canonical reporesentation of an
    AP candidate. Note: A candidate can 
    be a person OR a ballot position.
    """
    def __init__(self, **kwargs):
        self.id = None
        self.unique_id = None
        self.first = None
        self.last = None
        self.party = None
        self.candidateid = None
        self.polid = None
        self.ballotorder = None
        self.polnum = None
        self.votecount = 0
        self.votepct = 0.0
        self.winner = False
        self.is_ballot_position = False
        self.level = None
        self.reportingunitname = None
        self.reportingunitid = None
        self.fipscode = None
        self.lastupdated = None
        self.precinctsreporting = 0
        self.precinctstotal = 0
        self.precinctsreportingpct = 0.0
        self.uncontested = False
        self.test = False
        self.raceid = None
        self.statepostal = None
        self.statename = None
        self.racetype = None
        self.racetypeid = None
        self.officeid = None
        self.officename = None
        self.seatname = None
        self.description = None
        self.seatnum = None
        self.uncontested = False
        self.lastupdated = None
        self.initialization_data = False
        self.national = False
        self.incumbent = False

        self.set_fields(**kwargs)
        self.set_winner()
        self.set_polid()
        self.set_unique_id()
        self.set_id_field()

        def set_id_field(self):
            self.id = "%s-%s-%s" % (self.raceid, self.unique_id, self.reportingunitid)

    def serialize(self):
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
            ('is_ballot_position', self.is_ballot_position),
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
        if self.is_ballot_position:
            payload = "%s" % self.party
        else:
            payload = "%s %s (%s)" % (self.first, self.last, self.party)
        if self.winner:
            payload += ' (w)'
        return payload


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
        self.precinctstotal = 0
        self.precinctsreportingpct = 0.0
        self.uncontested = False
        self.test = False
        self.raceid = None
        self.statepostal = None
        self.statename = None
        self.racetype = None
        self.racetypeid = None
        self.officeid = None
        self.officename = None
        self.seatname = None
        self.description = None
        self.seatnum = None
        self.uncontested = False
        self.lastupdated = None
        self.initialization_data = False
        self.national = False
        self.candidates = []

        self.set_fields(**kwargs)
        self.set_dates(['lastupdated'])
        self.set_reportingunitids()
        self.set_candidates()
        self.set_votecount()
        self.set_candidate_votepct()
        self.set_id_field()

    def __unicode__(self):
        if self.reportingunitname:
            return "%s %s (%s %% reporting)" % (self.statepostal, self.reportingunitname, self.precinctsreportingpct)
        return "%s %s (%s %% reporting)" % (self.statepostal, self.level, self.precinctsreportingpct)

    def set_id_field(self):
        self.id = self.reportingunitid

    def set_votecount(self):
        if not self.uncontested:
            for c in self.candidates:
                self.votecount = sum([c.votecount for c in self.candidates if c.level != 'subunit'])
        else:
            self.votecount = None

    def set_candidate_votepct(self):
        if not self.uncontested:
            for c in self.candidates:
                if c.level != 'subunit':
                    try:
                        c.votepct = float(c.votecount) / float(self.votecount)
                    except ZeroDivisionError:
                        pass

    def serialize(self):
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


class Race(BaseObject):
    """
    Canonical representation of a single
    race, which is a seat in a political geography
    within a certain election.
    """
    def __init__(self, **kwargs):
        self.statepostal = None
        self.statename = None
        self.test = False
        self.raceid = None
        self.racetype = None
        self.racetypeid = None
        self.officeid = None
        self.officename = None
        self.party = None
        self.seatname = None
        self.description = None
        self.seatnum = None
        self.uncontested = False
        self.lastupdated = None
        self.initialization_data = False
        self.national = False
        self.candidates = []
        self.reportingunits = []

        self.set_fields(**kwargs)
        self.set_dates(['lastupdated'])
        self.set_id_field()

        if self.initialization_data:
            self.set_candidates()
        else:
            self.set_reportingunits()
            self.set_state_fields_from_reportingunits()

    def set_id_field():
        self.id = self.raceid

    def serialize(self):
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


class Election(BaseObject):
    """
    Canonical representation of an election on
    a single date.

    :param electiondate: The date of the election.
    :param datafile: A cached data file.
    """
    def __init__(self, **kwargs):
        self.testresults = False
        self.liveresults = False
        self.electiondate = None

        self.parsed_json = None
        self.next_request = None
        self.datafile = None

        self.set_fields(**kwargs)
        self.set_dates(['electiondate'])
        self.set_id_field()

    def __unicode__(self):
        return self.electiondate

    def set_id_field(self):
        self.id = self.electiondate

    @classmethod
    def get_elections(cls, datafile=None):
        if not datafile:
            elections = list(utils.api_request('/')['elections'])
        else:
            with open(datafile) as f:
                elections = list(json.load(f)['elections'])

        return [Election(**election) for election in elections]

    @classmethod
    def get_next_election(cls, datafile=None, electiondate=None):
        if not electiondate:
            today = datetime.datetime.now()
        else:
            today = parser.parse(electiondate)

        next_election = None
        lowest_diff = None
        for e in Election.get_elections(datafile=datafile):
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

    def get(self, path, **params):
        """
        Farms out request to api_request.
        Could possibly handle choosing which
        parser backend to use -- API-only right now.
        Also the entry point for recording, which
        is set via environment variable.
        """
        return utils.api_request(path, **params)

    def get_uniques(self, candidate_reporting_units):
        """
        Parses out unique candidates and ballot positions
        from a list of CandidateReportingUnit objects.
        """
        unique_candidates = {}
        unique_ballot_positions = {}

        for c in candidate_reporting_units:
            if c.is_ballot_position:
                if not unique_ballot_positions.get(c.candidateid, None):
                    unique_ballot_positions[c.candidateid] = BallotPosition(
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
        ballot_positions = [v for v in unique_ballot_positions.values()]
        return candidates, ballot_positions 

    def get_raw_races(self, **kwargs):
        """
        Convenience method for fetching races by election date.
        Accepts an AP formatting date string, e.g., YYYY-MM-DD.
        Accepts any number of URL params as kwargs.

        If datafile passed to constructor, the file will be used instead of making an HTTP request.
        """
        if self.datafile:
            with open(self.datafile, 'r') as readfile:
                payload = dict(json.loads(readfile.read()))
        else:
            payload = self.get('/%s' % self.electiondate, **kwargs)

        return payload

    def get_race_objects(self, parsed_json):
        """
        Given some parsed JSON, decided if this is standard
        results data or 
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
        return OrderedDict((
            ('id', self.id),
            ('electiondate', self.electiondate),
            ('liveresults', self.liveresults),
            ('testresults', self.testresults)
        ))

    @property
    def races(self):
        """
        Return list of race objects
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
        Return list of reporting unit objects
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
        Return list of candidate reporting unit objects
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
        Return list of candidate reporting unit objects with results
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
        Return list of candidate objects with results
        """
        raw_races = self.get_raw_races(
            omitResults=True,
            level="ru",
            test=self.testresults
        )
        race_objs = self.get_race_objects(raw_races)
        races, reporting_units, candidate_reporting_units = self.get_units(race_objs)
        candidates, ballot_positions = self.get_uniques(candidate_reporting_units)
        return candidates

    @property
    def ballot_positions(self):
        """
        Return list of ballot position (aka ballot issue) objects with results
        """
        raw_races = self.get_raw_races(
            omitResults=True,
            level="ru",
            test=self.testresults
        )
        race_objs = self.get_race_objects(raw_races)
        races, reporting_units, candidate_reporting_units = self.get_units(race_objs)
        candidates, ballot_positions = self.get_uniques(candidate_reporting_units)
        return ballot_positions
