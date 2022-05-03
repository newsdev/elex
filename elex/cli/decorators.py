from elex import CACHE_DIRECTORY
from elex.cli.utils import parse_date
from elex.exceptions import APAPIKeyException
from functools import wraps
from requests.exceptions import ConnectionError, HTTPError
from xml.dom.minidom import parseString


def require_date_argument(fn):
    """
    Decorator that checks for date argument.
    """
    @wraps(fn)
    def decorated(self):
        name = fn.__name__.replace('_', '-')
        if self.app.pargs.data_file:
            return fn(self)
        elif len(self.app.pargs.date) and self.app.pargs.date[0]:
            try:
                self.app.election.electiondate = parse_date(
                    self.app.pargs.date[0]
                )
                return fn(self)
            except ValueError:
                text = '{0} could not be recognized as a date.'
                self.app.log.error(text.format(self.app.pargs.date[0]))
                self.app.close(1)

            return fn(self)
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
        except APAPIKeyException:
            text = 'APAPIKeyError: AP_API_KEY environment variable is not set.'
            self.app.log.error(text)
            self.app.close(1)
        except ConnectionError as e:
            real_exception = e.args[0]
            self.app.log.error('Connection error ({0})'.format(real_exception.reason))
            self.app.log.debug('Connection error accessing {0}'.format(e.request.url))

    return decorated
