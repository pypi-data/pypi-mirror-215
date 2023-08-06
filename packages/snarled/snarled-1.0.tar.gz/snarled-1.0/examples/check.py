"""
Example code for checking connectivity in a layout by using `snarled`
"""
import logging

import snarled
from snarled.types import layer_t


logging.basicConfig()
logging.getLogger('snarled').setLevel(logging.INFO)

# How are the conductors connected to each other?
connectivity = [
    ((1, 0), (1, 2), (2, 0)),   # M1 to M2 (via V12)
    ((1, 0), (1, 3), (3, 0)),   # M1 to M3 (via V13)
    ((2, 0), (2, 3), (3, 0)),   # M2 to M3 (via V23)
    ]

# What labels should be loaded, and which geometry layers should they apply to?
labels_map: dict[layer_t, layer_t] = {
    (1, 0): (1, 0),
    (2, 0): (2, 0),
    (3, 0): (3, 0),
    }

filename = 'connectivity.oas'

nets = snarled.trace_layout(filename, connectivity, topcell='top', labels_map=labels_map)
result = snarled.TraceAnalysis(nets)

print('\n')
print(result)
