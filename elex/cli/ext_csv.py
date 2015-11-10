import csv
import sys

from cement.core import handler, output


class CSVOutputHandler(output.CementOutputHandler):
    class Meta:
        label = 'csv'
        overridable = True

    def render(self, data, template=None):
        fields = data[0].__dict__.keys()
        fields.sort()

        try:
            writer = csv.writer(sys.stdout)
            writer.writerow([field for field in fields if (field != 'reportingunits' and field != 'candidates')])

            for row in data:
                writer.writerow([getattr(row, field) for field in fields if (field != 'reportingunits' and field != 'candidates')])

        except IOError:
            # Handle pipes that could close before output is done, see http://stackoverflow.com/questions/15793886/
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

