from aot.model.enums.sizes import Size
from aot.model.scenario import Scenario
from aot.utilities.configuration import Configuration

from aot.model.enums import constants
import logging

from test.test_api.compare import compare_scenario_files

C = Configuration("config.json")

logging.basicConfig(level=logging.DEBUG)

scn = Scenario(header_type=constants.HT_AOE2_DE, size=Size.GIANT)
scn.load(C.game_path_scenario, "debug_de")
scn.save(C.game_path_scenario, "debug_de_save")

scn_to_check = Scenario(header_type=constants.HT_AOE2_DE, size=Size.GIANT)
scn_to_check.load(C.game_path_scenario, "debug_de_save")

true_scn = Scenario(header_type=constants.HT_AOE2_DE, size=Size.GIANT)
true_scn.load(C.game_path_scenario, "debug_de")

compare_scenario_files(scn_to_check,true_scn)