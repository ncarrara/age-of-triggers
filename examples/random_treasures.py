import numpy as np

import logging
from aot import Scenario
from aot.metatriggers.metatrigger_treasure import TreasureLoot, TreasureQuarry, TreasureLumber
from aot.utilities.configuration import Configuration

logging.basicConfig(level=logging.DEBUG)
C = Configuration("configuration_de.json")
scn = Scenario()

for _ in range(100):
    n = np.random.random()
    x = int(np.random.random() * scn.get_width())
    y = int(np.random.random() * scn.get_height())
    if n < 0.33:
        treasure = TreasureLoot(x, y, 500)
    elif n < 0.66:
        treasure = TreasureLumber(x, y, 500)
    else:
        treasure = TreasureQuarry(x, y, 500)
    scn.add(treasure)

scn.save(C.game_path_scenario, "random_tresures")
