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
basename = "debug_de"

logging.basicConfig(level=logging.DEBUG)

true = Scenario(header_type=constants.HT_AOE2_DE, size=Size.GIANT)
true.load("../scenarios", basename, "../tmp/true.header","../tmp/true.decompressed")
true.save("../tmp", basename, change_timestamp=False)
copy = Scenario(header_type=constants.HT_AOE2_DE, size=Size.GIANT)
copy.load("../tmp", basename, "../tmp/copy.header","../tmp/copy.decompressed")

differences = compare_scenario_files(copy, true)

assert len(differences) == 0, "Variables are different for those keys " + str(differences)

print("[OK] Variables")

copy_size = os.path.getsize("../tmp/copy.header")
true_size = os.path.getsize("../tmp/true.header")
assert copy_size == true_size, "HEADER copy_size={} != {}=true_size, diff={} bytes".format(copy_size,true_size,true_size-copy_size)

true_bytes = None

with open("../tmp/true.header", "rb") as f:
    true_bytes = f.read()

copy_bytes = None
with open("../tmp/copy.header", "rb") as f:
    copy_bytes = f.read()

for i, true in enumerate(true_bytes):
    copy = copy_bytes[i]
    assert true == copy, "[byte {}] header files are different, {} should be {}".format(i, copy, true)

print("[OK] Header")

copy_size = os.path.getsize("../tmp/copy.decompressed")
true_size = os.path.getsize("../tmp/true.decompressed")
print("true size decompressed",true_size)
print("copy size decompressed",copy_size)
assert copy_size == true_size, "copy_size={} != {}=true_size, diff={} bytes".format(copy_size,true_size,true_size-copy_size)



true_bytes = None

with open("../tmp/true.decompressed", "rb") as f:
    true_bytes = f.read()

copy_bytes = None
with open("../tmp/copy.decompressed", "rb") as f:
    copy_bytes = f.read()

for i, true in enumerate(true_bytes):
    #try:
    copy = copy_bytes[i]
    #except:
    #    print("comparaison failed at byte {}, all previous bytes were equals".format(i))
    #    print(bytes(true_bytes[i:]))
    #    exit()
    #if true != copy:

        #print("[byte {}] decompressed files are different, {} should be {}".format(i, copy, true))
    assert true == copy, "[byte {}] decompressed files are different, {} should be {}".format(i, copy, true)

print("[OK] Decompressed")








##############################################################
##############################################################
##############################################################
##############################################################
true_bytes = None

with open("../scenarios/" + basename + ".aoe2scenario", "rb") as f:
    true_bytes = f.read()

copy_bytes = None
with open("../tmp/" + basename + ".aoe2scenario", "rb") as f:
    copy_bytes = f.read()

assert len(true_bytes)==len(copy_bytes), "full file have different lenght,true={} != {}=copy".format(len(true_bytes),len(copy_bytes))

for i, (true, copy) in enumerate(zip(true_bytes, copy_bytes)):
    #if  true != copy:
    #    print("[byte {}] compressed file are different, {} should be {}".format(i, copy, true))
    assert true == copy, "[byte {}] full files are different, {} should be {}".format(i, copy, true)

print("[OK] Full file")