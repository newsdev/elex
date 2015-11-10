from clint.textui import puts
from elex.parser import api
from elex.cli.utils import parse_date


def process_date_hook(app):
    """
    Pre-parse date argument.
    """
    if len(app.argv):
        try:
            app.argv[-1] = parse_date(app.argv[-1])
            return
        except ValueError:
            puts('"{0}" could not be recognized as a date.\n'.format(app.argv[-1]))
    else:
        puts('Please specify an election date and optional command (e.g. `elex init-races 2015-11-03`)\n')

    app.args.print_help()
    app.close()


def add_races_hook(app):
    """
    Cache election API object reference after parsing args.
    """
    app.election = api.Election(
        electiondate=app.pargs.date[0],
        testresults=app.pargs.test,
        liveresults=not app.pargs.not_live,
        is_test=False
    )
