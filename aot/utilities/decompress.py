from aot.model.enums.constants import HT_AOE2_HD,HT_AOE2_DE
from aot.utilities import *
from aot.model import *
import zlib
import time

import logging

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
            if len(str_var)> 50:
                str_var = str_var[:50] + " ... [too long to print]"
            logger.debug("[READING][{}] {}=<{}>".format(f.__name__, key, str_var))
        return var

    def decompressHeader(self, data):
        d = Decoder(data)

        self.scenario.version = self._read("header_decompressed.examples.version", lambda: d.getAscii(length=4))
        length = self._read("header_decompressed.lenght", d.get_s32)  # header length
        self.scenario.header_type = self._read("header_decompressed.header_type", d.get_s32)
        if self.scenario.header_type not in [HT_AOE2_DE,HT_AOE2_HD]:
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
            #exit()
        return d.offset()

    def unzip(self, bytes):
        return zlib.decompress(bytes, -zlib.MAX_WBITS)

    def decompressData(self, bData):
        d = Decoder(bData)

        # Shortcuts: Scenario
        scenario = self.scenario
        players = self.scenario.players
        messages = self.scenario.messages
        triggers = self.scenario.triggers

        #########################
        ### COMPRESSED HEADER ###
        #########################

        scenario.units.nextID = self._read("units.nextID", d.get_u32)
        self.scenario.version2 = self._read("version2", d.getFloat)

        for i in range(1, 17):
            players[i].name = self._read("player_{}.name".format(i), lambda: d.getAscii(256))

        for i in range(1, 17):
            players[i].nameID = self._read("player_{}.nameID".format(i), d.get_s32)

        for i in range(1, 17):
            players[i].active = self._read("player_{}.active".format(i), d.get_u32)
            players[i].human = self._read("player_{}.human".format(i), d.get_u32)
            players[i].civilization = self._read("player_{}.civilization".format(i), d.get_u32)
            players[i].unknown1 = self._read("player_{}.unknown1".format(i), d.get_u32)

        scenario.unknown1_compressed_header = self._read("unknown1_compressed_header", d.get_s32)  # unk1
        scenario.unknown2_compressed_header = self._read("unknown2_compressed_header", d.get_s32)  # unk2
        scenario.separator_at_compressed_header = self._read("separator_at_compressed_header",
                                                             lambda: d.getBytes(1))  # unk1
        scenario.filename = self._read("original_filename", lambda: d.getStr16(remove_last=False))  # original filename

        #########################
        ### MESSAGES ###
        #########################

        messages.objectives.id = self._read("messages.objectives.id", f=d.get_u32)
        messages.hints.id = self._read("messages.hints.id", f=d.get_u32)
        messages.victory.id = self._read("messages.victory.id", f=d.get_u32)
        messages.loss.id = self._read("messages.loss.id", f=d.get_u32)
        messages.history.id = self._read("messages.history.id", f=d.get_u32)
        messages.scouts.id = self._read("messages.scouts.id", f=d.get_u32)
        messages.objectives.text = self._read("messages.objectives.text", f=lambda: d.getStr16(remove_last=False))
        messages.hints.text = self._read("messages.hints.text", f=lambda: d.getStr16(remove_last=False))
        messages.victory.text = self._read("messages.victory.text", f=lambda: d.getStr16(remove_last=False))
        messages.loss.text = self._read("messages.loss.text", f=lambda: d.getStr16(remove_last=False))
        messages.history.text = self._read("messages.history.text", f=lambda: d.getStr16(remove_last=False))
        messages.scouts.text = self._read("messages.scouts.text ", f=lambda: d.getStr16(remove_last=False))

        # section: CINEMATICS
        scenario.cinematics.intro = self._read("examples.cinematics.intro", f=lambda: d.getStr16(remove_last=False))
        scenario.cinematics.defeat = self._read("examples.cinematics.defeat", f=lambda: d.getStr16(remove_last=False))
        scenario.cinematics.victory = self._read("examples.cinematics.victory", f=lambda: d.getStr16(remove_last=False))

        # section: BACKGROUND

        if scenario.header_type == HT_AOE2_DE:
            scenario.unknown_bytes_after_cinematics = self._read("examples.unknown_bytes_after_cinematics",lambda : d.getBytes(20))

        scenario.background.filename = self._read("examples.background.filename",
                                                  f=lambda: d.getStr16(remove_last=False))

        #self._read("xaxa",lambda : d.getBytes(100))

        scenario.background.included = self._read("examples.background.included", f=d.get_s32)
        scenario.background.width = self._read("examples.background.width", f=d.get_s32)
        scenario.background.height = self._read("examples.background.height", f=d.get_s32)
        self.scenario.background.include = self._read("self.examples.background.include", d.get_s16)

        if (self.scenario.background.include == -1 or self.scenario.background.include == 2):
            scenario.size = self._read("examples.size", d.get_u32)
            scenario.width = self._read("examples.width", d.get_s32)
            scenario.height = self._read("examples.height ", d.get_s32)
            scenario.planes = self._read("examples.planes", d.get_s16)
            scenario.bitCount = self._read("examples.bitCount", d.get_s16)
            scenario.compression = self._read("examples.compression", d.get_s32)
            scenario.sizeImage = self._read("examples.sizeImage", d.get_s32)
            scenario.xPels = self._read("examples.xPels", d.get_s32)
            scenario.yPels = self._read("examples.yPels", d.get_s32)
            scenario.colors = self._read("examples.colors", d.get_u32)
            scenario.iColors = self._read("examples.iColors", d.get_s32)
            scenario.colorTable = self._read("examples.colorTable", lambda: d.getBytes(scenario.colors * 4))
            scenario.rawData = self._read("examples.rawData", lambda: d.getBytes(scenario.sizeImage))

        if scenario.header_type == HT_AOE2_DE:
            logger.debug(d.getBytes(200))
           # exit()
            logger.debug(d.getBytes(8))
            #
            #logger.debug(d.getStr32())
            xaxa = self._read("xaxa",  d.getStr16)
            logger.debug(d.getBytes(1000))
            TODO
            exit()

        # section: PLAYER DATA 2
        for i in range(1, 17):
            players[i].vc_names = self._read("player_{}.vc_names".format(i), lambda: d.getStr16(remove_last=False))

        for i in range(1, 17):
            players[i].cty_names = self._read("player_{}.cty_names".format(i), lambda: d.getStr16(remove_last=False))

        for i in range(1, 17):
            players[i].per_names = self._read("player_{}.per_names".format(i), lambda: d.getStr16(remove_last=False))

        for i in range(1, 17):
            # not sure of int type here
            #if self.examples.header_type == HT_AOE2_HD:
            players[i].vc_per_length = self._read("player_{}.vc_per_length".format(i), d.get_s32)  # Unknown 1
            players[i].cty_per_length = self._read("player_{}.cty_per_length".format(i), d.get_s32)  # Unknown 1
            players[i].per_per_length = self._read("player_{}.per_per_length".format(i), d.get_s32)

            players[i].vc = self._read("player_{}.vc".format(i), lambda: d.getBytes(players[i].vc_per_length))
            players[i].cty = self._read("player_{}.cty".format(i), lambda: d.getBytes(players[i].cty_per_length))
            players[i].per = self._read("player_{}.per".format(i), lambda: d.getBytes(players[i].per_per_length))

            #elif self.examples.header_type == HT_AOE2_DE:
               #players[i].vc_per_length = self._read("player_{}.vc_per_length".format(i), d.getInt8)  # Unknown 1
                #players[i].cty_per_length = self._read("player_{}.cty_per_length".format(i), d.getInt8)  # Unknown 1
                #players[i].per_per_length = self._read("player_{}.per_per_length".format(i), d.getInt8)  # Unknown 1

                #players[i].vc = self._read("player_{}.vc".format(i), lambda: d.getBytes(players[i].vc_per_length))
                #players[i].cty = self._read("player_{}.cty".format(i), lambda: d.getBytes(players[i].cty_per_length))
                #players[i].per = self._read("player_{}.per".format(i), lambda: d.getBytes(players[i].per_per_length))

               #players[i].vc = self._read("player_{}.vc".format(i),d.getStr16)
               # players[i].cty = self._read("player_{}.cty".format(i), d.getStr16)
               # players[i].per = self._read("player_{}.per".format(i), d.getStr16)



        for i in range(1, 17):
            players[i].ai.type = self._read("player_{}.ai.type".format(i), d.getInt8)

        self._read("skip sep after AI", d.skip_separator)  # Separator 0xFFFFFF9D
        for i in range(1, 17):
            players[i]._unused_resource.gold = self._read("player_{}.unused_resource.gold".format(i), d.get_s32)
            players[i]._unused_resource.wood = self._read("player_{}.unused_resource.wood".format(i), d.get_s32)
            players[i]._unused_resource.food = self._read("player_{}.unused_resource.food".format(i), d.get_s32)
            players[i]._unused_resource.stone = self._read("player_{}.unused_resource.stone".format(i), d.get_s32)
            players[i]._unused_resource.ore = self._read("player_{}.unused_resource.ore".format(i), d.get_s32)
            players[i]._unused_resource.padding = self._read("player_{}.unused_resource.padding".format(i), d.get_s32)
            players[i]._unused_resource.index = self._read("player_{}.unused_resource.index".format(i), d.get_s32)

        self._read("skip sep after unused resources", d.skip_separator)  # Separator 0xFFFFFF9D

        # section: Goals
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

        # section: Diplomacy
        for i in range(1, 17):
            for j in range(1, 17):
                players[i].diplomacy[j] = self._read("P{} diplo for P{} is :".format(i, j), d.get_s32)

        scenario.big_skip_after_diplo = self._read("big_skip_after_diplo", lambda: d.getBytes(11520))  # unused space
        d.skip_separator()  # separator

        for i in range(1, 17):
            players[i].ally_vic = self._read("P{} ally vic =".format(i), d.get_s32)

        d.skip_constant(67109120)  # 4 unknown bytes

        ############
        # DISABLES #
        ############

        logger.debug("tech count : {}".format(d.unpack('i' * 16)))
        for i in range(1, 17):
            players[i].disabledTechs = [d.get_s32() for _ in range(30)]
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
        # AGE
        print("----")
        for i in range(1, 17):
            players[i].age = self._read("P{} age=".format(i), d.get_s32)
            # print("reading age ",players[i].age)

        d.skip_separator()  # separator

        # ======== MAP ========
        x = self._read("x_camera", d.get_s32)
        y = self._read("y_camera", d.get_s32)  # starting camera
        scenario.map.aiType = self._read("examples.map.aiType", d.get_u32)

        scenario.unknown_bytes_before_w_h = self._read("examples.unknown_bytes_before_w_h", lambda: d.getBytes(16))

        w = self._read("w_map", d.get_s32)
        h = self._read("h_map", d.get_s32)  # starting camera

        scenario.map.camera = x, y
        scenario.map.resize(w, h)

        for i, tile in enumerate(self.scenario.tiles):
            tile.type = self._read(None, d.getInt8)
            tile.elevation = d.getInt8()
            tile.unknown = d.getInt8()

        d.skip_constant(9)  # number of unit sections, N. I've always seen = 9.

        for i in range(1, 9):
            resource = players[i].resource
            resource.food = self._read("P{} food=".format(i), d.getFloat)
            resource.wood = self._read("P{} wood=".format(i), d.getFloat)
            resource.gold = self._read("P{} gold=".format(i), d.getFloat)
            resource.stone = self._read("P{} stone=".format(i), d.getFloat)
            resource.ore = self._read("P{} ore ==".format(i), d.get_s32)
            resource.padding = self._read("P{} padding=".format(i), d.get_s32)
            players[i].population = self._read("P{} max pop ? =".format(i), d.getFloat)

        # Units section
        for i in range(9):
            units = d.get_u32()
            for u in range(units):
                scenario.units.new(owner=i, x=d.getFloat(), y=d.getFloat(),
                                   unknown1=d.getFloat(), id=d.get_u32(), type=d.get_u16(),
                                   unknown2=d.getInt8(), angle=d.getFloat(), frame=d.get_u16(),
                                   inId=d.get_s32())

        d.skip_constant(9)  # number of plyers, again

        for i in range(1, 9):  # only for playable players
            players[i].constName = d.getStr16()
            players[i].camera.x = d.getFloat()
            players[i].camera.y = d.getFloat()
            players[i].camera.unknown1 = d.get_s16()
            players[i].camera.unknown2 = d.get_s16()
            players[i].allyVictory = d.getInt8()
            dip = d.get_u16()  # Player count for diplomacy
            d.skip(dip * 1)  # 0 = allied, 1 = neutral, 2 = ? , 3 = enemy
            #  d.skip(dip*4)  # 0 = GAIA, 1 = self,
            #  2 = allied, 3 = neutral, 4 = enemy
            for j in range(9):
                players[i].diplomacy.gaia[j] = d.get_s32()
            players[i].color = d.get_u32()
            unk1 = d.getFloat()
            unk2 = d.get_u16()
            if unk1 == 2.0:
                d.skip(8 * 1)
            d.skip(unk2 * 44)
            d.skip(7 * 1)
            d.skip(4)
        d.skip(8)

        d.getInt8()  # unknown

        n = d.get_u32()  # number of triggers
        for t in range(n):
            triggers.new(
                enable=self._read("enable( /{})".format(t), d.get_u32),
                loop=self._read("loop( /{})".format(t), d.get_u32),
                unknown1=self._read("unknown1( /{})".format(t), d.getInt8),
                objective=self._read("objective( /{})".format(t), d.getInt8),
                objectiveOrd=self._read("objectiveOrd( /{})".format(t), d.get_u32),
                unknown2=self._read("unknown2( /{})".format(t), d.get_u32),
                text=self._read("text( /{})".format(t), d.getStr32),
                name=self._read("name( /{})".format(t), d.getStr32),
                id=t
            )
            logger.debug("PROCESSING EFFECTS")
            ne = self._read("number of effect( /{})".format(t), d.get_s32)  # number of effects
            for e in range(ne):
                type = self._read("type({}/{})".format(e, t), d.get_s32)
                check = self._read("check({}/{})".format(e, t), d.get_s32)
                if check != 24:
                    logger.warning(
                        "check attribut is '{}' for effects but should be 24 for aoe2scenario ???!!".format(check))
                aiGoal = self._read("aiGoal({}/{})".format(e, t), d.get_s32)
                amount = self._read("amount({}/{})".format(e, t), d.get_s32)
                resource = self._read("resource({}/{})".format(e, t), d.get_s32)
                state = self._read("state({}/{})".format(e, t), d.get_s32)

                selectedCount = self._read("selectedCount({}/{})".format(e, t), d.get_s32)
                unitId = self._read("unitId({}/{})".format(e, t), d.get_s32)

                unitName = self._read("unitName({}/{})".format(e, t), d.get_s32)
                sourcePlayer = self._read("sourcePlayer({}/{})".format(e, t), d.get_s32)
                targetPlayer = self._read("targetPlayer({}/{})".format(e, t), d.get_s32)

                tech = self._read("tech({}/{})".format(e, t), d.get_s32)

                stringId = self._read("stringId({}/{})".format(e, t), d.get_s32)
                unknown1 = self._read("unknown1({}/{})".format(e, t), d.get_s32)
                time = self._read("time({}/{})".format(e, t), d.get_s32)

                triggerId = self._read("triggerId({}/{})".format(e, t), d.get_s32)
                x = self._read("x({}/{})".format(e, t), d.get_s32)
                y = self._read("y({}/{})".format(e, t), d.get_s32)
                x1 = self._read("x1({}/{})".format(e, t), d.get_s32)

                y1 = self._read("y1({}/{})".format(e, t), d.get_s32)
                x2 = self._read("x2({}/{})".format(e, t), d.get_s32)
                y2 = self._read("y2({}/{})".format(e, t), d.get_s32)
                unitGroup = self._read("unitGroup({}/{})".format(e, t), d.get_s32)
                unitType = self._read("unitType({}/{})".format(e, t), d.get_s32)
                instructionId = self._read("instructionId({}/{})".format(e, t), d.get_s32)

                unknown2 = self._read("unknown2({}/{})".format(e, t), d.get_s32)
                text = self._read("text({}/{})".format(e, t), d.getStr32)
                filename = self._read("filename({}/{})".format(e, t), d.getStr32)

                triggers[t].newEffect(
                    type=type,
                    check=check,
                    aiGoal=aiGoal,
                    amount=amount,
                    resource=resource,
                    state=state,
                    selectedCount=selectedCount,
                    unitId=unitId,
                    unitName=unitName,
                    sourcePlayer=sourcePlayer,
                    targetPlayer=targetPlayer,
                    tech=tech,
                    stringId=stringId,
                    unknown1=unknown1,
                    unknown2=unknown2,
                    time=time,
                    trigger_to_activate=Trigger(id=triggerId),
                    x=x,
                    y=y,
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2,
                    unitGroup=unitGroup,
                    unitType=unitType,
                    instructionId=instructionId,
                    text=text,
                    filename=filename
                )
                for k in range(triggers[t].effects[e].selectedCount):
                    unitid = self._read("Unit number id ({},{})".format(k,t), d.get_s32)
                    triggers[t].effects[e].unitIds.append(unitid)
            d.skip(ne * 4)  # effects order

            nc = d.get_s32()  # number of conditions
            logger.debug("PROCESSING CONDITIONS")
            logger.debug("number of conditions : {}".format(nc))

            for c in range(nc):
                type_ = self._read("type_({},{})".format(c,t), d.get_u32)
                check = self._read("check({},{})".format(c,t), d.get_s32)
                amount = self._read("amount({},{})".format(c,t), d.get_s32)
                resource = self._read("resource({},{})".format(c,t), d.get_s32)
                unitObject = self._read("unitObject({},{})".format(c,t), d.get_s32)
                unitId = self._read("unitId({},{})".format(c,t), d.get_s32)
                unitName = self._read("unitName({},{})".format(c,t), d.get_s32)
                sourcePlayer = self._read("sourcePlayer({},{})".format(c,t), d.get_s32)
                tech = self._read("tech({},{})".format(c,t), d.get_s32)
                timer = self._read("timer({},{})".format(c,t), d.get_s32)
                unknown1 = self._read("unknown1({},{})".format(c,t), d.get_s32)
                x1 =self._read("x1({},{})".format(c,t), d.get_s32)
                y1 = self._read("y1({},{})".format(c,t), d.get_s32)
                x2 = self._read("x2({},{})".format(c,t), d.get_s32)
                y2 = self._read("y2({},{})".format(c,t), d.get_s32)
                unitGroup =self._read("unitGroup({},{})".format(c,t), d.get_s32)
                unitType =self._read("unitType({},{})".format(c,t), d.get_s32)
                aiSignal = self._read("aiSignal({},{})".format(c,t), d.get_s32)
                reversed = self._read("reversed({},{})".format(c,t), d.get_s32)
                unknown2 =self._read("unknown2({},{})".format(c,t), d.get_s32)
                triggers[t].newCondition(
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
        for t in scenario.triggers:
            for e in t.effects:
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
