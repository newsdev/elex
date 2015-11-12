from clint.textui import puts, colored
from elex.cli.utils import parse_date
from functools import wraps


def require_date_argument(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        return fn(*args, **kwargs)
        #if len(self.app.pargs.date):
                #import ipdb; ipdb.set_trace();
            #try:
                #self.app.pargs.date = parse_date(self.app.pargs.date[0])
            #except ValueError:
                #puts(colored.yellow('Whoa there, friend! There was an error:\n'))
                #puts('{0} could not be recognized as a date.\n'.format(colored.yellow(self.app.pargs.date[0])))
        #else:
            #puts(colored.yellow('Please specify an election date (e.g. `elex init-races 2015-11-03`). Run `elex --help` for details.\n'))
            #self.app.close()


    return decorated
