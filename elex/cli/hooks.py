import logging
from elex.api import Election

CACHECONTROL_LOG_FORMAT = '%(asctime)s (%(levelname)s) %(name)s : %(message)s'


def add_election_hook(app):
    """
    Cache election API object reference after parsing args.
    """

    app.election = Election(
        testresults=app.pargs.test,
        liveresults=not app.pargs.not_live,
        resultslevel=app.pargs.results_level,
        setzerocounts=app.pargs.set_zero_counts,
        is_test=False
    )

    if app.pargs.data_file:
        app.election.datafile = app.pargs.data_file

    if app.pargs.national_only:
        app.election.national = True

    if app.pargs.local_only:
        app.election.national = False


def cachecontrol_logging_hook(app):
    """
    Reroute cachecontrol logger to use cement log handlers.
    """
    cachecontrol_logger = logging.getLogger('cachecontrol.controller')
    formatter = logging.Formatter(CACHECONTROL_LOG_FORMAT)
    for handler in app.log.backend.handlers:
        handler.setFormatter(formatter)
        cachecontrol_logger.addHandler(handler)
    cachecontrol_logger.setLevel(logging.DEBUG)
