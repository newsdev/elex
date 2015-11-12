from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.ext.ext_logging import LoggingLogHandler
from elex.cli.hooks import add_election_hook
from elex.cli.decorators import require_date

LOG_FORMAT = "%(asctime)s (%(levelname)s) %(namespace)s : %(message)s"


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

    @expose(help="Initialize races")
    @require_date
    def init_races(self):
        """
        Initialize races
        """
        self.app.log.info('Running init_races for election {0}'
            .format(self.app.election.electiondate))
        self.app.render(self.app.election.races)

    @expose(help="Initialize reporting units")
    @require_date
    def init_reporting_units(self):
        """
        Initialize reporting units
        """
        self.app.log.info('Running init_reporting_units for election {0}'
            .format(self.app.election.electiondate))
        self.app.render(self.app.election.reporting_units)

    @expose(help="Initialize candidate reporting units")
    @require_date
    def init_candidate_reporting_units(self):
        """
        Initialize reporting units
        """
        self.app.log.info('Running init_candidate_reporting_units for election {0}'
            .format(self.app.election.electiondate))
        self.app.render(self.app.election.candidate_reporting_units)

    @expose(help="Initialize candidates")
    @require_date
    def init_candidates(self):
        """
        Initialize reporting units
        """
        self.app.log.info('Running init_candidates for election {0}'
            .format(self.app.election.electiondate))
        self.app.render(self.app.election.candidates)

    @expose(help="Initialize ballot positions")
    @require_date
    def init_ballot_positions(self):
        """
        Initialize reporting units
        """
        self.app.log.info('Running init_ballot_positions for election {0}'
            .format(self.app.election.electiondate))
        self.app.render(self.app.election.ballot_positions)

    @expose(help="Get results")
    @require_date
    def get_results(self):
        """
        Initialize reporting units
        """
        self.app.log.info('Running get-results for election {0}'
            .format(self.app.election.electiondate))
        self.app.render(self.app.election.results)

    @expose(help="Show list of elections known to the API")
    def elections(self):
        """
        Initialize reporting units
        """
        self.app.log.info('Getting election list')
        elections = self.app.election.get_elections()
        self.app.render(elections)

    @expose(help="Print next election")
    def next_election(self):
        """
        Initialize reporting units
        """
        self.app.log.info('Getting next election')
        election = self.app.election.get_next_election()
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
