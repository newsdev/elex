import csv
import json
import sys

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from clint.textui import puts
from dateutil import parser
from elex.parser import api

def _parse_date(datestring, app):
    dateobj = parser.parse(datestring)
    return dateobj.strftime('%Y-%m-%d')


def process_date_hook(app):
    if len(app.argv):
        try:
            app.argv[-1] = _parse_date(app.argv[-1], app)
        except ValueError:
            puts('"{0}" could not be recognized as a date.\n'.format(app.argv[-1]))
            app.args.print_help()
            app.close()
    else:
        puts('Please specify an election date and optional command (e.g. `elex init 2015-11-03`)\n')
        app.args.print_help()
        app.close()


def add_races_hook(app):
    app.election = api.Election(electiondate=app.pargs.date[0], testresults=False, liveresults=True, is_test=False)
    app.race_data = app.election.get_races(omitResults=False, level="ru", test=False)


class ElexBaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = "Get and process AP elections data"
        arguments = [
            (['date'], dict(
                nargs=1,
                action='store',
                help='Election date (e.g. "2015-11-03"; most common date formats accepted).'
            )),
        ]

    @expose(hide=True)
    def default(self):
        print self.app.pargs.date[0]

    @expose(help="Intialize races")
    def init_races(self):
        races, reporting_units, candidate_reporting_units = self.app.election.get_units(self.app.race_data)
        writer = csv.writer(sys.stdout)

        writer.writerow(('office name', 'seat name', 'seat num'))
        for race in races:
            writer.writerow((race.officename, race.seatname, race.seatnum))


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
