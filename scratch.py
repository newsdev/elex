from elex.api import *

gr = USGovernorTrendReport()
print [o.serialize() for o in gr.parties]

sr = USSenateTrendReport()
print [o.serialize() for o in sr.parties]

hr = USHouseTrendReport()
print [o.serialize() for o in hr.parties]
