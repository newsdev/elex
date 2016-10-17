from elex import __version__ as VERSION

LOG_FORMAT = '%(asctime)s (%(levelname)s) %(name)s \
(v' + VERSION + ') : %(message)s'

BANNER = """
Elex version {0}
""".format(VERSION)
