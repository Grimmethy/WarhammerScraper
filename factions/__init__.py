from .aos_destruction import _DESTRUCTION
from .aos_death import _DEATH
from .aos_order import _ORDER
from .aos_chaos import _CHAOS
from .wh40k import _WH40K
from .horus_heresy import _HORUS_HERESY

FACTIONS_AOS = {**_DESTRUCTION, **_DEATH, **_ORDER, **_CHAOS}
FACTIONS_40K = _WH40K
FACTIONS_HH  = _HORUS_HERESY
FACTIONS     = {**FACTIONS_AOS, **FACTIONS_40K, **FACTIONS_HH}
