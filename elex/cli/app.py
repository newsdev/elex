
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.ext.ext_logging import LoggingLogHandler
from elex import __version__ as VERSION
from elex.cli.hooks import add_election_hook
from elex.cli.decorators import require_date_argument, require_ap_api_key

LOG_FORMAT = '%(asctime)s (%(levelname)s) %(namespace)s (v{0}) : %(message)s'.format(VERSION)

BANNER = """
NYT AP Elections version {0}
""".format(VERSION)


class ElexBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = "Get and process AP elections data"
        arguments = [
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
                help='Specify data file instead of making HTTP request'
            )),
            (['--format-json'], dict(
                action='store_true',
                help='Pretty print JSON (only when using -o json)'
            )),
            (['-v', '--version'], dict(
                action='version',
                version=BANNER
            )),
            (['date'], dict(
                nargs='*',
                action='store',
                help='Election date (e.g. "2015-11-03"; most common date formats accepted).'
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
        self.app.log.info('Getting races for election {0}'
            .format(self.app.election.electiondate))
        self.app.render(self.app.election.races)

    @expose(help="Get reporting units")
    @require_ap_api_key
    @require_date_argument
    def reporting_units(self):
        """
        Initialize reporting units
        """
        self.app.log.info('Getting reporting units for election {0}'
            .format(self.app.election.electiondate))
        self.app.render(self.app.election.reporting_units)

    @expose(help="Get candidate reporting units (without results)")
    @require_ap_api_key
    @require_date_argument
    def candidate_reporting_units(self):
        """
        Initialize reporting units
        """
        self.app.log.info('Getting candidate reporting units for election {0}'
            .format(self.app.election.electiondate))
        self.app.render(self.app.election.candidate_reporting_units)

    @expose(help="Get candidates")
    @require_ap_api_key
    @require_date_argument
    def candidates(self):
        """
        Initialize reporting units
        """
        self.app.log.info('Getting candidates for election {0}'
            .format(self.app.election.electiondate))
        self.app.render(self.app.election.candidates)

    @expose(help="Get ballot positions (also known as ballot issues)")
    @require_ap_api_key
    @require_date_argument
    def ballot_measures(self):
        """
        Initialize reporting units
        """
        self.app.log.info('Getting ballot positions for election {0}'
            .format(self.app.election.electiondate))
        self.app.render(self.app.election.ballot_measures)

    @expose(help="Get results")
    @require_ap_api_key
    @require_date_argument
    def results(self):
        """
        Initialize reporting units
        """
        self.app.log.info('Getting results for election {0}'
            .format(self.app.election.electiondate))
        self.app.render(self.app.election.results)

    @expose(help="Get list of available elections")
    @require_ap_api_key
    def elections(self):
        """
        Initialize reporting units
        """
        self.app.log.info('Getting election list')
        elections = self.app.election.get_elections(datafile=self.app.pargs.data_file)
        self.app.render(elections)

    @expose(help="Get the next election (if date is specified, will be relative to that date, otherwise will use today's date)")
    @require_ap_api_key
    def next_election(self):
        """
        Initialize reporting units
        """
        self.app.log.info('Getting next election')
        election = self.app.election.get_next_election(datafile=self.app.pargs.data_file, electiondate=self.app.pargs.date[0])
        self.app.render(election)


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
        log_handler = LoggingLogHandler(console_format=LOG_FORMAT, file_format=LOG_FORMAT)


def main():
    with ElexApp() as app:
        app.run()
