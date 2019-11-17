from aot.model.enums.sizes import Size
from aot.model.scenario import Scenario
from aot.utilities.configuration import Configuration

from aot.model.enums import constants
import logging

#basename = "debug_de"
basename = "fresh_scenario"
#basename = "fresh_scenario2"
basename = "fresh_scenario3"

C = Configuration("config.json")

logging.basicConfig(level=logging.DEBUG)

scn = Scenario(header_type=constants.HT_AOE2_DE, size=Size.GIANT)
scn.load(C.game_path_scenario, basename)