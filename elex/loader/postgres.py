# -*- coding: utf-8 -*-

import peewee

from elex import loader


class Candidate(loader.PostgresModel, loader.CandidateModel):
    pass


class ReportingUnit(loader.PostgresModel, loader.ReportingUnitModel):
    pass


class Race(loader.PostgresModel, loader.RaceModel):
    pass


class Election(loader.PostgresModel, loader.ElectionModel):
    pass