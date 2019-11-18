from aot.model.enums.sizes import Size
from aot.model.scenario import Scenario
from aot.utilities.configuration import Configuration

from aot.model.enums import constants
import logging

from test.test_api.compare import compare_scenario_files
import logging
import os

logger = logging.getLogger(__name__)
C = Configuration("config.json")

#basename = "debug_de"
#basename = "fresh_scenario"
basename = "fresh"

logging.basicConfig(level=logging.DEBUG)

scn = Scenario(header_type=constants.HT_AOE2_DE, size=Size.GIANT)
scn.load(C.game_path_scenario, basename)
scn.save("../tmp", basename)

scn_to_check = Scenario(header_type=constants.HT_AOE2_DE, size=Size.GIANT)
scn_to_check.load("../tmp", basename, path_decompressed_data="../tmp/copy.decompressed")

true_scn = Scenario(header_type=constants.HT_AOE2_DE, size=Size.GIANT)
true_scn.load(C.game_path_scenario, basename, path_decompressed_data="../tmp/true.decompressed")

logger.debug("---------------------------------------")
logger.debug("---------------------------------------")
logger.debug("---------------------------------------")
logger.debug("---------------------------------------")

copy_size = os.path.getsize("../tmp/copy.decompressed")
true_size = os.path.getsize("../tmp/true.decompressed")

print("copy_size={} true_size={} diff={} bytes".format(copy_size,true_size,true_size-copy_size))

compare_scenario_files(scn_to_check,true_scn)