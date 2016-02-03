from dateutil import parser as dateutil_parser


def parse_date(datestring):
    """
    Parse many date formats into an AP friendly format.
    """
    dateobj = dateutil_parser.parse(datestring)
    return dateobj.strftime('%Y-%m-%d')
