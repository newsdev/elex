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
    class Meta:
        database = ELEX_PG_CONNEX


class CandidateResultModel(peewee.Model):
    """
    Fields but no database connection.
    For flexibility.
    For the record, this is a single candidate's
    record in a single reporting unit.
    """
    accept_ap_calls = peewee.BooleanField(default=True)
    race = peewee.IntegerField(null=True)
    reporting_unit = peewee.IntegerField(null=True)
    candidate = peewee.IntegerField(null=True)
    officeid = peewee.CharField(null=True)
    racetype = peewee.CharField(null=True)
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
    seatname = peewee.CharField(null=True)
    description = peewee.CharField(null=True)


class BallotPositionModel(peewee.Model):
    """
    Fields but no database connection.
    For flexibility.
    last contains the 'yes/no' field.
    """
    clean_name = peewee.CharField(null=True)
    clean_description = peewee.TextField(null=True)
    last = peewee.CharField(null=True)
    candidateid = peewee.CharField(null=True)
    polid = peewee.CharField(null=True)
    ballotorder = peewee.CharField(null=True)
    polnum = peewee.CharField(null=True)
    description = peewee.CharField(null=True)
    seatname = peewee.CharField(null=True)


class CandidateModel(peewee.Model):
    """
    Fields but no database connection.
    For flexibility.
    """
    clean_name = peewee.CharField(null=True)
    clean_description = peewee.TextField(null=True)
    first = peewee.CharField(null=True)
    last = peewee.CharField(null=True)
    party = peewee.CharField(null=True)
    candidateid = peewee.CharField(null=True)
    polid = peewee.CharField(null=True)
    ballotorder = peewee.CharField(null=True)
    polnum = peewee.CharField(null=True)


class ReportingUnitModel(peewee.Model):
    """
    Fields but no database connection.
    For flexibility.
    """
    accept_ap_calls = peewee.BooleanField(default=True)
    clean_name = peewee.CharField(null=True)
    clean_description = peewee.TextField(null=True)
    officeid = peewee.CharField(null=True)
    racetype = peewee.CharField(null=True)
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
    description = peewee.CharField(null=True)
    seatname = peewee.CharField(null=True)


class RaceModel(peewee.Model):
    """
    Fields but no database connection.
    For flexibility.
    """
    accept_ap_calls = peewee.BooleanField(default=True)
    clean_name = peewee.CharField(null=True)
    clean_description = peewee.TextField(null=True)
    description = peewee.CharField(null=True)
    test = peewee.BooleanField(default=False)
    raceid = peewee.CharField(null=True)
    statepostal = peewee.CharField(null=True)
    statename = peewee.CharField(null=True)
    racetype = peewee.CharField(null=True)
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


class ElectionModel(peewee.Model):
    """
    Fields but no database connection.
    For flexibility.
    """
    testresults = peewee.BooleanField(default=False)
    liveresults = peewee.BooleanField(default=False)
    electiondate = peewee.CharField(null=True)
    is_test = peewee.BooleanField(default=False)
