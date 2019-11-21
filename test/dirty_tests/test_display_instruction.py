from aot.model.enums.sizes import Size
from aot.model.scenario import Scenario
from aot.utilities.configuration import Configuration
import logging
from test.test_api.compare import compare_scenario_files

logger = logging.getLogger(__name__)
C = Configuration("config.json")

logging.basicConfig(level=logging.DEBUG)

copy = Scenario(size=Size.GIANT)
copy.load(C.game_path_scenario, "test_display_instruction")
copy.save(C.game_path_scenario,"test_display_instruction_copy")
true = Scenario(size=Size.GIANT)
true.load(C.game_path_scenario, "test_display_instruction")

copy = Scenario(size=Size.GIANT)
copy.load(C.game_path_scenario, "test_display_instruction_copy")

print(compare_scenario_files(copy,true,header=True))
print(compare_scenario_files(copy,true,header=False))