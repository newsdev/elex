from elex.api import Elections
from elex.api import DelegateReport
from elex.api.delegates import clear_delegate_cache
from elex import DELEGATE_REPORT_ID_CACHE_FILE
from elex import __version__ as VERSION
from cement.core.foundation import CementApp
from elex.cli.hooks import add_election_hook
from cement.ext.ext_logging import LoggingLogHandler
from cement.core.controller import CementBaseController, expose
from elex.cli.decorators import require_date_argument, require_ap_api_key

LOG_FORMAT = '%(asctime)s (%(levelname)s) %(namespace)s (v{0}) : \
%(message)s'.format(VERSION)
BANNER = """
NYT AP Elections version {0}
""".format(VERSION)


class ElexBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = "Get and process AP elections data"
        arguments = [
            (['date'], dict(
                nargs='*',
                action='store',
                help='Election date (e.g. "2015-11-03"; most common date \
formats accepted).'
            )),
            (['-t', '--test'], dict(
                action='store_true',
                help='Use testing API calls'
            )),
            (['-n', '--not-live'], dict(
                action='store_true',
                help='Do not use live data API calls'
            )),
            (['-d', '--data-file'], dict(
                action='store',
                help='Specify data file instead of making HTTP request when \
using election commands like `elex results` and `elex races`.'
            )),
            (['--delegate-sum-file'], dict(
                action='store',
                help='Specify delegate sum report file instead of making HTTP \
request when using `elex delegates`'
            )),
            (['--delegate-super-file'], dict(
                action='store',
                help='Specify delegate super report file instead of making \
HTTP request when using `elex delegates`'
            )),
            (['--format-json'], dict(
                action='store_true',
                help='Pretty print JSON when using `-o json`.'
            )),
            (['-v', '--version'], dict(
                action='version',
                version=BANNER
            )),
            (['--results-level'], dict(
                action='store',
                help='Specify reporting level for results',
                default='ru'
            )),
            (['--set-zero-counts'], dict(
                action='store_true',
                help='Override results with zeros; omits the winner indicator.\
Sets the vote, delegate, and reporting precinct counts to zero.',
                default=False
            )),
            (['--local-only'], dict(
                action='store_false',
                help='Limit results to local-level results only.',
                default=None
            )),
            (['--with-timestamp'], dict(
                action='store_true',
                help='Append a `timestamp` column to each row of data output with current\
                      system timestamp.',
            )),
            (['--batch-name'], dict(
                action='store',
                help='Specify a value for a `batchname` column to append to each row.',
            )),
        ]

    @expose(hide=True)
    def default(self):
        """
        Print help
        """
        self.app.args.print_help()

    @expose(help="Get races")
    @require_ap_api_key
    @require_date_argument
    def races(self):
        """
        Initialize races
        """
        data = self.app.election.races
        self.app.log.info(
            'Getting races for election {0}'.format(
                self.app.election.electiondate
            )
        )
        if self.app.election._response:
            self.app.log.debug(
                'Elex API URL: {0}'.format(self.app.election._response.url)
            )
        self.app.render(data)

    @expose(help="Get reporting units")
    @require_ap_api_key
    @require_date_argument
    def reporting_units(self):
        """
        Initialize reporting units
        """
        data = self.app.election.reporting_units
        self.app.log.info(
            'Getting reporting units for election {0}'.format(
                self.app.election.electiondate
            )
        )
        if self.app.election._response:
            self.app.log.debug(
                'Elex API URL: {0}'.format(self.app.election._response.url)
            )
        self.app.render(data)

    @expose(help="Get candidate reporting units (without results)")
    @require_ap_api_key
    @require_date_argument
    def candidate_reporting_units(self):
        """
        Initialize reporting units
        """
        data = self.app.election.candidate_reporting_units
        self.app.log.info(
            'Getting candidate reporting units for election {0}'.format(
                self.app.election.electiondate
            )
        )
        if self.app.election._response:
            self.app.log.debug(
                'Elex API URL: {0}'.format(self.app.election._response.url)
            )
        self.app.render(data)

    @expose(help="Get candidates")
    @require_ap_api_key
    @require_date_argument
    def candidates(self):
        """
        Initialize reporting units
        """
        data = self.app.election.candidates
        self.app.log.info(
            'Getting candidates for election {0}'.format(
                self.app.election.electiondate
            )
        )
        if self.app.election._response:
            self.app.log.debug(
                'Elex API URL: {0}'.format(self.app.election._response.url)
            )
        self.app.render(data)

    @expose(help="Get ballot measures")
    @require_ap_api_key
    @require_date_argument
    def ballot_measures(self):
        """
        Initialize reporting units
        """
        data = self.app.election.ballot_measures
        self.app.log.info(
            'Getting ballot measures for election {0}'.format(
                self.app.election.electiondate
            )
        )
        if self.app.election._response:
            self.app.log.debug(
                'Elex API URL: {0}'.format(self.app.election._response.url)
            )
        self.app.render(data)

    @expose(help="Get results")
    @require_ap_api_key
    @require_date_argument
    def results(self):
        """
        Initialize reporting units
        """
        data = self.app.election.results
        self.app.log.info('Getting results for election {0}'.format(
            self.app.election.electiondate
        ))
        if self.app.election._response:
            self.app.log.debug(
                'Elex API URL: {0}'.format(self.app.election._response.url)
            )
        self.app.render(data)

    @expose(help="Get list of available elections")
    @require_ap_api_key
    def elections(self):
        """
        Initialize reporting units
        """
        self.app.log.info('Getting election list')
        elections = Elections().get_elections(
            datafile=self.app.pargs.data_file
        )
        self.app.render(elections)

    @expose(help="Get all delegate reports")
    @require_ap_api_key
    def delegates(self):
        """
        Provide all delegate reports
        """
        self.app.log.info('Getting delegate reports')
        if (
            self.app.pargs.delegate_super_file and
            self.app.pargs.delegate_sum_file
        ):
            report = DelegateReport(
                delsuper_datafile=self.app.pargs.delegate_super_file,
                delsum_datafile=self.app.pargs.delegate_sum_file
            )
        else:
            self.app.log.debug(
                'Elex delegate cache location: {0}'.format(DELEGATE_REPORT_ID_CACHE_FILE)
            )
            report = DelegateReport()

        self.app.render(report.candidate_objects)

    @expose(help="Get the next election (if date is specified, will be \
relative to that date, otherwise will use today's date)")
    @require_ap_api_key
    def next_election(self):
        """
        Initialize reporting units
        """
        self.app.log.info('Getting next election')
        if len(self.app.pargs.date):
            electiondate = self.app.pargs.date[0]
        else:
            electiondate = None
        election = Elections().get_next_election(
            datafile=self.app.pargs.data_file,
            electiondate=electiondate
        )
        if election is None:
            self.app.log.error('No next election')
            self.app.close(1)

        self.app.render(election)

    @expose(help="Clear the delegate report ID cache.")
    def clear_delegate_cache(self):
        self.app.log.info('Deleting delegate report ID cache ({0})'.format(DELEGATE_REPORT_ID_CACHE_FILE))
        clear_delegate_cache()


class ElexApp(CementApp):
    class Meta:
        label = 'elex'
        base_controller = ElexBaseController
        hooks = [
            ('post_argument_parsing', add_election_hook),
        ]
        extensions = [
            'elex.cli.ext_csv',
            'elex.cli.ext_json'
        ]
        output_handler = 'csv'

        handler_override_options = dict(
            output=(['-o'], dict(help='output format (default: csv)')),
        )
        log_handler = LoggingLogHandler(
            console_format=LOG_FORMAT,
            file_format=LOG_FORMAT
        )


def main():
    with ElexApp() as app:
        app.run()
