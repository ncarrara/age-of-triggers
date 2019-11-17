import numpy as np

from aot.model.enums.constants import HT_AOE2_DE
from aot.utilities import *
from aot.model import *
import zlib
import os
import logging

from aot.utilities.encoder import Encoder

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
        0  # stra0 = Z_DEFAULT_STRATEGY
        #   tegy:
        #   1 = Z_FILTERED
        #   2 = Z_HUFFMAN_ONLY
        #   3 = Z_RLE
        #   4 = Z_FIXED
    )

    deflated = compress.compress(data)
    deflated += compress.flush()

    return deflated


class Compress:

    def __init__(self, scenario, path):
        self.scenario = scenario
        # self.version = version

        temp0 = "{}_0.temp".format(scenario.filename)
        temp1 = "{}_1.temp".format(scenario.filename)

        f1 = open(temp0, 'wb')
        f2 = open(temp1, 'wb')
        self.compressHeader(f1)
        self.compressData(f2)
        f1.close()
        f2.close()
        data = open(temp0, 'rb').read()
        d = deflate(open(temp1, 'rb').read())
        open(path, 'wb').write(data + d)
        os.remove(temp0)
        os.remove(temp1)

    def compressHeader(self, f):
        encoder = Encoder(f)

        putAscii = encoder.put_ascii
        putUInt32 = encoder.put_u32
        putInt32 = encoder.put_s32
        putStr32 = encoder.put_str32

        putAscii(str(self.scenario.version))
        # if self.examples.is_aoe2scenario:
        len_header = 0
        # else:
        #     len_header = 20 + len(self.examples.instructions)
        putInt32(len_header)  # header length
        putInt32(self.scenario.header_type)  # unknown constant
        putInt32(self.scenario.timestamp)
        putStr32(self.scenario.instructions)
        putUInt32(0)  # unknown constant
        putUInt32(self.scenario.n_players)
        # if self.examples.is_aoe2scenario:
        putUInt32(self.scenario.hd_constant)
        putUInt32(self.scenario.use_expansion)
        putUInt32(len(self.scenario.datasets))
        for dataset in self.scenario.datasets:
            putInt32(dataset)

        putStr32(self.scenario.author)  # todo default
        putInt32(self.scenario.header_unknown)  # todo default

    def compressData(self, f):
        encoder = Encoder(f)
        version = self.scenario.version

        scenario = self.scenario
        players = self.scenario.players
        messages = self.scenario.messages
        triggers = self.scenario.triggers
        debug = self.scenario.debug

        put_ascii = encoder.put_ascii
        put_u32 = encoder.put_u32
        put_s8 = encoder.put_s8
        put_u8 = encoder.put_u8
        put_s16 = encoder.put_s16
        put_u16 = encoder.put_u16
        put_s32 = encoder.put_s32
        put_str16 = encoder.put_str16
        put_str32 = encoder.put_str32
        put_float = encoder.put_float
        put_bytes = encoder.put_bytes

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- COMPRESSED HEADER --------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        put_u32(scenario.units.getNextID())
        put_float(scenario.version2)

        for i in range(1, 17):
            put_ascii(players[i].name, 256)

        for i in range(1, 17):
            put_s32(players[i].nameID)

        for i in range(1, 17):
            if i == 9:
                i = 0  # GAIA is 9th
            if i > 9:
                i -= 1
            put_u32(players[i].active, "player.active")
            put_u32(players[i].human)
            put_u32(players[i].civilization)
            put_u32(players[i].unknown1)

        put_bytes(self.scenario.unknown_bytes_after_civs)  # todo default

        put_str16(scenario.original_filename, remove_last=False) # todo default

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- MESSAGES ----------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        put_s32(messages.objectives.id)
        put_s32(messages.hints.id)
        put_s32(messages.victory.id)
        put_s32(messages.loss.id)
        put_s32(messages.history.id)
        put_s32(messages.scouts.id)

        put_str16(messages.objectives.text, remove_last=False)
        put_str16(messages.hints.text, remove_last=False)
        put_str16(messages.victory.text, remove_last=False)
        put_str16(messages.loss.text, remove_last=False)
        put_str16(messages.history.text, remove_last=False)
        put_str16(messages.scouts.text, remove_last=False)

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- CINEMATICS ----------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        put_str16(scenario.cinematics.intro, remove_last=False)
        put_str16(scenario.cinematics.victory, remove_last=False)
        put_str16(scenario.cinematics.defeat, remove_last=False)

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- BACKGROUND ----------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        put_str16(scenario.background.filename, remove_last=False)
        put_u32(scenario.background.included)
        put_u32(scenario.background.width)
        put_u32(scenario.background.height)
        put_s16(scenario.background.include)

        if (scenario.background.include == - 1 or scenario.background.include == 2):
            put_u32(scenario.size)
            put_s32(scenario.width)
            put_s32(scenario.height)
            put_s16(scenario.planes)
            put_s16(scenario.bitCount)
            put_s32(scenario.compression)
            put_s32(scenario.sizeImage)
            put_s32(scenario.xPels)
            put_s32(scenario.yPels)
            put_u32(scenario.colors)
            put_s32(scenario.iColors)
            put_bytes(scenario.colorTable)
            put_bytes(scenario.rawData)

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- PLAYER DATA 2-------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        for i in range(1, 17):
            put_u32(players[i].unknown_constant)  # todo default

        for i in range(1, 17):
            if i == 9:
                i = 0  # GAIA is 9th
            if i > 9:
                i -= 1
            put_str16(players[i].vc_names, remove_last=False)

        for i in range(1, 17):
            if i == 9:
                i = 0  # GAIA is 9th
            if i > 9:
                i -= 1
            put_bytes(players[i].unknown8bytes)  # todo default
            put_str32(players[i].cty_names, remove_last=False)

        put_bytes(self.scenario.unk_after_civs)  # todo default

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
            put_s32(int(players[i]._unused_resource.gold))
            put_s32(int(players[i]._unused_resource.wood))
            put_s32(int(players[i]._unused_resource.food))
            put_s32(int(players[i]._unused_resource.stone))
            put_s32(int(players[i]._unused_resource.ore))
            put_s32(int(players[i]._unused_resource.padding))
            put_s32(int(players[i]._unused_resource.index))

        put_u32(4294967197)  # Separator, again 0xFFFFFF9D

        # section: Goals
        put_s32(scenario.goals.conquest)
        put_s32(scenario.goals.unknown1)
        put_s32(scenario.goals.relics)
        put_s32(scenario.goals.unknown2)
        put_s32(scenario.goals.exploration)
        put_s32(scenario.goals.unknown3)
        put_s32(scenario.goals.all)
        put_s32(scenario.goals.mode)
        put_s32(scenario.goals.score)
        put_s32(scenario.goals.time)

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- DIPLOMACY ----------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        # section: Diplomacy
        for i in range(1, 17):
            for j in range(1, 17):
                put_s32(players[i].diplomacy[j])

        put_bytes(scenario.big_skip_after_diplo)
        put_u32(4294967197)  # separator

        for i in range(1, 17):  # allied victory
            put_s32(players[i].ally_vic)

        put_s32(67109120)

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- DISABLES -----------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        for i in range(1, 17):  # tech count
            put_s32(len(players[i].disabledTechs))  # todo default
        for i in range(1, 17):  # techs
            for t in players[i].disabledTechs:
                put_s32(t)

        for i in range(1, 17):  # unit count
            put_s32(len(players[i].disabledUnits))  # todo default
        for i in range(1, 17):  # units
            for t in players[i].disabledUnits:
                put_s32(t)

        for i in range(1, 17):  # building count
            put_s32(len(players[i].disabledBuildings))  # todo default
        for i in range(1, 17):  # buildings
            for t in players[i].disabledBuildings:
                put_s32(t)

        put_u32(scenario.unknown1_after_tech)
        put_u32(scenario.unknown1_after_tech)
        put_u32(scenario.is_all_tech)

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- AGE ----------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        for i in range(1, 17):
            put_s32(players[i].age, "age for P{}".format(i))

        put_u32(4294967197)

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- MAP ----------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        put_s32(scenario.map.camera[0])  # warning: doesn't match
        put_s32(scenario.map.camera[1])  # warning: doesn't match

        put_u32(scenario.map.aiType)

        put_bytes(scenario.map.unk_before_water_definitions)  # todo default

        put_str16(scenario.map.water_definitions)  # todo default

        put_bytes(scenario.map.unk_before_empty)  # todo default

        put_str16(scenario.map.empty)  # todo default

        put_bytes(scenario.map.unk_before_w_h)  # todo default

        put_s32(scenario.tiles.size()[0])
        put_s32(scenario.tiles.size()[1])

        for i, tile in enumerate(scenario.tiles):
            put_u8(tile.type)
            put_s8(tile.elevation)
            put_u8(tile.unknown1)  # todo default
            put_u8(tile.unknown2)  # todo default

            put_u8(tile.unknown3)  # todo default
            put_u8(tile.layer_type)  # todo default
            put_u8(tile.is_layering)  # todo default

        put_u32(9)  # number of units section

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------- (DEFAULT ?) RESOURCE------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        for i in range(1, 9):
            put_float(players[i].resource.food)
            put_float(players[i].resource.wood)
            put_float(players[i].resource.gold)
            put_float(players[i].resource.stone)
            put_float(players[i].resource.ore)
            put_s32(players[i].resource.padding)
            put_float(players[i].population)

        put_u32(9)  # number of playable players

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- Player Data 3 Section ----------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        for i in range(1, 9):
            put_str16(players[i].constName)
            put_float(players[i].camera.x)
            put_float(players[i].camera.y)
            put_s16(players[i].camera.unknown1)
            put_s16(players[i].camera.unknown2)
            put_s8(players[i].allyVictory)

            put_u16(players[i].dip)  # todo default
            put_bytes(players[i].unk0)  # todo default

            for j in range(9):
                put_s32(players[i].diplomacy.gaia[j])

            put_u32(players[i].color)
            put_float(players[i].unk1)  # todo default
            put_u16(players[i].unk2)  # todo default
            if players[i].unk1 == 2.0:
                put_bytes(players[i].unk3)  # todo default
            put_bytes(players[i].unk4)  # todo default
            put_bytes(players[i].unk5)  # todo default
            put_bytes(players[i].unk6)  # todo default

        put_bytes(scenario.data3_unk)  # todo default

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- UNITS SECTION (DE) -------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        put_s8(scenario.unk_unit_section)

        for i in range(1, 9):
            number_of_units = len(players[i].units)
            put_u32(number_of_units)
            for unit in players[i].units:
                put_float(unit.x)
                put_float(unit.y)
                put_float(unit.unknown1)
                put_u32(unit.id)
                put_u16(unit.type)
                put_s8(unit.unknown2)
                put_float(unit.angle)
                put_u16(unit.frame)
                put_s32(unit.inId)

        put_bytes(scenario.ukn_9_bytes_before_triggers)

        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("---------------------- TRIGGERS  ----------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")
        logger.debug("-------------------------------------------------------")

        put_s32(len(triggers))

        for trigger in triggers:
            put_u32(trigger.enable)
            put_s8(trigger.loop)
            put_s8(trigger.trigger_description["string_table_id"])
            put_s8(trigger.unknowns[0])
            put_s8(trigger.unknowns[1])
            put_s8(trigger.unknowns[2])
            put_s8(trigger.display_as_objective)
            put_u32(trigger.description_order)
            put_s8(trigger.make_header)
            put_s8(trigger.short_description["string_table_id"])
            put_s8(trigger.unknowns[3])
            put_s8(trigger.unknowns[4])
            put_s8(trigger.unknowns[5])
            put_s8(trigger.short_description["display_on_screen"])
            put_s8(trigger.unknowns[6])
            put_s8(trigger.unknowns[7])
            put_s8(trigger.unknowns[8])
            put_s8(trigger.unknowns[9])
            put_s8(trigger.unknowns[10])
            put_s8(trigger.mute_objectives)
            put_str32(trigger.trigger_description["text"])
            put_str32(trigger.name)
            put_str32(trigger.short_description["text"])

            put_s32(len(trigger.effects))
            for e in range(len(trigger.effects)):
                effect = trigger.effects[e]
                put_s32(effect.type)
                if effect.check is None:
                    effect.check = 24
                put_s32(effect.check)
                put_s32(effect.aiGoal)
                put_s32(effect.amount)
                put_s32(effect.resource)
                put_s32(effect.state)
                put_s32(len(effect.unitIds))  # selected count
                put_s32(effect.unitId)
                put_s32(effect.unitName)
                put_s32(effect.sourcePlayer)
                put_s32(effect.targetPlayer)
                put_s32(effect.tech)
                put_s32(effect.stringId)
                put_s32(effect.unknown1)
                put_s32(effect.time)
                put_s32(-1 if effect.trigger_to_activate is None else effect.trigger_to_activate.id)
                put_s32(effect.x)
                put_s32(effect.y)
                put_s32(effect.x1)
                put_s32(effect.y1)
                put_s32(effect.x2)
                put_s32(effect.y2)
                put_s32(effect.unitGroup)
                put_s32(effect.unitType)
                put_s32(effect.instructionId)
                put_s32(effect.unknown2)
                put_str32(effect.text, "effect.text")
                put_str32(effect.filename, "effect.filename")
                for id in effect.unitIds:
                    put_s32(id)
            for i in range(len(trigger.effects)):
                put_s32(i)
            put_s32(len(trigger.conditions))
            logger.debug("number of conditions : {}".format(len(trigger.conditions)))
            for c in range(len(trigger.conditions)):
                logger.debug(c.__repr__())
                condition = trigger.conditions[c]
                put_u32(condition.type)
                put_s32(condition.check)
                put_s32(condition.amount)
                put_s32(condition.resource, "condition.resource")
                put_s32(condition.unitObject)
                put_s32(condition.unitId)
                put_s32(condition.unitName)
                put_s32(condition.sourcePlayer)
                put_s32(condition.tech)
                put_s32(condition.timer)
                put_s32(condition.unknown1)
                put_s32(condition.x1)
                put_s32(condition.y1)
                put_s32(condition.x2)
                put_s32(condition.y2)
                put_s32(condition.unitGroup)
                put_s32(condition.unitType)
                put_s32(condition.aiSignal)
                put_s32(condition.reversed, "condition.reversed")
                put_s32(condition.unknown2)
            for i in range(len(trigger.conditions)):
                put_s32(i)
        for i in range(len(triggers)):
            put_s32(i)
        put_u32(debug.included)
        put_u32(debug.error)
        if debug.included:
            put_bytes(debug.raw)


# = open('')
if __name__ == "__main__":
    pass
