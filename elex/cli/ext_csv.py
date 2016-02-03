import csv
import sys
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

        try:
            writer = csv.writer(sys.stdout)
            for i, row in enumerate(data):
                if i == 0:
                    writer.writerow(row.serialize().keys())
                writer.writerow(row.serialize().values())
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
