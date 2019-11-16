import unittest

from test.compare import compare_scenario_files
from aot.utilities.configuration import Configuration
from aot import Scenario, Size
from aot.model.enums import constants
import logging

C = Configuration("aot/test/configuration_de.json")

logging.basicConfig(level=logging.DEBUG)


class TestFromScratch(unittest.TestCase):

    def setUp(self):
        self.scn = Scenario(header_type=constants.HT_AOE2_DE, size=Size.GIANT)
        self.scn_true = Scenario(header_type=constants.HT_AOE2_DE, size=Size.GIANT)
        self.scn_true.load(C.temp_path, "giant_de")

    def test_load(self):
        diffs = compare_scenario_files(self.scn,self.scn_true)
        print(diffs)


if __name__ == '__main__':
    unittest.main()
