import unittest

from test.compare import compare_scenario_files
from aot.utilities.configuration import Configuration
from aot import Scenario, logging

logger = logging.getLogger(__name__)

C = Configuration("config.json")


def read_write_and_reread(basename):
    scn = Scenario()
    scn.load(C.test_path_scenario, basename)
    scn.save(C.temp_path, basename + "_copy")

    true = Scenario()
    true.load(C.test_path_scenario, basename)

    copy = Scenario()
    copy.load(C.temp_path, basename + "_copy")
    diffs = compare_scenario_files(copy, true)
    return diffs


class TestFromScratch(unittest.TestCase):

    def test_DEoldworldIA(self):
        diffs = read_write_and_reread("DEoldworldIA")
        print(diffs)


if __name__ == '__main__':
    unittest.main()
