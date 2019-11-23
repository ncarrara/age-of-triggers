from aot.model.condition import Condition
from aot.model.effect import Effect
from aot.model.enums.constants import HT_AOE2_HD, HT_AOE2_DE
from aot.model.enums.effect import EffectType
from aot.model.trigger import Trigger
from aot.utilities import *
from aot.model import *
import zlib
import time
import logging

from aot.utilities.decoder import Decoder
import collections
logger = logging.getLogger(__name__)


def inflate(data):
    decompress = zlib.decompressobj(
        -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()

    return inflated


def deflate(data, compresslevel=9):
    compress = zlib.compressobj(
        compresslevel,  # level: 0-9
        zlib.DEFLATED,  # method: must be DEFLATED
        -zlib.MAX_WBITS,  # window size in bits:
        #   -15..-8: negate, suppress header
        #   8..15: normal
        #   16..30: subtract 16, gzip header
        zlib.DEF_MEM_LEVEL,  # mem level: 1..8/9
        0  # strategy:
        #   0 = Z_DEFAULT_STRATEGY
        #   1 = Z_FILTERED
        #   2 = Z_HUFFMAN_ONLY
        #   3 = Z_RLE
        #   4 = Z_FIXED
    )

    deflated = compress.compress(data)
    deflated += compress.flush()

    return deflated


class Decompress:

    def __init__(self, scenario, bData, path_header=None, path_decompressed_data=None):
        self.scenario = scenario
        self.key_counter = 0
        self.scenario.variables = collections.OrderedDict()
        self.scenario.variables_header = collections.OrderedDict()
        self.scenario.header_length = self.decompressHeader(bData)
        decompressed = self.unzip(bData[scenario.header_length:])
        self.decompressData(decompressed)
        if path_decompressed_data:
            f = open(path_decompressed_data, 'wb')
            f.write(decompressed)
            f.close()

        if path_header:
            f = open(path_header, 'wb')
            f.write(bData[:scenario.header_length])
            f.close()

    def _read(self, key=None, f=None, header=False, log=True):
        if header:
            variables = self.scenario.variables_header
        else:
            variables = self.scenario.variables
        offset = self.decoder.offset()
        var = f()
        if offset in variables:
            for k, v in variables.items():
                print(k, v)
            raise Exception("duplicate offset : {}".format(offset))  # use hash set better
        variables[offset] = (key, var)
        if log:
            str_var = str(var)
            if len(str_var) > 30:  # and len(str_var) < 100:
                str_var = str_var[:15] + " [...] " + str_var[-15:]
            logger.debug("[READING byte {}][{}] {}=<{}>".format(offset, f.__name__, key, str_var))
        return var

    def decompressHeader(self, data):
        d = Decoder(data)
        self.decoder = d

        self.scenario.version = self._read("header_decompressed.examples.version", lambda: d.getAscii(length=4),
                                           header=True)
        length = self._read("header_decompressed.lenght", d.get_s32, header=True)  # header length
        self.scenario.header_type = self._read("header_decompressed.header_type", d.get_s32, header=True)

        if self.scenario.header_type not in [HT_AOE2_DE]:
            raise Exception("File format not supported, header type = {}".format(self.scenario.header_type))

        self.scenario.timestamp = self._read("header_decompressed.timestamp", d.get_s32, header=True)
        self.scenario.instructions = self._read("header_decompressed.instructions", d.get_str32, header=True)
        self.scenario.unk_constant1 = self._read("header_decompressed.constant1", lambda: d.skip_constant(0),
                                                 header=True)
        self.scenario.n_players = self._read("header_decompressed.examples.n_players", d.get_s32, header=True)
        self.scenario.unk_constant2 = self._read("header_decompressed.constant2", lambda: d.skip_constant(1000),
                                                 header=True)
        self.scenario.use_expansion = self._read("header_decompressed.use_expansion", d.get_s32, header=True)
        n_datasets = self._read("header_decompressed.n_datasets", d.get_s32, header=True)
        self.scenario.datasets = [self._read("header_decompressed.dataset_{}".format(i), d.get_s32, header=True)
                                  for i in range(n_datasets)]

        self.scenario.author = self._read("author", d.get_str32, header=True)
        self.scenario.header_unknown = self._read("scenario.header_unknown", d.get_s32, header=True)
        return d.offset()

    def unzip(self, bytes):
        return zlib.decompress(bytes, -zlib.MAX_WBITS)

    def show_next_bytes(self, n, decoder):
        logger.debug(decoder.get_bytes(n))
        exit()

    def show_next_ints(self, n, decoder):
        for _ in range(n):
            logger.debug(decoder.get_s32())
        exit()

    def show_next_floats(self, n, decoder):
        for _ in range(n):
            logger.debug(decoder.get_float())
        exit()

    def decompressData(self, bData):
        d = Decoder(bData)
        self.decoder = d
        # Shortcuts: Scenario
        scenario = self.scenario
        players = self.scenario.players
        messages = self.scenario.messages
        triggers = self.scenario.triggers
        debug = self.scenario.debug

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- COMPRESSED HEADER --------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        nextID = self._read("units.nextID", d.get_u32)
        self.scenario.units.nextID = 1 if nextID==0 else nextID
        self.scenario.version2 = self._read("version2", d.get_float)

        for i in range(1, 17):
            players[i].name = self._read("player_{}.name".format(i), lambda: d.get_bytes(256))

        for i in range(1, 17):
            players[i].nameID = self._read("player_{}.nameID".format(i), d.get_s32)

        for i in range(1, 17):  # missing player 16 because gaia is 9, then offset ?
            if i == 9:
                i = 0  # GAIA is 9th
            if i > 9:
                i -= 1
            players[i].active = self._read("player_{}.active".format(i), d.get_u32)
            players[i].human = self._read("player_{}.human".format(i), d.get_u32)
            players[i].civilization = self._read("player_{}.civilization".format(i), d.get_u32)
            players[i].unknown1 = self._read("player_{}.unknown1".format(i), d.get_u32)

        scenario.unknown_bytes_after_civs = self._read(" scenario.unknown_bytes_after_civs", lambda: d.get_bytes(73))
        # print(scenario.unknown_bytes_after_civs)

        scenario.original_filename = self._read("original_filename",
                                                lambda: d.get_str16(remove_last=False))  # original filename
        # self.show_next_bytes(1000, d)
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- MESSAGES ----------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        messages.objectives.id = self._read("messages.objectives.id", f=d.get_s32)
        messages.hints.id = self._read("messages.hints.id", f=d.get_s32)
        messages.victory.id = self._read("messages.victory.id", f=d.get_s32)
        messages.loss.id = self._read("messages.loss.id", f=d.get_s32)
        messages.history.id = self._read("messages.history.id", f=d.get_s32)
        messages.scouts.id = self._read("messages.scouts.id", f=d.get_s32)

        messages.objectives.text = self._read("messages.objectives.text", f=lambda: d.get_str16(remove_last=False))
        messages.hints.text = self._read("messages.hints.text", f=lambda: d.get_str16(remove_last=False))
        messages.victory.text = self._read("messages.victory.text", f=lambda: d.get_str16(remove_last=False))
        messages.loss.text = self._read("messages.loss.text", f=lambda: d.get_str16(remove_last=False))
        messages.history.text = self._read("messages.history.text", f=lambda: d.get_str16(remove_last=False))
        messages.scouts.text = self._read("messages.scouts.text ", f=lambda: d.get_str16(remove_last=False))

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- CINEMATICS ----------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        scenario.cinematics.intro = self._read("scenario.cinematics.intro", f=lambda: d.get_str16(remove_last=False))
        scenario.cinematics.victory = self._read("scenario.cinematics.victory",
                                                 f=lambda: d.get_str16(remove_last=False))
        scenario.cinematics.defeat = self._read("scenario.cinematics.defeat", f=lambda: d.get_str16(remove_last=False))

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- BACKGROUND ----------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        scenario.background.filename = self._read("scenario.background.filename",
                                                  f=lambda: d.get_str16(remove_last=False))
        scenario.background.included = self._read("scenario.background.included", f=d.get_u32)
        scenario.background.width = self._read("scenario.background.width", f=d.get_u32)
        scenario.background.height = self._read("scenario.background.height", f=d.get_u32)
        self.scenario.background.include = self._read("scenario.background.include", d.get_s16)

        if (self.scenario.background.include == -1 or self.scenario.background.include == 2):
            scenario.size = self._read("scenario.size", d.get_u32)
            scenario.width = self._read("scenario.width", d.get_s32)
            scenario.height = self._read("scenario.height ", d.get_s32)
            scenario.planes = self._read("scenario.planes", d.get_s16)
            scenario.bitCount = self._read("scenario.bitCount", d.get_s16)
            scenario.compression = self._read("scenario.compression", d.get_s32)
            scenario.sizeImage = self._read("scenario.sizeImage", d.get_s32)
            scenario.xPels = self._read("scenario.xPels", d.get_s32)
            scenario.yPels = self._read("scenario.yPels", d.get_s32)
            scenario.colors = self._read("scenario.colors", d.get_u32)
            scenario.iColors = self._read("scenario.iColors", d.get_s32)
            scenario.colorTable = self._read("scenario.colorTable", lambda: d.get_bytes(scenario.colors * 4))
            scenario.rawData = self._read("scenario.rawData", lambda: d.get_bytes(scenario.sizeImage))

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- PLAYER DATA 2-------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        for i in range(1, 17):
            players[i].unknown_constant = self._read("players[{}].unknown_constant".format(i), d.get_u32)

        for i in range(1, 17):
            if i == 9:
                i = 0  # GAIA is 9th
            if i > 9:
                i -= 1
            players[i].vc_names = self._read("player_{}.vc_names".format(i), lambda: d.get_str16(remove_last=False))

        for i in range(1, 17):
            if i == 9:
                i = 0  # GAIA is 9th
            if i > 9:
                i -= 1
            players[i].unknown8bytes = self._read("players[{}].unknown8bytes".format(i), lambda: d.get_bytes(8))
            players[i].cty_names = self._read("player_{}.cty_names".format(i), lambda: d.get_str32(remove_last=False))

        self.scenario.unk_after_civs = self._read("scenario.unk_after_civs", lambda: d.get_bytes(20))

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- UNUSED RESOURCES -------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        for i in range(1, 17):
            if i == 9:
                i = 0  # GAIA is 9th
            if i > 9:
                i -= 1
            players[i]._unused_resource.gold = self._read("player_{}.unused_resource.gold".format(i), d.get_s32)
            players[i]._unused_resource.wood = self._read("player_{}.unused_resource.wood".format(i), d.get_s32)
            players[i]._unused_resource.food = self._read("player_{}.unused_resource.food".format(i), d.get_s32)
            players[i]._unused_resource.stone = self._read("player_{}.unused_resource.stone".format(i), d.get_s32)
            players[i]._unused_resource.ore = self._read("player_{}.unused_resource.ore".format(i), d.get_s32)
            players[i]._unused_resource.padding = self._read("player_{}.unused_resource.padding".format(i), d.get_s32)
            players[i]._unused_resource.index = self._read("player_{}.unused_resource.index".format(i), d.get_s32)

        self._read("skip sep after unused resources", d.skip_separator)  # Separator 0xFFFFFF9D

        scenario.goals.conquest = self._read("goal.conquest", d.get_s32)
        scenario.goals.unknown1 = self._read("goal.unknown1", d.get_s32)
        scenario.goals.relics = self._read("goal.relics", d.get_s32)
        scenario.goals.unknown2 = self._read("goal.unknown2", d.get_s32)
        scenario.goals.exploration = self._read("goal.exploration", d.get_s32)
        scenario.goals.unknown3 = self._read("goal.unknown3", d.get_s32)
        scenario.goals.all = self._read("goal.all", d.get_s32)
        scenario.goals.mode = self._read("goal.mode", d.get_s32)
        scenario.goals.score = self._read("goal.score", d.get_s32)
        scenario.goals.time = self._read("goal.time", d.get_s32)

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- DIPLOMACY ----------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        for i in range(1, 17):
            for j in range(1, 17):
                players[i].diplomacy[j] = self._read("P{} diplo for P{} is :".format(i, j), d.get_s32)

        scenario.big_skip_after_diplo = self._read("big_skip_after_diplo", lambda: d.get_bytes(11520))  # unused space
        d.skip_separator()  # separator

        for i in range(1, 17):
            players[i].ally_vic = self._read("P{} ally vic =".format(i), d.get_s32)

        d.skip_constant(67109120)  # 4 unknown bytes

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- DISABLES -----------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        tech_count = d.unpack('I' * 16)
        logger.debug("tech count : {}".format(tech_count))
        for i in range(1, 17):
            players[i].disabledTechs = [self._read("players[{}].disabledTechs".format(i), d.get_u32) for _ in
                                        range(tech_count[i - 1])]
            logger.debug("P{}={}".format(i, players[i].disabledTechs))
        unit_count = d.unpack('I' * 16)
        logger.debug("unit_count : {}".format(unit_count))
        for i in range(1, 17):
            players[i].disabledUnits = [self._read("players[{}].disabledUnits".format(i), d.get_u32) for _ in
                                        range(unit_count[i - 1])]
            logger.debug("P{}={}".format(i, players[i].disabledUnits))
        building_count = d.unpack('I' * 16)
        logger.debug("building_count : {}".format(building_count))
        for i in range(1, 17):
            players[i].disabledBuildings = [self._read("players[{}].disabledBuildings".format(i), d.get_u32) for _ in
                                            range(building_count[i - 1])]
            logger.debug("P{}={}".format(i, players[i].disabledBuildings))

        scenario.unknown1_after_tech = self._read("scenario.unknown1_after_tech", d.get_u32)  # unused
        scenario.unknown2_after_tech = self._read("scenario.unknown2_after_tech", d.get_u32)  # unused
        scenario.is_all_tech = self._read("scenario.is_all_tech", d.get_u32)  # All tech

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- AGE ----------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        for i in range(1, 17):
            players[i].age = self._read("P{} age=".format(i), d.get_s32)

        d.skip_separator()  # separator
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- MAP ----------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        x = self._read("x_camera", d.get_s32)
        y = self._read("y_camera", d.get_s32)  # starting camera

        scenario.map.aiType = self._read("examples.map.aiType", d.get_u32)

        scenario.map.unk_before_water_definitions = self._read("scenario.map.unk_before_water_definitions",
                                                               lambda: d.get_bytes(22))
        scenario.map.water_definitions = self._read("scenario.map.water_definitions",
                                                    lambda: d.get_str16(remove_last=False))

        scenario.map.unk_before_empty = self._read("scenario.map.unk_before_empty", lambda: d.get_bytes(2))

        scenario.map.empty = self._read("scenario.map.empty", lambda: d.get_str16(remove_last=False))

        scenario.map.unk_before_w_h = self._read("scenario.map.unk_before_w_h", lambda: d.get_bytes(10))

        w = self._read("w_map", d.get_s32)
        h = self._read("h_map", d.get_s32)

        scenario.map.camera = x, y
        scenario.map.resize(w, h)

        for i, tile in enumerate(self.scenario.tiles):
            tile.type = self._read("tile[{}].type".format(i), d.get_u8, log=False)
            tile.elevation = self._read("tile[{}].elevation".format(i), d.get_u8, log=False)
            tile.unknown1 = self._read("tile[{}].unknown1".format(i), d.get_u8, log=False)
            tile.unknown2 = self._read("tile[{}].unknown2".format(i), d.get_u8, log=False)
            tile.unknown3 = self._read("tile[{}].unknown3".format(i), d.get_u8, log=False)
            tile.layer_type = self._read("tile[{}].layer_type".format(i), d.get_u8, log=False)
            tile.is_layering = self._read("tile[{}].is_layering".format(i), d.get_u8, log=False)  # 0 if yes

        d.skip_constant(9)  # number of unit sections, N. I've always seen = 9.

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------- (DEFAULT ?) RESOURCE------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        for i in range(1, 9):
            resource = players[i].resource
            resource.food = self._read("P{} food=".format(i), d.get_float)
            resource.wood = self._read("P{} wood=".format(i), d.get_float)
            resource.gold = self._read("P{} gold=".format(i), d.get_float)
            resource.stone = self._read("P{} stone=".format(i), d.get_float)
            resource.ore = self._read("P{} ore ==".format(i), d.get_float)
            resource.padding = self._read("P{} padding=".format(i), d.get_s32)
            players[i].population = self._read("P{} max pop ? =".format(i), d.get_float)

        d.skip_constant(9)  # number of plyers, again

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- Player Data 3 Section ----------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        for i in range(1, 9):  # only for playable players
            players[i].constName = self._read("players[{}].constName".format(i), d.get_str16)
            players[i].camera.x = self._read("players[{}].camera.x".format(i), d.get_float)
            players[i].camera.y = self._read("players[{}].camera.y".format(i), d.get_float)
            players[i].camera.unknown1 = self._read("players[{}].camera.unknown1".format(i), d.get_s16)
            players[i].camera.unknown2 = self._read("players[{}].camera.unknown2".format(i), d.get_s16)
            players[i].allyVictory = self._read("players[{}].allyVictory".format(i), d.get_s8)

            players[i].dip = self._read("players[{}].dip".format(i), d.get_u16)
            players[i].unk0 = self._read("players[{}].unk0".format(i), lambda: d.get_bytes(players[i].dip))
            # 0 = allied, 1 = neutral, 2 = ? , 3 = enemy

            for j in range(9):
                players[i].diplomacy.gaia[j] = self._read("players[{}].diplomacy.gaia[{}]".format(i, j), d.get_s32)
            players[i].color = self._read("players[{}].color".format(i), d.get_u32)
            players[i].unk1 = self._read("players[{}].unk1".format(i), d.get_float)
            players[i].unk2 = self._read("players[{}].unk2".format(i), d.get_u16)
            if players[i].unk1 == 2.0:
                players[i].unk3 = self._read("players[{}].unk3".format(i), lambda: d.get_bytes(8))

            if players[i].unk2 > 0:
                players[i].unk4 = self._read("players[{}].unk4".format(i), lambda: d.get_bytes(players[i].unk2 * 44))
            players[i].unk5 = self._read("players[{}].unk5".format(i), lambda: d.get_bytes(7))
            players[i].unk6 = self._read("players[{}].unk6".format(i), lambda: d.get_bytes(4))

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- UNITS SECTION (DE) -------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        for i in range(0, 9):

            number_of_units = self._read("number_of_units[{}]".format(i), d.get_u32)
            for u in range(number_of_units):
                scenario.units.new(owner=i,
                                   x=self._read("x [{}][{}]".format(i, u), d.get_float),
                                   y=self._read("y [{}][{}]".format(i, u), d.get_float),
                                   unknown1=self._read("unknown1 [{}][{}]".format(i, u), d.get_float),
                                   id=self._read("id [{}][{}]".format(i, u), d.get_u32),
                                   type=self._read("type [{}][{}]".format(i, u), d.get_u16),
                                   unknown2=self._read("unknown2 [{}][{}]".format(i, u), d.get_s8),
                                   angle=self._read("angle [{}][{}]".format(i, u), d.get_float),
                                   frame=self._read("frame [{}][{}]".format(i, u), d.get_u16),
                                   inId=self._read("inId [{}][{}]".format(i, u), d.get_s32))

        self.scenario.ukn_9_bytes_before_triggers = self._read("scenario.ukn_9_bytes_before_triggers",
                                                               lambda: d.get_bytes(9))

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- TRIGGERS  ----------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        n = self._read("number of triggers".format(i), d.get_u32)  # number of triggers

        for id_trigger in range(n):
            logger.debug("-----------trigger {} ----------".format(id_trigger))
            trigger = Trigger()  # TODO compress
            self.scenario.add(trigger)
            trigger.id = id_trigger
            trigger.enable = self._read("trigger[{}].enable".format(id_trigger), d.get_u32)
            trigger.loop = self._read("trigger[{}].loop".format(id_trigger), d.get_s8)
            trigger.trigger_description["string_table_id"] = \
                self._read("trigger[{}].trigger_description[\"string_table_id\"]".format(id_trigger), d.get_s8)
            trigger.unknowns[0] = self._read("trigger.unknowns[0]", d.get_s8)
            trigger.unknowns[1] = self._read("trigger.unknowns[1]", d.get_s8)
            trigger.unknowns[2] = self._read("trigger.unknowns[2]", d.get_s8)
            trigger.display_as_objective = \
                self._read("trigger[{}].display_as_objective".format(id_trigger), d.get_s8)
            trigger.description_order = self._read("[id={}] trigger.description_order".format(id_trigger), d.get_u32)
            trigger.make_header = self._read("[id={}] trigger.make_header".format(id_trigger), d.get_s8)
            trigger.short_description["string_table_id"] = \
                self._read("trigger[{}].short_description[\"string_table_id\"]".format(id_trigger), d.get_s8)
            trigger.unknowns[3] = self._read("trigger.unknowns[3]", d.get_s8)
            trigger.unknowns[4] = self._read("trigger.unknowns[4]", d.get_s8)
            trigger.unknowns[5] = self._read("trigger.unknowns[5]", d.get_s8)
            trigger.short_description["display_on_screen"] = \
                self._read("trigger[{}].short_description[\"display_on_screen\"]".format(id_trigger), d.get_s8)
            trigger.unknowns[6] = self._read("trigger.unknowns[6]", d.get_s8)
            trigger.unknowns[7] = self._read("trigger.unknowns[7]", d.get_s8)
            trigger.unknowns[8] = self._read("trigger.unknowns[8]", d.get_s8)
            trigger.unknowns[9] = self._read("trigger.unknowns[9]", d.get_s8)
            trigger.unknowns[10] = self._read("trigger.unknowns[10]", d.get_s8)
            logger.debug("trigger[{}].unknowns={}".format(id_trigger, trigger.unknowns))
            trigger.mute_objectives = self._read("trigger[{}].mute_objectives".format(id_trigger), d.get_s8)
            trigger.trigger_description["text"] = \
                self._read("trigger[{}].trigger_description[\"text\"]".format(id_trigger), d.get_str32)

            trigger.name = self._read("trigger[{}].name".format(id_trigger), d.get_str32)
            trigger.short_description["text"] = \
                self._read("trigger[{}].short_description[\"text\"]".format(id_trigger), d.get_str32)

            logger.debug("PROCESSING EFFECTS")
            ne = self._read("number of effect({})".format(id_trigger), d.get_s32)  # number of effects
            for id_effect in range(ne):
                logger.debug("---------- effect {} -----------".format(id_effect))
                effect = Effect()
                trigger.then_(effect)
                effect.type = self._read("trigger[{}].effect[{}].type".format(id_trigger, id_effect), d.get_s32)
                effect.check = self._read("trigger[{}].effect[{}].check".format(id_trigger, id_effect), d.get_s32)
                if effect.check != 46:  # 24 for HD
                    logger.warning(
                        "check attribut is '{}' for effects but should be 46 for aoe2scenario".format(
                            effect.check))
                effect.ai_goal = self._read("trigger[{}].effect[{}].aiGoal".format(id_trigger, id_effect), d.get_s32)
                effect.amount = self._read("trigger[{}].effect[{}].amount".format(id_trigger, id_effect), d.get_s32)
                effect.resource = self._read("trigger[{}].effect[{}].resource".format(id_trigger, id_effect), d.get_s32)
                effect.state = self._read("trigger[{}].effect[{}].state".format(id_trigger, id_effect), d.get_s32)

                effect.selected_count = self._read("trigger[{}].effect[{}].selectedCount".format(id_trigger, id_effect),
                                                   d.get_s32)
                effect.unit_id = self._read("trigger[{}].effect[{}].unitId".format(id_trigger, id_effect), d.get_s32)

                effect.unit_cons = self._read("trigger[{}].effect[{}].unit_cons".format(id_trigger, id_effect),
                                              d.get_s32)
                effect.source_player = self._read("trigger[{}].effect[{}].sourcePlayer".format(id_trigger, id_effect),
                                                  d.get_s32)
                effect.target_player = self._read("trigger[{}].effect[{}].targetPlayer".format(id_trigger, id_effect),
                                                  d.get_s32)

                effect.tech = self._read("trigger[{}].effect[{}].tech".format(id_trigger, id_effect), d.get_s32)

                effect.string_table_id = self._read(
                    "trigger[{}].effect[{}].string_table_id".format(id_trigger, id_effect), d.get_s32)
                effect.unknown1 = self._read("trigger[{}].effect[{}].unknown1".format(id_trigger, id_effect), d.get_s32)
                effect.time = self._read("trigger[{}].effect[{}].time".format(id_trigger, id_effect), d.get_s32)

                triggerId = self._read("trigger[{}].effect[{}].triggerId".format(id_trigger, id_effect), d.get_s32)
                effect.trigger_to_activate = Trigger(id=triggerId)
                effect.x = self._read("trigger[{}].effect[{}].x".format(id_trigger, id_effect), d.get_s32)
                effect.y = self._read("trigger[{}].effect[{}].y".format(id_trigger, id_effect), d.get_s32)

                effect.x1 = self._read("trigger[{}].effect[{}].x1".format(id_trigger, id_effect), d.get_s32)
                effect.y1 = self._read("trigger[{}].effect[{}].y1".format(id_trigger, id_effect), d.get_s32)
                effect.x2 = self._read("trigger[{}].effect[{}].x2".format(id_trigger, id_effect), d.get_s32)
                effect.y2 = self._read("trigger[{}].effect[{}].y2".format(id_trigger, id_effect), d.get_s32)

                effect.unit_group = self._read("trigger[{}].effect[{}].unitGroup".format(id_trigger, id_effect), d.get_s32)
                effect.unit_type = self._read("trigger[{}].effect[{}].unitType".format(id_trigger, id_effect), d.get_s32)
                effect.panel_location = self._read("trigger[{}].effect[{}].panel_location".format(id_trigger, id_effect),d.get_s32)

                # effect.unknown2 = self._read("trigger[{}].effect[{}].unknown2".format(id_trigger, id_effect), d.get_s32)

                # effect.text = self._read("trigger[{}].effect[{}].text".format(id_trigger, id_effect), d.get_str32)
                # effect.filename = self._read("trigger[{}].effect[{}].filename".format(id_trigger, id_effect),d.get_str32)
                effect.unknown3 = self._read("trigger[{}].effect[{}].unknown3".format(id_trigger, id_effect),lambda: d.get_bytes(80))

                effect.facet = self._read("trigger[{}].effect[{}].facet".format(id_trigger, id_effect), d.get_s32)
                effect.unknown4 = self._read("trigger[{}].effect[{}].unknown4".format(id_trigger, id_effect), d.get_s32)
                effect.unknown5 = self._read("trigger[{}].effect[{}].unknown5".format(id_trigger, id_effect), d.get_s32)

                effect.message = self._read("trigger[{}].effect[{}].message".format(id_trigger, id_effect),lambda: d.get_str32(remove_last=True))
                effect.sound_event_name = self._read("trigger[{}].effect[{}].sound_event_name".format(id_trigger, id_effect),lambda: d.get_str32(remove_last=True))
                for k in range(effect.selected_count):
                    unitid = self._read("trigger[{}].effect[{}].unitid[{}]".format(id_trigger, id_effect, k), d.get_s32)
                    effect.unit_ids.append(unitid)

            trigger.effects_order = [self._read(
                "trigger[{}].effect[{}] order".format(id_trigger, e),
                d.get_u32) for e in range(ne)]

            # exit()

            nc = self._read("trigger[{}].number of conditions".format(id_trigger), d.get_s32)  # number of conditions
            logger.debug("PROCESSING CONDITIONS")
            logger.debug("number of conditions : {}".format(nc))
            # exit()
            for id_condition in range(nc):
                c = Condition()
                logger.debug("---------- condition {} ----------".format(id_condition))
                c.type = self._read("trigger[{}].condition[{}].type".format(id_trigger, id_condition), d.get_u32)
                c.check = self._read("trigger[{}].condition[{}].check".format(id_trigger, id_condition), d.get_s32)
                if c.check != 21:
                    logger.warning(
                        "check attribut is '{}' for conditions but should be 21 for aoe2scenario".format(c.check))
                c.amount = self._read("trigger[{}].condition[{}].amount".format(id_trigger, id_condition), d.get_s32)
                c.resource = self._read("trigger[{}].condition[{}].resource".format(id_trigger, id_condition), d.get_s32)
                c.unit_object = self._read("trigger[{}].condition[{}].unit_object".format(id_trigger, id_condition), d.get_s32)
                c.unit_id = self._read("trigger[{}].condition[{}].unit_id".format(id_trigger, id_condition), d.get_s32)
                c.unit_cons = self._read("trigger[{}].condition[{}].unit_cons".format(id_trigger, id_condition), d.get_s32)
                c.source_player = self._read("trigger[{}].condition[{}].source_player".format(id_trigger, id_condition), d.get_s32)
                c.tech = self._read("trigger[{}].condition[{}].tech".format(id_trigger, id_condition), d.get_s32)
                c.timer = self._read("trigger[{}].condition[{}].timer".format(id_trigger, id_condition), d.get_s32)
                c.unknown1 = self._read("trigger[{}].condition[{}].unknown1".format(id_trigger, id_condition), d.get_s32)
                c.x1 = self._read("trigger[{}].condition[{}].x1".format(id_trigger, id_condition), d.get_s32)
                c.y1 = self._read("trigger[{}].condition[{}].y1".format(id_trigger, id_condition), d.get_s32)
                c.x2 = self._read("trigger[{}].condition[{}].x2".format(id_trigger, id_condition), d.get_s32)
                c.y2 = self._read("trigger[{}].condition[{}].y2".format(id_trigger, id_condition), d.get_s32)
                c.unit_group = self._read("trigger[{}].condition[{}].unit_group".format(id_trigger, id_condition), d.get_s32)
                c.unit_type = self._read("trigger[{}].condition[{}].unit_type".format(id_trigger, id_condition), d.get_s32)
                c.ai_signal = self._read("trigger[{}].condition[{}].ai_signal".format(id_trigger, id_condition), d.get_s32)
                c.reversed = self._read("trigger[{}].condition[{}].reversed".format(id_trigger, id_condition), d.get_s32)
                c.unknown2 = self._read("trigger[{}].condition[{}].unknown2".format(id_trigger, id_condition), d.get_s32)
                c.unknown3 = self._read("trigger[{}].condition[{}].unknown3".format(id_trigger, id_condition), d.get_s32)
                c.unknown4 = self._read("trigger[{}].condition[{}].unknown4".format(id_trigger, id_condition), d.get_s32)
                c.unknown5 = self._read("trigger[{}].condition[{}].unknown5".format(id_trigger, id_condition), d.get_s32)

                trigger.then_(c)

            trigger.conditions_order = [self._read(
                "trigger[{}].conditions[{}] order".format(id_trigger, c),
                d.get_u32) for c in range(nc)]
        triggers.order = [self._read(
            "triggers.order[{}] order".format(i),
            d.get_u32) for i in range(n)]

        # not very well optimized if you ask me
        for id_trigger in scenario.triggers:
            for id_effect in id_trigger.effects:
                if id_effect.type == EffectType.ACTIVATE_TRIGGER.value:
                    if id_effect.trigger_to_activate.id != -1:
                        for tr in scenario.triggers:
                            if tr.id == id_effect.trigger_to_activate.id:
                                id_effect.trigger_to_activate = tr

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- DEBUG  -------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        debug.included = self._read("debug.included", d.get_u32)
        debug.error = self._read("debug.error", d.get_u32)

        if debug.included:
            debug.raw = self._read("debug.raw", lambda: d.get_bytes(396))  # AI DEBUG file

        scenario.extra_bytes_at_the_end = self._read("scenario.extra_bytes_at_the_end", lambda: d.get_bytes(1024))

        scenario.has_embedded_ai_file = self._read("scenario.has_embemded_ai_file", d.get_u8)

        scenario.unk_before_embedded = self._read("scenario.unk_before_embedded", lambda: d.get_bytes(7))

        if scenario.has_embedded_ai_file:

            scenario.number_of_ai_files = self._read(scenario.number_of_ai_files, d.get_u32)
            scenario.ai_files = []
            for i in range(scenario.number_of_ai_files):
                fileper = self._read("fileper{}".format(i), lambda: d.get_str32(remove_last=True))
                aifile = self._read("aifile{}".format(i), lambda: d.get_str32(remove_last=True))
                scenario.ai_files.append((fileper, aifile))

        # exit()

        if 0 < d.bytes_remaining():
            raise Exception("it remains {} bytes\n\n{}".format(d.bytes_remaining(), d.get_bytes(d.bytes_remaining())))
