from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from elex.cli.hooks import process_date_hook, add_races_hook


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
            (['date'], dict(
                nargs='*',
                action='store',
                help='Election date (e.g. "2015-11-03"; most common date formats accepted).'
            )),
        ]

    @expose(help="Initialize races")
    def init_races(self):
        """
        Initialize races
        """
        race_data = self.app.election.get_races(
            omitResults=False,
            level="ru",
            test=self.app.pargs.test
        )
        races, reporting_units, candidate_reporting_units = self.app.election.get_units(race_data)
        self.app.render(races)

    @expose(help="Initialize reporting units")
    def init_reporting_units(self):
        """
        Initialize reporting units
        """
        race_data = self.app.election.get_races(
            omitResults=False,
            level="ru",
            test=self.app.pargs.test
        )
        races, reporting_units, candidate_reporting_units = self.app.election.get_units(race_data)
        self.app.render(reporting_units)


class ElexApp(CementApp):
    class Meta:
        label = 'elex'
        base_controller = ElexBaseController
        hooks = [
            ('post_argument_parsing', process_date_hook),
            ('post_argument_parsing', add_races_hook)
        ]
        extensions = ['elex.cli.ext_csv', 'json']
        output_handler = 'csv'

        handler_override_options = dict(
            output=(['-o'], dict(help='output format (default: csv)')),
        )


def main():
    with ElexApp() as app:
        app.run()
