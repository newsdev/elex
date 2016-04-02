import json
import sys
import time
from bson import json_util
from cement.core import handler, output


class ElexJSONOutputHandler(output.CementOutputHandler):
    """
    A custom JSON output handler
    """
    class Meta:
        label = 'json'
        overridable = True

    def render(self, data, template=None):
        if not isinstance(data, (list, tuple)):
            data = [data]

        if len(data) == 0:
            return

        try:
            kwargs = {}
            if self.app.pargs.format_json:
                kwargs['sort_keys'] = True
                kwargs['indent'] = 4

            if self.app.pargs.with_timestamp:
                now = time.time()

            json_data = []
            for obj in data:
                row = obj.serialize()
                if self.app.pargs.with_timestamp:
                    row['timestamp'] = str(int(now))
                if self.app.pargs.batch_name:
                    row['batchname'] = self.app.pargs.batch_name
                json_data.append(row)

            json.dump(
                json_data,
                sys.stdout,
                default=json_util.default,
                **kwargs
            )
        except IOError:
            # Handle pipes that could close before output is done.
            # See http://stackoverflow.com/questions/15793886/
            try:
                sys.stdout.close()
            except IOError:
                pass
            try:
                sys.stderr.close()
            except IOError:
                pass


def load(app):
    handler.register(ElexJSONOutputHandler)
