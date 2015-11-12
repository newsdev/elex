from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from elex.cli.hooks import add_election_hook
from elex.cli.decorators import require_date

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
            (['--format-json'], dict(
                action='store_true',
                help='Print print JSON (only when using -o json)'
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
        races, reporting_units, candidate_reporting_units = self._get_init_units()
        self.app.render(races)

    @expose(help="Initialize reporting units")
    @require_date
    def init_reporting_units(self):
        """
        Initialize reporting units
        """
        races, reporting_units, candidate_reporting_units = self._get_init_units()
        self.app.render(reporting_units)

    @expose(help="Initialize candidate reporting units")
    @require_date
    def init_candidate_reporting_units(self):
        """
        Initialize reporting units
        """
        races, reporting_units, candidate_reporting_units = self._get_init__units()
        self.app.render(candidate_reporting_units)

    @expose(help="Initialize candidates")
    @require_date
    def init_candidates(self):
        """
        Initialize reporting units
        """
        candidates, ballot_positions = self._get_init_uniques()
        self.app.render(candidates)

    @expose(help="Initialize ballot positions")
    @require_date
    def init_ballot_positions(self):
        """
        Initialize reporting units
        """
        candidates, ballot_positions = self._get_init_uniques()
        self.app.render(ballot_positions)

    @expose(help="Get results")
    @require_date
    def get_results(self):
        """
        Initialize reporting units
        """
        raw_races = self.app.election.get_raw_races(
            omitResults=False,
            level="ru",
            test=self.app.pargs.test
        )
        race_objs = self.app.election.get_race_objects(raw_races)
        races, reporting_units, candidate_reporting_units = self.app.election.get_units(race_objs)

        self.app.render(candidate_reporting_units)

    @expose(help="Show list of elections known to the API")
    def elections(self):
        """
        Initialize reporting units
        """
        elections = self.app.election.get_elections()
        self.app.render(elections)

    @expose(help="Print next election")
    def next_election(self):
        """
        Initialize reporting units
        """
        election = self.app.election.get_next_election()
        self.app.render(election)

    def _get_init_units(self):
        """
        Wrapper for Election.get_units()
        """
        raw_races = self.app.election.get_raw_races(
            omitResults=True,
            level="ru",
            test=self.app.pargs.test
        )
        race_objs = self.app.election.get_race_objects(raw_races)
        return self.app.election.get_units(race_objs)

    def _get_init_uniques(self):
        """
        Wrapper for Election.get_uniques()
        """
        raw_races = self.app.election.get_raw_races(
            omitResults=True,
            level="ru",
            test=self.app.pargs.test
        )
        race_objs = self.app.election.get_race_objects(raw_races)
        races, reporting_units, candidate_reporting_units = self.app.election.get_units(race_objs)
        return self.app.election.get_uniques(candidate_reporting_units)


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


def main():
    with ElexApp() as app:
        app.run()
