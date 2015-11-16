import csv
import sys
import tests

from cStringIO import StringIO
from elex.cli.app import ElexApp

DATA_FILE = 'tests/data/20151103_national.json'
ELECTIONS_DATA_FILE = 'tests/data/00000000_elections.json'
TEST_COMMANDS = ['races', 'candidates', 'reporting-units', 'candidate-reporting-units']


class ElexCLITestMeta(type):
    def __new__(mcs, name, bases, dict):

        def gen_test(command, subcommand):
            """
            Dynamically generate a test function, like test_init_races
            """
            def test(self):
                cli_fields, cli_data = self._test_command(argv=[subcommand])
                api_data = getattr(self, command.replace('-', '_'))
                api_fields = api_data[0].serialize().keys()
                self.assertEqual(cli_fields, api_fields)
                self.assertEqual(len(cli_data), len(api_data))
                for i, row in enumerate(cli_data):
                    for k, v in api_data[i].serialize().items():
                        if v is None:
                            v = ''
                        self.assertEqual(row[k], str(v))

            return test

        for command in TEST_COMMANDS:
            subcommand = 'init-{0}'.format(command)
            test_name = 'test_{0}'.format(subcommand.replace('-', '_'))
            dict[test_name] = gen_test(command, subcommand)

        return type.__new__(mcs, name, bases, dict)


class ElexCLITestCase(tests.ElectionResultsTestCase):
    __metaclass__ = ElexCLITestMeta

    def test_next_election_fields(self):
        """
        Test `elex elections` field names
        """
        fields, data = self._test_command(argv=['elections'], datafile=ELECTIONS_DATA_FILE)
        self.assertEqual(fields, ['electiondate', 'liveresults', 'testresults'])

    def test_next_election_data(self):
        """
        Test `elex next-election` field names
        """
        fields, data = self._test_command(argv=['next-election'], datafile=ELECTIONS_DATA_FILE)
        # @TODO implement with fixed "now" date
        pass

    def _test_command(self, argv, datafile=DATA_FILE):
        """
        Execute an `elex` sub-command; returns fieldnames and rows
        """
        stdout_backup = sys.stdout
        sys.stdout = StringIO()

        app = ElexApp(argv=argv + ['--data-file', datafile])
        app.setup()
        app.log.set_level('FATAL')
        app.run()
        lines = sys.stdout.getvalue().split('\n')
        reader = csv.DictReader(lines)

        sys.stdout.close()
        sys.stdout = stdout_backup

        return reader.fieldnames, list(reader)
