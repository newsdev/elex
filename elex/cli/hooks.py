import logging
from elex.api import Election
from elex.cli.constants import LOG_FORMAT


def add_election_hook(app):
    """
    Cache election API object reference after parsing args.
    """
    app.election = Election(
        testresults=app.pargs.test,
        liveresults=not app.pargs.not_live,
        resultslevel=app.pargs.results_level,
        setzerocounts=app.pargs.set_zero_counts,
        is_test=False,
        raceids=[]
    )

    if app.pargs.data_file:
        app.election.datafile = app.pargs.data_file

    if app.pargs.national_only:
        app.election.national = True

    if app.pargs.local_only:
        app.election.national = False

    if app.pargs.raceids:
        app.election.raceids = [x.strip() for x in app.pargs.raceids.split(',')]


def cachecontrol_logging_hook(app):
    """
    Reroute cachecontrol logger to use cement log handlers.
    """
    from cachecontrol.controller import logger
    formatter = logging.Formatter(LOG_FORMAT)

    for handler in app.log.backend.handlers:
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(logging.DEBUG)
