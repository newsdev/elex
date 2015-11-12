from clint.textui import puts, colored
from elex.cli.utils import parse_date
from elex.parser import api
from functools import wraps


def require_date(fn):
    @wraps(fn)
    def decorated(self):
        if len(self.app.pargs.date) and self.app.pargs.date[0]:
            try:
                self.app.election.electiondate = parse_date(self.app.pargs.date[0])
                return fn(self)
            except ValueError:
                puts(colored.yellow('Whoa there, friend! There was an error:\n'))
                puts('{0} could not be recognized as a date.\n'.format(colored.yellow(self.app.pargs.date[0])))
        else:
            puts(colored.yellow('Please specify an election date (e.g. `elex init-races 2015-11-03`). Run `elex --help` for details.\n'))


    return decorated
