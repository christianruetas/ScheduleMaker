from Optimizations.DayOff import DayOff
from Optimizations.EarlyEnd import EarlyEnd
from Optimizations.InPerson import InPerson
from Optimizations.InPersonNot import Online
from Optimizations.OpenSeats import OpenSeats
from Optimizations.Balanced import Balanced

ENABLED_OPTIMIZER_OBJECT_LIST = [EarlyEnd(), DayOff(), InPerson(), Online(), OpenSeats(), Balanced()]
# ^^^ ALSO UPDATE: FullProcess/OptimizerRequestStructure.py -> OptimizerRequest.build_request()
