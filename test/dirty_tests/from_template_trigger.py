from aot.model.effect import *
from aot.model.trigger import Trigger
from aot.model.enums.sizes import Size
from aot.model.scenario import Scenario
from aot.utilities.configuration import Configuration
import logging
from test.test_api.compare import compare_scenario_files

logging.basicConfig(level=logging.DEBUG)
C = Configuration("test/dirty_tests/config.json")

scn = Scenario(size=Size.GIANT)
scn.load_template(Size.GIANT)

scn.add(Trigger("Trigger 0",enable=1).then_(SendInstruction(message="Hello instruction !!!! (from true file)")))
scn.add(Trigger("Trigger 1",enable=1).then_(SendInstruction(message="Hello instruction 2 !!!! (from true file)")))

scn.save(C.game_path_scenario, "test_instruction_from_scratch")

copy = Scenario(size=Size.GIANT)
copy.load(C.game_path_scenario, "test_instruction_from_scratch")
true = Scenario(size=Size.GIANT)
true.load(C.game_path_scenario, "hello_instruction")

compare_scenario_files(copy, true, header=True)

compare_scenario_files(copy, true, header=False)
