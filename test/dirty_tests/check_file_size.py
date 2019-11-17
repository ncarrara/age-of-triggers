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

basename = "fresh"

logging.basicConfig(level=logging.DEBUG)

true = Scenario(header_type=constants.HT_AOE2_DE, size=Size.GIANT)
true.load("../scenarios", basename, "../tmp/true.decompressed")
true.save("../tmp", basename, change_timestamp=False)
copy = Scenario(header_type=constants.HT_AOE2_DE, size=Size.GIANT)
copy.load("../tmp", basename, "../tmp/copy.decompressed")

differences = compare_scenario_files(copy, true)

assert len(differences) == 0, "Variables are different for those keys " + str(differences)

copy_size = os.path.getsize("../tmp/copy.decompressed")
true_size = os.path.getsize("../tmp/true.decompressed")
assert copy_size == true_size

true_bytes = None

with open("../scenarios/" + basename + ".aoe2scenario", "rb") as f:
    true_bytes = f.read()

copy_bytes = None
with open("../tmp/" + basename + ".aoe2scenario", "rb") as f:
    copy_bytes = f.read()

for i, (true, copy) in enumerate(zip(true_bytes, copy_bytes)):
    true_size = os.path.getsize("../tmp/true.decompressed")
    assert true == copy, "[byte {}] file are different, {} should be {}".format(i, copy, true)
