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

# basename = "fresh"

logging.basicConfig(level=logging.DEBUG)

# true = Scenario( size=Size.GIANT)
# true.load(C.game_path_scenario, "age-of-total-war 0.02")
copy = Scenario(size=Size.GIANT)
copy.load(C.game_path_scenario, "age-of-total-war xaxa")

# differences = compare_scenario_files(copy, true, header=True)
# print(differences)
# differences = compare_scenario_files(copy, true)
# print(differences)