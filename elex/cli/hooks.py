from elex.api import Election


def add_election_hook(app):
    """
    Cache election API object reference after parsing args.
    """
    app.election = Election(
        testresults=app.pargs.test,
        liveresults=not app.pargs.not_live,
        resultslevel=app.pargs.results_level,
        setzerocounts=app.pargs.set_zero_counts,
        national=app.pargs.local_only,
        is_test=False
    )
    if app.pargs.data_file:
        app.election.datafile = app.pargs.data_file
