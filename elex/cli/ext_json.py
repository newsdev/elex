import json
import sys
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

            json_data = [row.serialize() for row in data]
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
