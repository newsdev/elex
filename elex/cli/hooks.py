import logging
from elex.api import Election
from elex.cli.constants import LOG_FORMAT
from elex.api import maps


def add_election_hook(app):
    """
    Cache election API object reference after parsing args.
    """
    app.election = Election(
        resultstype=app.pargs.results_type,
        liveresults=not app.pargs.not_live,
        resultslevel=app.pargs.results_level,
        setzerocounts=app.pargs.set_zero_counts,
        is_test=False,
        raceids=[],
        officeids=None
    )

    if app.pargs.data_file:
        app.election.datafile = app.pargs.data_file

    if app.pargs.national_only:
        app.election.national = True

    if app.pargs.local_only:
        app.election.national = False

    if app.pargs.raceids:
        app.election.raceids = [x.strip() for x in app.pargs.raceids.split(',')]

    if app.pargs.officeids:
        invalid_officeids = [x for x in app.pargs.officeids.split(',') if x not in maps.OFFICE_NAMES]
        if invalid_officeids:
            text = '{0} is/are invalid officeID(s). Here is a list of valid officeIDs: {1}'
            app.log.error(text.format(", ".join(invalid_officeids), ", ".join(maps.OFFICE_NAMES.keys())))
            app.close(1)
        else:
            app.election.officeids = app.pargs.officeids
            # kept as a comma-delimited string so officeID as a param always appears once in request url (e.g. officeID=P%2CH%2CG)


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
