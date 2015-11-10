from clint.textui import puts, colored
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
            puts(colored.green('Whoa there, friend! There was an error:\n'))
            puts('{0} could not be recognized as a date.\n'.format(colored.yellow(app.argv[-1])))
    else:
        puts(colored.yellow('Please specify a command and election date (e.g. `elex init-races 2015-11-03`). See below for details.\n'))

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
