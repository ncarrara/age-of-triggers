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
basename = "debug_de"

logging.basicConfig(level=logging.DEBUG)

true = Scenario( size=Size.GIANT)
true.load("../scenarios", basename, "../tmp/true.header", "../tmp/true.decompressed")

true.save("../tmp", basename, change_timestamp=False)
true.save(C.game_path_scenario, basename + "_tmp", change_timestamp=True)
copy = Scenario(size=Size.GIANT)
copy.load("../tmp", basename, "../tmp/copy.header", "../tmp/copy.decompressed")

differences = compare_scenario_files(copy, true, header=True)
assert len(differences) == 0, "Variables from HEADER are different for those keys " + str(differences)
print("[OK] Variables header")

differences = compare_scenario_files(copy, true)

assert len(differences) == 0, "Variables are different for those keys " + str(differences)

print("[OK] Variables decompressed")

copy_size = os.path.getsize("../tmp/copy.header")
true_size = os.path.getsize("../tmp/true.header")
assert copy_size == true_size, "HEADER copy_size={} != {}=true_size, diff={} bytes".format(copy_size, true_size,
                                                                                           true_size - copy_size)
print("[OK] Header Sizes")
true_bytes = None

with open("../tmp/true.header", "rb") as f:
    true_bytes = f.read()

copy_bytes = None
with open("../tmp/copy.header", "rb") as f:
    copy_bytes = f.read()

for i, true_byte in enumerate(true_bytes):
    copy_byte = copy_bytes[i]
    assert true_byte == copy_byte, "[byte {}] header files are different, {} should be {}".format(i, copy_byte,
                                                                                                  true_byte)

print("[OK] Header")

copy_size = os.path.getsize("../tmp/copy.decompressed")
true_size = os.path.getsize("../tmp/true.decompressed")
assert copy_size == true_size, "copy_size={} != {}=true_size, diff={} bytes".format(copy_size, true_size,
                                                                                    true_size - copy_size)
print("[OK] Decompressed Sizes")
true_bytes = None
with open("../tmp/true.decompressed", "rb") as f:
    true_bytes = f.read()

copy_bytes = None
with open("../tmp/copy.decompressed", "rb") as f:
    copy_bytes = f.read()

for i, true_byte in enumerate(true_bytes):
    # i += true.header_length
    copy_byte = copy_bytes[i]
    if true_byte != copy_byte:
        for offset in true.variables.keys():
            if offset <= i + 1:
                key_copy,value_copy = copy.variables[offset]
                key_true,value_true = true.variables[offset]
                print("offset=<{}> \n{} >>> {} -- {}\n{} >>> {} -- {}".format(
                    offset,
                    key_true, str(value_true)[:50], str(value_true)[-50:],
                    key_copy, str(value_copy)[:50], str(value_copy)[-50:]))
                for j in range(len(str(value_true))):
                    assert str(value_true)[j]==str(value_copy)[j],"{} !={}".format(str(value_true)[j],str(value_copy)[j])
    assert true_byte == copy_byte, "[byte {}] decompressed files are different, {} should be {}" \
        .format(i, copy_byte, true_byte)

print("[OK] Decompressed byte by byte")

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

assert len(true_bytes) == len(copy_bytes), "full file have different lenght,true={} != {}=copy".format(len(true_bytes),
                                                                                                       len(copy_bytes))

for i, (true_byte, copy_byte) in enumerate(zip(true_bytes, copy_bytes)):
    # if  true != copy:
    #    print("[byte {}] compressed file are different, {} should be {}".format(i, copy, true))
    assert true_byte == copy_byte, "[byte {}] full files are different, {} should be {}".format(i, copy_byte, true_byte)

print("[OK] Full file")
