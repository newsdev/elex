import csv
import sys

from cStringIO import StringIO
from cement.utils import test
from elex.cli.app import ElexApp

DATA_FILE = 'tests/data/20151103_national.json'
ELECTIONS_DATA_FILE = 'tests/data/00000000_elections.json'


class ElexCLITestCase(test.CementTestCase):
    app_class = ElexApp

    def setUp(self):
        """
        Reassign stdout for capture
        """
        self.stdout_backup = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        """
        Restore stdout
        """
        sys.stdout.close()
        sys.stdout = self.stdout_backup

    def test_init_races_fields(self):
        """
        Test `elex init-races` field names
        """
        fields, data = self._test_command(argv=['init-races'])
        self.assertEqual(fields, ['raceid', 'racetype', 'racetypeid', 'description', 'initialization_data', 'lastupdated', 'national', 'officeid', 'officename', 'party', 'seatname', 'seatnum', 'statename', 'statepostal', 'test', 'uncontested'])

    def test_init_races_data(self):
        """
        Test `elex init-races` data
        """
        fields, races = self._test_command(argv=['init-races'])
        race = races[-1]
        self.assertEqual(race['national'], 'True')
        self.assertEqual(race['officeid'], 'G')
        self.assertEqual(race['officename'], 'Governor')
        self.assertEqual(race['raceid'], '18525')
        self.assertEqual(race['racetype'], 'General')
        self.assertEqual(race['racetypeid'], 'G')

    def test_elections_fields(self):
        """
        Test `elex elections` field names
        """
        fields, data = self._test_command(argv=['elections'], datafile=ELECTIONS_DATA_FILE)
        self.assertEqual(fields, ['electiondate', 'liveresults', 'testresults'])

    def test_elections_data(self):
        """
        Test `elex elections` data
        """
        fields, data = self._test_command(argv=['elections'], datafile=ELECTIONS_DATA_FILE)
        election = data[-1]
        self.assertEqual(election['electiondate'], '2016-02-09')
        self.assertEqual(election['liveresults'], 'False')
        self.assertEqual(election['testresults'], 'True')

    def _test_command(self, argv, datafile=DATA_FILE):
        """
        Execute an app command
        """
        app = ElexApp(argv=argv + ['--data-file', datafile])
        app.setup()
        app.log.set_level('FATAL')
        app.run()
        lines = sys.stdout.getvalue().split('\n')
        reader = csv.DictReader(lines)
        return reader.fieldnames, list(reader)
