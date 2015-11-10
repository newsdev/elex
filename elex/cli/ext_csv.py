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

        writer = csv.writer(sys.stdout)
        writer.writerow([field for field in fields if (field != 'reportingunits' and field != 'candidates')])

        for row in data:
            writer.writerow([getattr(row, field) for field in fields if (field != 'reportingunits' and field != 'candidates')])


def load(app):
    handler.register(CSVOutputHandler)

