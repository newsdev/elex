import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from .models import (
    APElection,
    Candidate,
    BallotMeasure,
    CandidateReportingUnit,
    ReportingUnit,
    Race,
    Elections,
    Election
)
from .delegates import (
    CandidateDelegateReport,
    DelegateReport
)

session = CacheControl(requests.session(),
                       cache=FileCache('.ecache'))

__all__ = [
    'APElection',
    'BallotMeasure',
    'Candidate',
    'CandidateDelegateReport',
    'CandidateReportingUnit',
    'DelegateReport',
    'Election',
    'Elections',
    'Race',
    'ReportingUnit',
]
