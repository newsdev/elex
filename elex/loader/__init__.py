# -*- coding: utf-8 -*-

import os

import peewee

ELEX_PG_DB = os.environ.get('ELEX_PG_DB', 'elex')
ELEX_PG_USER = os.environ.get('ELEX_PG_USER', 'elex')
ELEX_PG_PASS = os.environ.get('ELEX_PG_PASS', '')
ELEX_PG_HOST = os.environ.get('ELEX_PG_HOST', '')
ELEX_PG_PORT = os.environ.get('ELEX_PG_PORT', '5432')

ELEX_PG_CONNEX = peewee.PostgresqlDatabase(
                    ELEX_PG_DB,
                    user=ELEX_PG_USER,
                    password=ELEX_PG_PASS,
                    host=ELEX_PG_HOST,
                    port=ELEX_PG_PORT)


class PostgresModel(peewee.Model):
    """
    Will be inherited by the postgres-specific models.
    """
    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()

    class Meta:
        database = ELEX_PG_CONNEX


class CandidateModel(peewee.Model):
    """
    Fields but no database connection.
    For flexibility.
    """
    reportingunitid = peewee.CharField(null=True)
    first = peewee.CharField(null=True)
    last = peewee.CharField(null=True)
    party = peewee.CharField(null=True)
    candidateid = peewee.CharField(null=True)
    polid = peewee.CharField(null=True)
    ballotorder = peewee.CharField(null=True)
    polnum = peewee.CharField(null=True)
    votecount = peewee.IntegerField(default=0)
    winner = peewee.BooleanField(default=False)
    is_ballot_position = peewee.BooleanField(default=False)
    raceid = peewee.CharField(null=True)
    statepostal = peewee.CharField(null=True)
    statename = peewee.CharField(null=True)

    def __unicode__(self):
        if self.is_ballot_position:
            payload = "%s" % self.party
        else:
            payload = "%s %s (%s)" % (self.first, self.last, self.party)
        if self.winner:
            payload += '✓'.decode('utf-8')
        return payload


class ReportingUnitModel(peewee.Model):
    """
    Fields but no database connection.
    For flexibility.
    """
    statepostal = peewee.CharField(null=True)
    statename = peewee.CharField(null=True)
    level = peewee.CharField(null=True)
    reportingunitname = peewee.CharField(null=True)
    reportingunitid = peewee.CharField(null=True)
    fipscode = peewee.CharField(null=True)
    lastupdated = peewee.CharField(null=True)
    lastupdated_parsed = peewee.DateTimeField(null=True)
    precinctsreporting = peewee.IntegerField(default=0)
    precinctsyotal = peewee.IntegerField(default=0)
    precinctsreportingpct = peewee.FloatField(default=0.0)
    raceid = peewee.CharField(null=True)

    def __unicode__(self):
        if self.reportingunitname:
            return "%s %s (%s %% reporting)" % (self.statepostal, self.reportingunitname, self.precinctsreportingpct)
        return "%s %s (%s %% reporting)" % (self.statepostal, self.level, self.precinctsreportingpct)

class RaceModel(peewee.Model):
    """
    Fields but no database connection.
    For flexibility.
    """
    test = peewee.BooleanField(default=False)
    raceid = peewee.CharField(null=True)
    statepostal = peewee.CharField(null=True)
    statename = peewee.CharField(null=True)
    raceType = peewee.CharField(null=True)
    reportingunitid = peewee.CharField(null=True)
    racetypeid = peewee.CharField(null=True)
    officeid = peewee.CharField(null=True)
    officename = peewee.CharField(null=True)
    party = peewee.CharField(null=True)
    seatname = peewee.CharField(null=True)
    seatnum = peewee.CharField(null=True)
    uncontested = peewee.BooleanField(default=False)
    lastupdated = peewee.CharField(null=True)
    lastupdated_parsed = peewee.DateTimeField(null=True)
    initialization_data = peewee.BooleanField(default=False)

    def __unicode__(self):
        name = self.officename
        if self.statepostal:
            name = "%s %s" % (self.statepostal, self.officename)
            if self.seatname:
                name += " %s" % self.seatname
        return name


class ElectionModel(peewee.Model):
    """
    Fields but no database connection.
    For flexibility.
    """
    testresults = peewee.BooleanField(default=False)
    liveresults = peewee.BooleanField(default=False)
    electiondate = peewee.CharField(null=True)
    is_test = peewee.BooleanField(default=False)

    def __unicode__(self):
        if self.is_test:
            return "TEST: %s" % self.electiondate
        else:
            return self.electiondate