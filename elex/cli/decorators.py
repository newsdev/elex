import os
from functools import wraps
from elex.cli.utils import parse_date
from clint.textui import puts, colored


def require_date_argument(fn):
    """
    Decorator that checks for date argument.
    """
    @wraps(fn)
    def decorated(self):
        name = fn.__name__.replace('_', '-')
        if len(self.app.pargs.date) and self.app.pargs.date[0]:
            try:
                self.app.election.electiondate = parse_date(
                    self.app.pargs.date[0]
                )
                return fn(self)
            except ValueError:
                puts(
                    colored.yellow('Whoa there, friend! There was an error:\n')
                )
                text = '{0} could not be recognized as a date.\n'
                puts(text.format(colored.green(self.app.pargs.date[0])))
            return fn(self)
        else:
            text = 'Please specify an election date (e.g. `elex {0} 2015-11-\
03\`) or data file (e.g. `elex {0} --data-file path/to/file.json`). \n\nRun \
`elex` for help.\n'
            puts(colored.yellow(text.format(name)))

    return decorated


def require_ap_api_key(fn):
    """
    Decorator that checks for Associated Press API key or data-file argument.
    """
    @wraps(fn)
    def decorated(self):
        if not self.app.pargs.data_file and not (
            self.app.pargs.delegate_sum_file and
            self.app.pargs.delegate_super_file
        ) and not os.environ.get("AP_API_KEY", None):
            puts(colored.yellow('Whoa there, friend! There was an error:\n'))
            text = 'You have not exported {0} as an environment variable.\n'
            puts(text.format(colored.green("AP_API_KEY")))
        else:
            return fn(self)
    return decorated
