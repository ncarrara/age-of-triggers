from aot.model.effect import Effect, EffectType
from aot.model.enums.constants import HT_AOE2_HD, HT_AOE2_DE
from aot.model.trigger import Trigger
from aot.utilities import *
from aot.model import *
import zlib
import time
import logging

from aot.utilities.decoder import Decoder

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

    def __init__(self, scenario, bData, temp=False):
        """!
        """
        self.scenario = scenario
        self.key_counter = 0
        self.variables = {}
        start = time.time()
        headerLength = self.decompressHeader(bData)
        decompressed = self.unzip(bData[headerLength:])
        dataLenght = self.decompressData(decompressed)
        end = time.time() - start
        if temp:
            f = open('decompressed.temp', 'wb')
            f.write(decompressed)
            f.close()

    def _read(self, key=None, f=None):
        var = f()
        toprint = True
        if key is None:
            key = self.key_counter
            self.key_counter += 1
            toprint = False
        if key in self.variables:
            raise Exception("duplicate key : {}".format(key))  # use hash set better
        self.variables[key] = var
        if toprint:
            str_var = str(var)
            if len(str_var) > 30:  # and len(str_var) < 100:
                str_var = str_var[:15] + " [...] " + str_var[-15:]
            logger.debug("[READING][{}] {}=<{}>".format(f.__name__, key, str_var))
        return var

    def decompressHeader(self, data):
        d = Decoder(data)

        self.scenario.version = self._read("header_decompressed.examples.version", lambda: d.getAscii(length=4))
        length = self._read("header_decompressed.lenght", d.get_s32)  # header length
        self.scenario.header_type = self._read("header_decompressed.header_type", d.get_s32)
        if self.scenario.header_type not in [HT_AOE2_DE, HT_AOE2_HD]:
            raise Exception("File format not supported, header type = {}".format(self.scenario.header_type))

        self.scenario.timestamp = self._read("header_decompressed.timestamp", d.get_s32)
        self.scenario.instructions = self._read("header_decompressed.instructions", d.getStr32)
        self._read("header_decompressed.constante", lambda: d.skip_constant(0))
        self.scenario.n_players = self._read("header_decompressed.examples.n_players", d.get_s32)
        self.scenario.hd_constant = self._read("header_decompressed.constante2", lambda: d.skip_constant(1000))
        self.scenario.use_expansion = self._read("header_decompressed.use_expansion", d.get_s32)
        n_datasets = self._read("header_decompressed.n_datasets", d.get_s32)
        self.scenario.datasets = [self._read("header_decompressed.dataset_{}".format(i), d.get_s32)
                                  for i in range(n_datasets)]

        if self.scenario.header_type == HT_AOE2_DE:
            self.scenario.author = self._read("author", d.getStr32)
            self.scenario.header_unknown = self._read("examples.header_unknown", d.get_s32)
            # exit()
        return d.offset()

    def unzip(self, bytes):
        return zlib.decompress(bytes, -zlib.MAX_WBITS)

    def show_next_bytes(self, n, decoder):
        logger.debug(decoder.getBytes(n))
        exit()

    def show_next_ints(self, n, decoder):
        for _ in range(n):
            logger.debug(decoder.get_s32())
        exit()

    def show_next_floats(self, n, decoder):
        for _ in range(n):
            logger.debug(decoder.getFloat())
        exit()

    def decompressData(self, bData):
        d = Decoder(bData)

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

        scenario.units.nextID = self._read("units.nextID", d.get_u32)
        self.scenario.version2 = self._read("version2", d.getFloat)

        for i in range(1, 17):
            players[i].name = self._read("player_{}.name".format(i), lambda: d.getAscii(256))

        for i in range(1, 17):
            players[i].nameID = self._read("player_{}.nameID".format(i), d.get_s32)

        for i in range(1, 17):  # missing player 16 because gaia is 9, then offset ?
            if self.scenario.header_type is HT_AOE2_DE:
                if i == 9:
                    i = 0  # GAIA is 9th
                if i > 9:
                    i -= 1
            players[i].active = self._read("player_{}.active".format(i), d.get_u32)
            players[i].human = self._read("player_{}.human".format(i), d.get_u32)
            players[i].civilization = self._read("player_{}.civilization".format(i), d.get_u32)
            players[i].unknown1 = self._read("player_{}.unknown1".format(i), d.get_u32)

        if self.scenario.header_type is HT_AOE2_DE:
            scenario.unknown_bytes_after_civs = self._read(" scenario.unknown_bytes_after_civs", lambda: d.getBytes(73))
        else:
            scenario.unknown1_compressed_header = self._read("unknown1_compressed_header", d.get_s32)  # unk1
            scenario.unknown2_compressed_header = self._read("unknown2_compressed_header", d.get_s32)  # unk2
            scenario.separator_at_compressed_header = self._read("separator_at_compressed_header",
                                                                 lambda: d.getBytes(1))  # unk1
        scenario.filename = self._read("original_filename", lambda: d.getStr16(remove_last=False))  # original filename

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

        messages.objectives.text = self._read("messages.objectives.text", f=lambda: d.getStr16(remove_last=False))
        messages.hints.text = self._read("messages.hints.text", f=lambda: d.getStr16(remove_last=False))
        messages.victory.text = self._read("messages.victory.text", f=lambda: d.getStr16(remove_last=False))
        messages.loss.text = self._read("messages.loss.text", f=lambda: d.getStr16(remove_last=False))
        messages.history.text = self._read("messages.history.text", f=lambda: d.getStr16(remove_last=False))
        messages.scouts.text = self._read("messages.scouts.text ", f=lambda: d.getStr16(remove_last=False))

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- CINEMATICS ----------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        scenario.cinematics.intro = self._read("scenario.cinematics.intro", f=lambda: d.getStr16(remove_last=False))
        scenario.cinematics.victory = self._read("scenario.cinematics.victory", f=lambda: d.getStr16(remove_last=False))
        scenario.cinematics.defeat = self._read("scenario.cinematics.defeat", f=lambda: d.getStr16(remove_last=False))

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- BACKGROUND ----------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        scenario.background.filename = self._read("scenario.background.filename",
                                                  f=lambda: d.getStr16(remove_last=False))
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
            scenario.colorTable = self._read("scenario.colorTable", lambda: d.getBytes(scenario.colors * 4))
            scenario.rawData = self._read("scenario.rawData", lambda: d.getBytes(scenario.sizeImage))

        if self.scenario.header_type is HT_AOE2_DE:
            for i in range(1, 17):
                players[i].unknown_constant = self._read("players[{}].unknown_constant".format(i), d.get_u32)

        # section: PLAYER DATA 2
        for i in range(1, 17):
            if self.scenario.header_type is HT_AOE2_DE:
                if i == 9:
                    i = 0  # GAIA is 9th
                if i > 9:
                    i -= 1
            players[i].vc_names = self._read("player_{}.vc_names".format(i), lambda: d.getStr16(remove_last=False))

        for i in range(1, 17):
            if self.scenario.header_type is HT_AOE2_DE:
                if i == 9:
                    i = 0  # GAIA is 9th
                if i > 9:
                    i -= 1
                players[i].unknown8bytes = self._read("players[{}].unknown8bytes".format(i), lambda: d.getBytes(8))
            f = lambda: d.getStr32(
                remove_last=False) if self.scenario.header_type is HT_AOE2_DE else lambda: d.getStr16(remove_last=False)
            players[i].cty_names = self._read("player_{}.cty_names".format(i), f)

        if self.scenario.header_type is HT_AOE2_DE:
            self.scenario.unk_after_civs = self._read("scenario.unk_after_civs", lambda: d.getBytes(20))
        else:
            for i in range(1, 17):
                players[i].per_names = self._read("player_{}.per_names".format(i),
                                                  lambda: d.getStr16(remove_last=False))

            for i in range(1, 17):
                f = d.get_u32
                players[i].vc_per_length = self._read("player_{}.vc_per_length".format(i), f)  # Unknown 1
                players[i].cty_per_length = self._read("player_{}.cty_per_length".format(i), f)  # Unknown 1
                players[i].per_per_length = self._read("player_{}.per_per_length".format(i), f)

                players[i].vc = self._read("player_{}.vc".format(i), lambda: d.getBytes(players[i].vc_per_length))
                players[i].cty = self._read("player_{}.cty".format(i), lambda: d.getBytes(players[i].cty_per_length))
                players[i].per = self._read("player_{}.per".format(i), lambda: d.getBytes(players[i].per_per_length))

            for i in range(1, 17):
                players[i].ai.type = self._read("player_{}.ai.type".format(i), d.getInt8)

            self._read("skip sep after AI", d.skip_separator)  # Separator 0xFFFFFF9D

        for i in range(1, 17):
            if self.scenario.header_type is HT_AOE2_DE:
                if i == 9:
                    i = 0  # GAIA is 9th
                if i > 9:
                    i -= 1
            players[i]._unused_resource.gold = self._read("player_{}.unused_resource.gold".format(i), d.get_s32)
            players[i]._unused_resource.wood = self._read("player_{}.unused_resource.wood".format(i), d.get_s32)
            players[i]._unused_resource.food = self._read("player_{}.unused_resource.food".format(i), d.get_s32)
            players[i]._unused_resource.stone = self._read("player_{}.unused_resource.stone".format(i), d.get_s32)
            players[i]._unused_resource.ore = self._read("player_{}.unused_resource.ore".format(i), d.get_s32)
            players[i]._unused_resource.padding = self._read("player_{}.unused_resource.padding".format(i),
                                                             d.get_s32)
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

        scenario.big_skip_after_diplo = self._read("big_skip_after_diplo", lambda: d.getBytes(11520))  # unused space
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
        if self.scenario.header_type is HT_AOE2_DE:
            tech_count = d.unpack('i' * 16)
            logger.debug("tech count : {}".format(tech_count))
            for i in range(1, 17):
                players[i].disabledTechs = [d.get_s32() for _ in range(tech_count[i - 1])]
                logger.debug("P{}={}".format(i, players[i].disabledTechs))
            unit_count = d.unpack('i' * 16)
            logger.debug("unit_count : {}".format(unit_count))
            for i in range(1, 17):
                players[i].disabledUnits = [d.get_s32() for _ in range(unit_count[i - 1])]
                logger.debug("P{}={}".format(i, players[i].disabledUnits))
            building_count = d.unpack('i' * 16)
            logger.debug("building_count : {}".format(building_count))
            for i in range(1, 17):
                players[i].disabledBuildings = [d.get_s32() for _ in range(building_count[i - 1])]
                logger.debug("P{}={}".format(i, players[i].disabledBuildings))
        else:
            logger.debug("tech count : {}".format(d.unpack('i' * 16)))
            for i in range(1, 17):
                players[i].disabledTechs = [d.get_s32() for _ in range(20)]
                logger.debug("P{}={}".format(i, players[i].disabledTechs))
            logger.debug("unit count : {}".format(d.unpack('i' * 16)))
            for i in range(1, 17):
                players[i].disabledUnits = [d.get_s32() for _ in range(30)]
                logger.debug("P{}={}".format(i, players[i].disabledUnits))

            logger.debug("building count : {}".format(d.unpack('i' * 16)))
            for i in range(1, 17):
                players[i].disabledBuildings = [d.get_s32() for _ in range(30)]
                logger.debug("P{}={}".format(i, players[i].disabledBuildings))

        scenario.unknown1_after_tech = self._read("examples.unknown1_after_tech", d.get_s32)  # unused
        scenario.unknown2_after_tech = self._read("examples.unknown2_after_tech", d.get_s32)  # unused
        scenario.is_all_tech = self._read("examples.is_all_tech", d.get_s32)  # All tech

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

        if self.scenario.header_type is HT_AOE2_DE:
            scenario.map.unk_before_water_definitions = self._read("scenario.map.unk_before_water_definitions",
                                                                   lambda: d.getBytes(22))
            scenario.map.water_definitions = self._read("scenario.map.water_definitions",
                                                        lambda: d.getStr16(remove_last=False))
            scenario.map.unk_before_empty = self._read("scenario.map.unk_before_empty", lambda: d.getBytes(2))
            scenario.map.empty = self._read("scenario.map.empty", lambda: d.getStr16(remove_last=False))
            scenario.map.unk_before_w_h = self._read("scenario.map.unk_before_w_h", lambda: d.getBytes(10))
            w = self._read("w_map", d.get_s32)

            h = self._read("h_map", d.get_s32)  # starting camera

            scenario.map.camera = x, y
            scenario.map.resize(w, h)

            for i, tile in enumerate(self.scenario.tiles):
                tile.type = self._read(None, d.getInt8)
                tile.elevation = self._read(None, d.getInt8)
                tile.unknown1 = self._read(None, d.getInt8)
                tile.unknown2 = self._read(None, d.getInt8)
                tile.unknown3 = self._read(None, d.getInt8)
                tile.layer_type = self._read(None, d.getInt8)
                tile.is_layering = self._read(None, d.getInt8)  # 0 if yes
        else:
            scenario.unknown_bytes_before_w_h = self._read("scenario.map.unknown_bytes_before_w_h",
                                                           lambda: d.getBytes(16))
            w = self._read("w_map", d.get_s32)
            h = self._read("h_map", d.get_s32)  # starting camera

            scenario.map.camera = x, y
            scenario.map.resize(w, h)

            for i, tile in enumerate(self.scenario.tiles):
                tile.type = self._read(None, d.getInt8)
                tile.elevation = d.getInt8()
                tile.unknown = d.getInt8()

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
            resource.food = self._read("P{} food=".format(i), d.getFloat)
            resource.wood = self._read("P{} wood=".format(i), d.getFloat)
            resource.gold = self._read("P{} gold=".format(i), d.getFloat)
            resource.stone = self._read("P{} stone=".format(i), d.getFloat)
            resource.ore = self._read("P{} ore ==".format(i), d.getFloat)
            resource.padding = self._read("P{} padding=".format(i), d.get_s32)
            players[i].population = self._read("P{} max pop ? =".format(i), d.getFloat)

        if self.scenario.header_type is HT_AOE2_DE:
            pass
        else:

            logger.debug("-------------------------------------------------------")
            logger.debug("-------------------------------------------------------")
            logger.debug("-------------------------------------------------------")
            logger.debug("---------------------- UNITS SECTION (HD) -------------")
            logger.debug("-------------------------------------------------------")
            logger.debug("-------------------------------------------------------")
            logger.debug("-------------------------------------------------------")

            for i in range(9):
                units = self._read("units for player[{}]".format(i), d.get_u32)
                for u in range(units):
                    scenario.units.new(owner=i, x=d.getFloat(), y=d.getFloat(),
                                       unknown1=d.getFloat(), id=d.get_u32(), type=d.get_u16(),
                                       unknown2=d.getInt8(), angle=d.getFloat(), frame=d.get_u16(),
                                       inId=d.get_s32())

        d.skip_constant(9)  # number of plyers, again
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- Player Data 3 Section ----------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        for i in range(1, 9):  # only for playable players
            players[i].constName = self._read("players[{}].constName".format(i), d.getStr16)
            players[i].camera.x = self._read("players[{}].camera.x".format(i), d.getFloat)
            players[i].camera.y = self._read("players[{}].camera.y".format(i), d.getFloat)
            players[i].camera.unknown1 = self._read("players[{}].camera.unknown1".format(i), d.get_s16)
            players[i].camera.unknown2 = self._read("players[{}].camera.unknown2".format(i), d.get_s16)
            players[i].allyVictory = self._read("players[{}].allyVictory".format(i), d.getInt8)
            players[i].dip = self._read("players[{}].dip".format(i),
                                        d.get_u16)  # Player count for diplomacy # TODO compress
            d.skip(players[i].dip * 1)  # 0 = allied, 1 = neutral, 2 = ? , 3 = enemy
            #  d.skip(dip*4)  # 0 = GAIA, 1 = self,
            #  2 = allied, 3 = neutral, 4 = enemy
            for j in range(9):
                players[i].diplomacy.gaia[j] = self._read("players[{}].diplomacy.gaia[{}]".format(i, j), d.get_s32)
            players[i].color = self._read("players[{}].color".format(i), d.get_u32)
            players[i].unk1 = self._read("players[{}].unk1".format(i), d.getFloat)  # TODO compress
            players[i].unk2 = self._read("players[{}].unk2".format(i), d.get_u16)  # TODO compress
            if players[i].unk1 == 2.0:
                d.skip(8 * 1)  # TODO decompress/compress
            d.skip(players[i].unk2 * 44)  # TODO decompress/compress
            d.skip(7 * 1)  # TODO decompress/compress
            d.skip(4)  # TODO decompress/compress

        self._read("skip after player data 3 ", lambda: d.getBytes(2))  # TODO compress

        self._read("unk after player data 3", d.getInt8)  # unknown # TODO compress

        if self.scenario.header_type is HT_AOE2_DE:
            logger.debug("-------------------------------------------------------")
            logger.debug("-------------------------------------------------------")
            logger.debug("-------------------------------------------------------")
            logger.debug("---------------------- UNITS SECTION (DE) -------------")
            logger.debug("-------------------------------------------------------")
            logger.debug("-------------------------------------------------------")
            logger.debug("-------------------------------------------------------")
            something = self._read("something", d.getInt8)
            for i in range(1, 9):

                number_of_units = self._read("number_of_units[{}]".format(i), d.get_u32)

                for u in range(number_of_units):
                    scenario.units.new(owner=i,
                                       x=self._read("x [{}][{}]".format(i, u), d.getFloat),
                                       y=self._read("y [{}][{}]".format(i, u), d.getFloat),
                                       unknown1=self._read("unknown1 [{}][{}]".format(i, u), d.getFloat),
                                       id=self._read("id [{}][{}]".format(i, u), d.get_u32),
                                       type=self._read("type [{}][{}]".format(i, u), d.get_u16),
                                       unknown2=self._read("unknown2 [{}][{}]".format(i, u), d.getInt8),
                                       angle=self._read("angle [{}][{}]".format(i, u), d.getFloat),
                                       frame=self._read("frame [{}][{}]".format(i, u), d.get_u16),
                                       inId=self._read("inId [{}][{}]".format(i, u), d.get_s32))

        if self.scenario.header_type is HT_AOE2_DE:
            self.scenario.ukn_9_bytes_before_triggers = self._read("scenario.ukn_9_bytes_before_triggers",
                                                                   lambda: d.getBytes(9))
        n = self._read("number of triggers".format(i), d.get_u32)  # number of triggers

        for id_trigger in range(n):

            trigger = Trigger()  # TODO compress
            self.scenario.add(trigger)
            trigger.id = id_trigger
            trigger.enable = self._read("trigger[{}].enable".format(id_trigger), d.get_u32)
            trigger.loop = self._read("trigger[{}].loop".format(id_trigger), d.getInt8)
            trigger.trigger_description["string_table_id"] = \
                self._read("trigger[{}].trigger_description[\"string_table_id\"]".format(id_trigger), d.getInt8)
            trigger.unknowns[0] = self._read(None, d.getInt8)
            trigger.unknowns[1] = self._read(None, d.getInt8)
            trigger.unknowns[2] = self._read(None, d.getInt8)
            trigger.display_as_objective = \
                self._read("trigger[{}].display_as_objective".format(id_trigger), d.getInt8)
            trigger.description_order = self._read("[id={}] trigger.description_order".format(id_trigger), d.get_u32)
            trigger.make_header = self._read("[id={}] trigger.make_header".format(id_trigger), d.getInt8)
            trigger.short_description["string_table_id"] = \
                self._read("trigger[{}].short_description[\"string_table_id\"]".format(id_trigger), d.getInt8)
            trigger.unknowns[3] = self._read(None, d.getInt8)
            trigger.unknowns[4] = self._read(None, d.getInt8)
            trigger.unknowns[5] = self._read(None, d.getInt8)
            trigger.short_description["display_on_screen"] = \
                self._read("trigger[{}].short_description[\"display_on_screen\"]".format(id_trigger), d.getInt8)
            trigger.unknowns[6] = self._read(None, d.getInt8)
            trigger.unknowns[7] = self._read(None, d.getInt8)
            trigger.unknowns[8] = self._read(None, d.getInt8)
            trigger.unknowns[9] = self._read(None, d.getInt8)
            trigger.unknowns[10] = self._read(None, d.getInt8)
            logger.debug("trigger[{}].unknowns={}".format(id_trigger, trigger.unknowns))
            trigger.mute_objectives = self._read("trigger[{}].mute_objectives".format(id_trigger), d.getInt8)
            trigger.trigger_description["text"] = \
                self._read("trigger[{}].trigger_description[\"text\"]".format(id_trigger), d.getStr32)
            trigger.name = self._read("trigger[{}].name".format(id_trigger), d.getStr32)
            trigger.short_description["text"] = \
                self._read("trigger[{}].short_description[\"text\"]".format(id_trigger), d.getStr32)

            logger.debug("PROCESSING EFFECTS")
            ne = self._read("number of effect({})".format(id_trigger), d.get_s32)  # number of effects
            for e in range(ne):
                effect = Effect()
                trigger.then_(effect)
                effect.type = self._read("type({}/{})".format(e, id_trigger), d.get_s32)
                effect.check = self._read("check({}/{})".format(e, id_trigger), d.get_s32)
                if effect.check != 24:
                    logger.warning(
                        "check attribut is '{}' for effects but should be 24 for aoe2scenario ???!!".format(check))
                effect.aiGoal = self._read("trigger[{}].effect[{}].aiGoal".format(id_trigger,e), d.get_s32)
                effect.amount = self._read("trigger[{}].effect[{}].amount".format(id_trigger,e), d.get_s32)
                effect.resource = self._read("trigger[{}].effect[{}].resource".format(id_trigger,e), d.get_s32)
                effect.state = self._read("trigger[{}].effect[{}].state".format(id_trigger,e), d.get_s32)

                effect.selectedCount = self._read("trigger[{}].effect[{}].selectedCount".format(id_trigger,e), d.get_s32)
                effect.unitId = self._read("trigger[{}].effect[{}].unitId".format(id_trigger,e), d.get_s32)

                effect.unitName = self._read("trigger[{}].effect[{}].unitName".format(id_trigger,e), d.get_s32)
                effect.source_player = self._read("trigger[{}].effect[{}].sourcePlayer".format(id_trigger,e), d.get_s32)
                effect.target_player = self._read("trigger[{}].effect[{}].targetPlayer".format(id_trigger,e), d.get_s32)

                effect.tech = self._read("trigger[{}].effect[{}].tech".format(id_trigger,e), d.get_s32)

                effect.stringId = self._read("trigger[{}].effect[{}].stringId".format(id_trigger,e), d.get_s32)
                effect.unknown1 = self._read("trigger[{}].effect[{}].unknown1".format(id_trigger,e), d.get_s32)
                effect.time = self._read("trigger[{}].effect[{}].time".format(id_trigger,e), d.get_s32)

                triggerId = self._read("trigger[{}].effect[{}].triggerId".format(id_trigger,e), d.get_s32)
                effect.trigger_to_activate = Trigger(id=triggerId)
                effect.x = self._read("trigger[{}].effect[{}].x".format(id_trigger,e), d.get_s32)
                effect.y = self._read("trigger[{}].effect[{}].y".format(id_trigger,e), d.get_s32)
                effect.x1 = self._read("trigger[{}].effect[{}].x1".format(id_trigger,e), d.get_s32)

                effect.y1 = self._read("trigger[{}].effect[{}].y1".format(id_trigger,e), d.get_s32)
                effect.x2 = self._read("trigger[{}].effect[{}].x2".format(id_trigger,e), d.get_s32)
                effect.y2 = self._read("trigger[{}].effect[{}].y2".format(id_trigger,e), d.get_s32)
                effect.unitGroup = self._read("trigger[{}].effect[{}].unitGroup".format(id_trigger,e), d.get_s32)
                effect.unitType = self._read("trigger[{}].effect[{}].unitType".format(id_trigger,e), d.get_s32)
                effect.instructionId = self._read("trigger[{}].effect[{}].instructionId".format(id_trigger,e), d.get_s32)

                effect.unknown2 = self._read("trigger[{}].effect[{}].unknown2".format(id_trigger,e), d.get_s32)
                effect.text = self._read("trigger[{}].effect[{}].text".format(id_trigger,e), d.getStr32)
                effect.filename = self._read("trigger[{}].effect[{}].filename".format(id_trigger,e), d.getStr32)

                for k in range(effect.selectedCount):
                    unitid = self._read("trigger[{}].effect[{}].unitid[{}]".format(id_trigger,e,k), d.get_s32)
                    effect.unitIds.append(unitid)
            d.skip(ne * 4)  # effects order

            nc = d.get_s32()  # number of conditions
            logger.debug("PROCESSING CONDITIONS")
            logger.debug("number of conditions : {}".format(nc))

            for c in range(nc):
                type_ = self._read("type_({},{})".format(c, id_trigger), d.get_u32)
                check = self._read("check({},{})".format(c, id_trigger), d.get_s32)
                amount = self._read("amount({},{})".format(c, id_trigger), d.get_s32)
                resource = self._read("resource({},{})".format(c, id_trigger), d.get_s32)
                unitObject = self._read("unitObject({},{})".format(c, id_trigger), d.get_s32)
                unitId = self._read("unitId({},{})".format(c, id_trigger), d.get_s32)
                unitName = self._read("unitName({},{})".format(c, id_trigger), d.get_s32)
                sourcePlayer = self._read("sourcePlayer({},{})".format(c, id_trigger), d.get_s32)
                tech = self._read("tech({},{})".format(c, id_trigger), d.get_s32)
                timer = self._read("timer({},{})".format(c, id_trigger), d.get_s32)
                unknown1 = self._read("unknown1({},{})".format(c, id_trigger), d.get_s32)
                x1 = self._read("x1({},{})".format(c, id_trigger), d.get_s32)
                y1 = self._read("y1({},{})".format(c, id_trigger), d.get_s32)
                x2 = self._read("x2({},{})".format(c, id_trigger), d.get_s32)
                y2 = self._read("y2({},{})".format(c, id_trigger), d.get_s32)
                unitGroup = self._read("unitGroup({},{})".format(c, id_trigger), d.get_s32)
                unitType = self._read("unitType({},{})".format(c, id_trigger), d.get_s32)
                aiSignal = self._read("aiSignal({},{})".format(c, id_trigger), d.get_s32)
                reversed = self._read("reversed({},{})".format(c, id_trigger), d.get_s32)
                unknown2 = self._read("unknown2({},{})".format(c, id_trigger), d.get_s32)
                triggers[id_trigger].newCondition(
                    type=type_, check=check, amount=amount,
                    resource=resource, unitObject=unitObject,
                    unitId=unitId, unitName=unitName,
                    sourcePlayer=sourcePlayer, tech=tech,
                    timer=timer, unknown1=unknown1, x1=x1, y1=y1, x2=x2,
                    y2=y2, unitGroup=unitGroup,
                    unitType=unitType, aiSignal=aiSignal, reversed=reversed, unknown2=unknown2
                )

            d.skip(nc * 4)  # conditions order
        d.skip(n * 4)

        # not very well optimized if you ask me
        for id_trigger in scenario.triggers:
            for e in id_trigger.effects:
                if e.type == EffectType.ACTIVATE_TRIGGER.value:
                    if e.trigger_to_activate.id != -1:
                        for tr in scenario.triggers:
                            if tr.id == e.trigger_to_activate.id:
                                e.trigger_to_activate = tr

        # print("last bytes")
        # print(decoder.getBytes(1000))
        debug.included = d.get_u32()
        debug.error = d.get_u32()
        if debug.included:
            debug.raw = d.getBytes(396)  # AI DEBUG file
        """
        for i in range(1, 9):
            examples.players[i].constName   = getStr16()
            examples.players[i].cameraX     = getFloat()
            examples.players[i].cameraY     = getFloat()
            examples.players[i].cameraXX    = getInt16()
            examples.players[i].cameraYY    = getInt16()
            examples.players[i].allyVictory = getInt8()
        """
