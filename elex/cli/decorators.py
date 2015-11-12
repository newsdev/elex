from clint.textui import puts, puts_err, colored
from elex.cli.utils import parse_date
from functools import wraps


def require_date(fn):
    @wraps(fn)
    def decorated(self):
        name = fn.__name__.replace('_', '-')
        if len(self.app.pargs.date) and self.app.pargs.date[0]:
            try:
                self.app.election.electiondate = parse_date(self.app.pargs.date[0])
                puts_err(colored.yellow('Running {0} for election {1}'.format(
                    fn.__name__,
                    self.app.election.electiondate
                )))
                return fn(self)
            except ValueError:
                puts(colored.yellow('Whoa there, friend! There was an error:\n'))
                puts('{0} could not be recognized as a date.\n'.format(colored.green(self.app.pargs.date[0])))
        else:
            puts(colored.yellow('Please specify an election date (e.g. `elex {0} 2015-11-03`). Run `elex` for help.\n'.format(name)))


    return decorated
