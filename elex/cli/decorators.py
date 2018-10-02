from elex import CACHE_DIRECTORY
from elex.cli.utils import parse_date
from elex.exceptions import APAPIKeyException
from functools import wraps
from requests.exceptions import ConnectionError, HTTPError
from xml.dom.minidom import parseString


def attach_election_date(app, wrapped_fn, callback_context):
    """
    Attaches value of date argument to election model used in commands.

    Common to both `accept_date_argument` and `require_date_argument`
    decorators (i.e., this is called whether the date argument is
    mandatory or optional).
    """
    try:
        app.election.electiondate = parse_date(app.pargs.date[0])
        return wrapped_fn(callback_context)
    except ValueError:
        text = '{0} could not be recognized as a date.'
        app.log.error(text.format(app.pargs.date[0]))
        app.close(1)

    return wrapped_fn(callback_context)


def accept_date_argument(fn):
    """
    Decorator that checks for optional date argument.
    """
    @wraps(fn)
    def decorated(self):
        if len(self.app.pargs.date) and self.app.pargs.date[0]:
            returned_value = attach_election_date(self.app, fn, self)
            return returned_value
        return fn(self)

    return decorated


def require_date_argument(fn):
    """
    Decorator that checks for required date argument.
    """
    @wraps(fn)
    def decorated(self):
        name = fn.__name__.replace('_', '-')
        if self.app.pargs.data_file:
            return fn(self)
        elif len(self.app.pargs.date) and self.app.pargs.date[0]:
            return attach_election_date(self.app, fn, self)
        else:
            text = 'No election date (e.g. `elex {0} 2015-11-\
03`) or data file (e.g. `elex {0} --data-file path/to/file.json`) specified.'
            self.app.log.error(text.format(name))
            self.app.close(1)

    return decorated


def require_ap_api_key(fn):
    """
    Decorator that checks for Associated Press API key or data-file argument.
    """
    @wraps(fn)
    def decorated(self):
        self.app.log.debug('Cache directory: {0}'.format(CACHE_DIRECTORY))
        try:
            return fn(self)
        except HTTPError as e:
            if e.response.status_code == 400:
                message = e.response.json().get('errorMessage')
            elif e.response.status_code == 401:
                dom = parseString(e.response.content)
                error_msg = dom.getElementsByTagName('Message')[0].childNodes[0].data
                message = '{0} ({1})'.format(e.response.reason, error_msg)
            else:
                message = e.response.reason
            self.app.log.error('HTTP Error {0} - {1}'.format(e.response.status_code, message))
            self.app.log.debug('HTTP Error {0} ({1})'.format(e.response.status_code, e.response.url))
            self.app.close(1)
        except APAPIKeyException as e:
            text = 'APAPIKeyError: AP_API_KEY environment variable is not set.'
            self.app.log.error(text)
            self.app.close(1)
        except ConnectionError as e:
            real_exception = e.args[0]
            self.app.log.error('Connection error ({0})'.format(real_exception.reason))
            self.app.log.debug('Connection error accessing {0}'.format(e.request.url))

    return decorated
