import csv
import json
import sys

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
                nargs=1,
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

        fields = races[0].__dict__.keys()
        fields.sort()

        writer = csv.writer(sys.stdout)
        writer.writerow([field for field in fields if (field != 'reportingunits' and field != 'candidates')])
        for race in races:
            writer.writerow([getattr(race, field) for field in fields if (field != 'reportingunits' and field != 'candidates')])

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

        fields = reporting_units[0].__dict__.keys()
        fields.sort()

        writer = csv.writer(sys.stdout)
        writer.writerow(fields)
        for ru in reporting_units:
            writer.writerow([getattr(ru, field) for field in fields])


class ElexApp(CementApp):
    class Meta:
        label = 'elex'
        base_controller = ElexBaseController
        hooks = [
            ('pre_argument_parsing', process_date_hook),
            ('post_argument_parsing', add_races_hook)
        ]


def main():
    with ElexApp() as app:
        app.run()
