import csv
import sys
import time
from cement.core import handler, output


class CSVOutputHandler(output.CementOutputHandler):
    """
    A custom CSV output handler
    """
    class Meta:
        label = 'csv'
        overridable = True

    def render(self, data, template=None):
        if not isinstance(data, (list, tuple)):
            data = [data]

        if len(data) == 0:
            return

        now = time.time()

        try:
            # Properly terminate lines for Windows and Excel.
            # See: https://github.com/newsdev/elex/issues/232
            writer = csv.writer(sys.stdout, lineterminator='\n')
            for i, obj in enumerate(data):
                row = obj.serialize()
                if self.app.pargs.with_timestamp:
                    row['timestamp'] = str(int(now))
                if i == 0:
                    writer.writerow(row.keys())
                writer.writerow(row.values())
        except IOError:
            # Handle pipes that could close before output is done.
            # See: http://stackoverflow.com/questions/15793886/
            try:
                sys.stdout.close()
            except IOError:
                pass
            try:
                sys.stderr.close()
            except IOError:
                pass


def load(app):
    handler.register(CSVOutputHandler)
