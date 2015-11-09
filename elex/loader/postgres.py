# -*- coding: utf-8 -*-

import peewee

from elex import loader


class BallotPosition(loader.PostgresModel, loader.BallotPositionModel):
    pass


class Candidate(loader.PostgresModel, loader.CandidateModel):
    pass


class CandidateReportingUnit(loader.PostgresModel, loader.CandidateReportingUnitModel):
    pass


class ReportingUnit(loader.PostgresModel, loader.ReportingUnitModel):
    pass


class Race(loader.PostgresModel, loader.RaceModel):
    pass


class Election(loader.PostgresModel, loader.ElectionModel):
    pass