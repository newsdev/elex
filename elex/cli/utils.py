from dateutil import parser

def parse_date(datestring):
    """
    Parse many date formats into an AP friendly format.
    """
    dateobj = parser.parse(datestring)
    return dateobj.strftime('%Y-%m-%d')
