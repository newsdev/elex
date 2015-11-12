from elex.parser import api


def add_races_hook(app):
    """
    Cache election API object reference after parsing args.
    """
    app.election = api.Election(
        electiondate=app.pargs.date,
        testresults=app.pargs.test,
        liveresults=not app.pargs.not_live,
        is_test=False
    )
