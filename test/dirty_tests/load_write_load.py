from aot.model.enums.sizes import Size
from aot.model.scenario import Scenario
from aot.utilities.configuration import Configuration

from aot.model.enums import constants
import logging

from test.test_api.compare import compare_scenario_files
import logging

logger = logging.getLogger(__name__)
C = Configuration("config.json")

#basename = "debug_de"
basename = "fresh_scenario"
#basename = "fresh"

logging.basicConfig(level=logging.DEBUG)

scn = Scenario(header_type=constants.HT_AOE2_DE, size=Size.GIANT)
scn.load(C.game_path_scenario, basename)
scn.save(C.game_path_scenario, basename+"_save")

scn_to_check = Scenario(header_type=constants.HT_AOE2_DE, size=Size.GIANT)
scn_to_check.load(C.game_path_scenario, basename+"_save")

true_scn = Scenario(header_type=constants.HT_AOE2_DE, size=Size.GIANT)
true_scn.load(C.game_path_scenario, basename)

logger.debug("---------------------------------------")
logger.debug("---------------------------------------")
logger.debug("---------------------------------------")
logger.debug("---------------------------------------")

compare_scenario_files(scn_to_check,true_scn)