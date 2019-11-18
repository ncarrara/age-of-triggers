from aot.model.enums.sizes import Size
from aot.model.scenario import Scenario
from aot.utilities.configuration import Configuration

from aot.model.enums import constants
import logging


basename = "fresh_scenario"
#basename = "fresh_scenario2"
basename = "fresh_scenario3"
basename = "large"

basename = "debug_de"
basename = "large2"
basename = "template_small"
C = Configuration("test/dirty_tests/config.json")

logging.basicConfig(level=logging.DEBUG)

scn = Scenario()
scn.load(C.game_path_scenario, basename)