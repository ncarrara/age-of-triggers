from aot.meta_triggers.metatrigger import MetaTrigger
from aot.model.controller.background import Background
from aot.model.controller.cinematics import Cinematics
from aot.model.controller.goals import Goals
from aot.model.controller.map import Map
from aot.model.controller.messages import Messages
from aot.model.controller.players import Players
from aot.model.controller.triggers import Triggers
from aot.model.enums.constants import HT_AOE2_DE
from aot.model.enums.sizes import Size
from aot.model.enums.unit import UnitConstant
from aot.model.trigger import Trigger
from aot.model.units import Units
from aot.utilities.compress import Compress
from aot.utilities.decompress import Decompress

import logging

logger = logging.getLogger(__name__)


class Scenario:
    """ Scenario class """

    def get_height(self):
        return self.map.height

    def get_width(self):
        return self.map.width

    def __init__(self, header_type=HT_AOE2_DE, size=Size.GIANT):

        self._clear(size=size)
        self.header_type = header_type

    def add(self, trigger):
        if issubclass(trigger.__class__, Trigger):
            self.triggers.add(trigger)
        elif issubclass(trigger.__class__, MetaTrigger):
            trigger.setup(self)
        else:
            raise Exception("unknown class of trigger: {}".format(trigger.__class__))

    def __repr__(self):
        name = "SCENARIO:{}\n".format(self.filename)
        info1 = "\tWIDTH:{} HEIGHT:{}\n".format(self.tiles.width, self.tiles.height)
        info2 = "\tUNITS:{}\n".format(len(self.units))
        info3 = "\tTRIGGERS:{}".format(len(self.triggers))
        return name + info1 + info2 + info3

    def load(self, path, basename):
        """
            load examples from file
            it doesn't save current examples

            Args:
                basename (str): examples filename
                ver (float, optional): version of examples

            Raises:
                IOError: if file doesn't exits or is broken
        """
        full_path = path + "/" + basename + ".aoe2scenario"
        logger.debug("loading  examples at {}".format(full_path))
        self._clear()

        try:
            f = open(full_path, 'rb')
        except:
            raise (IOError("File is broken or doesn't exists"))
        b = f.read()  # get bytes from file
        d = Decompress(self, b, False)  # load data
        self.variables = d.variables

    def save(self, path, basename):
        """
            save examples as scx format

            Args:
                filename (str, optional): if set, it will create new
                    examples file, otherwise rewrite current

            Todo:
                finish this section
        """
        from datetime import datetime
        self.timestamp = int(datetime.timestamp(datetime.now()))
        self.filename = basename + ".aoe2scenario"
        path = path + "/" + self.filename
        logger.debug("saving  examples at {}".format(path))

        Compress(self, path)

    def _clear(self, size=None):
        """clear all examples data"""
        self.filename = None  # examples filename
        # self.version = None  # examples version

        self.instructions = ""
        self.n_players = 8
        self.hd_constant = 1000

        self.players = Players()  # initialize players
        self.messages = Messages()  #
        self.cinematics = Cinematics()  # movies
        self.background = Background()  # pre-game image
        if size is not None:
            self.map = Map(size.w, size.h)
        else:
            self.map = Map()
        self.tiles = self.map.tiles
        self.goals = Goals()
        self.units = Units()
        self.triggers = Triggers()
        self.units = Units()
        self.debug = Debug()

        for i in range(len(self.players)):
            self.players[i].units = self.units[i]

        self.timestamp = 0  # last save
        self.version = "1.21"
        self.is_aoe2scenario = True
        self.use_expansion = 1
        self.version2 = 1.2599999904632568
        self.datasets = [2, 3, 4, 5, 6]
        self.n_datasets = len(self.datasets)
        # self.header_type = header_type
        self.unknown1_compressed_header = 1
        self.unknown2_compressed_header = 0
        self.separator_at_compressed_header = b'\x00'
        self.big_skip_after_diplo = b'\x00' * 11520
        self.unknown1_after_tech = 0
        self.unknown2_after_tech = 0
        self.is_all_tech = 0
        self.unknown_bytes_before_w_h = b'\x00' * 16

    def build_rectangle(self, x1, y1, x2, y2, tile_type=40):
        for y in range(y1, y2):
            self.map.tiles[y][x1].type = tile_type
        for y in range(y1, y2):
            self.map.tiles[y][x2].type = tile_type
        for x in range(x1, x2):
            self.map.tiles[y1][x].type = tile_type
        for x in range(x1, x2):
            self.map.tiles[y2][x].type = tile_type

    def grid_of_tile(self, tile_type=40, separator=5):
        for x in range(1, int(self.map.width / separator) + 1):
            for y in range(0, self.map.height):
                self.map.tiles[x * separator - 1][y].type = tile_type

        for x in range(1, int(self.map.height / separator) + 1):
            for y in range(0, self.map.width):
                self.map.tiles[y][x * separator - 1].type = tile_type

    def build_trigger_space(self, tile=3):
        # print(self.players[0].units)
        for x in range(10, self.map.width - 8):
            self.players[0].units.new(x=x - 0.5, y=9 - 0.5, type=UnitConstant.HAY_STACK.type)
        for x in range(10, self.map.width - 8):
            self.players[0].units.new(x=x - 0.5, y=self.map.height - 9 + 0.5, type=UnitConstant.HAY_STACK.type)
        for x in range(10, self.map.height - 8):
            self.players[0].units.new(x=9 - 0.5, y=x - 0.5, type=UnitConstant.HAY_STACK.type)
        for x in range(10, self.map.height - 8):
            self.players[0].units.new(x=self.map.width - 9 + 0.5, y=x - 0.5, type=UnitConstant.HAY_STACK.type)
        for x in range(0, self.map.width):
            for y in range(0, 8):
                self.map.tiles[x][y].type = tile
        for x in range(0, self.map.width):
            for y in range(self.map.height - 8, self.map.height):
                self.map.tiles[x][y].type = tile
        for x in range(0, self.map.height):
            for y in range(0, 8):
                self.map.tiles[y][x].type = tile
        for x in range(0, self.map.height):
            for y in range(self.map.width - 8, self.map.width):
                self.map.tiles[y][x].type = tile
