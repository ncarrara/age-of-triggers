import unittest

from test.compare import compare_scenario_files
from aot.utilities.configuration import Configuration
from aot import Scenario, Size
from aot.model.enums import constants
import logging

C = Configuration("config.json")

logging.basicConfig(level=logging.DEBUG)

scn = Scenario(header_type=constants.HT_AOE2_DE, size=Size.GIANT)
scn.load(C.test_path_scenario, "giant_de")