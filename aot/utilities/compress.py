import numpy as np
from aot.utilities import *
from aot.model import *
import zlib
import os
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

        f1 = open('c1.temp', 'wb')
        f2 = open('c2.temp', 'wb')
        self.compressHeader(f1)
        self.compressData(f2)
        f1.close()
        f2.close()
        data = open('c1.temp', 'rb').read()
        d = deflate(open('c2.temp', 'rb').read())
        open(path, 'wb').write(data + d)
        os.remove("c1.temp")
        os.remove("c2.temp")

    def compressHeader(self, f):
        encoder = Encoder(f)

        putAscii = encoder.putAscii
        putUInt32 = encoder.putUInt32
        putInt32 = encoder.putInt32
        putStr32 = encoder.putStr32

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

    def compressData(self, f):
        encoder = Encoder(f)
        version = self.scenario.version

        scenario = self.scenario
        players = self.scenario.players
        messages = self.scenario.messages
        triggers = self.scenario.triggers
        debug = self.scenario.debug

        putAscii = encoder.putAscii
        putUInt32 = encoder.putUInt32
        putInt8 = encoder.putInt8
        putInt16 = encoder.putInt16
        putUInt16 = encoder.putUInt16
        putInt32 = encoder.putInt32
        putStr16 = encoder.putStr16
        putStr32 = encoder.putStr32
        putFloat = encoder.putFloat
        putBytes = encoder.putBytes

        #########################
        ### COMPRESSED HEADER ###
        #########################

        putUInt32(scenario.units.getNextID())
        putFloat(scenario.version2)

        for i in range(1, 17):
            putAscii(players[i].name, 256)

        for i in range(1, 17):
            putInt32(players[i].nameID)

        for i in range(1, 17):
            putUInt32(players[i].active, "player.active")
            putUInt32(players[i].human)
            putUInt32(players[i].civilization)
            putUInt32(players[i].unknown1)

        putInt32(scenario.unknown1_compressed_header)  # unknown <!>
        putInt32(scenario.unknown2_compressed_header)  # unknown <!>
        putBytes(scenario.separator_at_compressed_header)  # separator
        putStr16(scenario.filename, remove_last=False)

        #########################
        ### MESSAGES ###
        #########################

        putInt32(messages.objectives.id)
        putInt32(messages.hints.id)
        putInt32(messages.victory.id)
        putInt32(messages.loss.id)
        putInt32(messages.history.id)
        putInt32(messages.scouts.id)
        putStr16(messages.objectives.text, remove_last=False)
        putStr16(messages.hints.text, remove_last=False)
        putStr16(messages.victory.text, remove_last=False)
        putStr16(messages.loss.text, remove_last=False)
        putStr16(messages.history.text, remove_last=False)
        putStr16(messages.scouts.text, remove_last=False)

        # section: CINEMATICS
        putStr16(scenario.cinematics.intro, remove_last=False)
        putStr16(scenario.cinematics.victory, remove_last=False)
        putStr16(scenario.cinematics.defeat, remove_last=False)

        # section: BACKGROUND
        putStr16(scenario.background.filename, remove_last=False)
        putInt32(scenario.background.included)
        putInt32(scenario.background.width)
        putInt32(scenario.background.height)
        putInt16(scenario.background.include)

        if (scenario.background.include == - 1 or scenario.background.include == 2):
            putUInt32(scenario.size)
            putInt32(scenario.width)
            putInt32(scenario.height)
            putInt16(scenario.planes)
            putInt16(scenario.bitCount)
            putInt32(scenario.compression)
            putInt32(scenario.sizeImage)
            putInt32(scenario.xPels)
            putInt32(scenario.yPels)
            putUInt32(scenario.colors)
            putInt32(scenario.iColors)
            putBytes(scenario.colorTable)
            putBytes(scenario.rawData)

        # section: PLAYER DATA 2
        for i in range(1, 17):
            putStr16(players[i].vc_names, remove_last=False)

        for i in range(1, 17):
            putStr16(players[i].cty_names, remove_last=False)

        for i in range(1, 17):
            putStr16(players[i].per_names, remove_last=False)

        for i in range(1, 17):
            putInt32(len(players[i].vc))
            putInt32(len(players[i].cty))
            putInt32(len(players[i].per))
            putBytes(players[i].vc)
            putBytes(players[i].cty)
            putBytes(players[i].per)

        for i in range(1, 17):
            putInt8(players[i].ai.type)

        putUInt32(4294967197)  # Separator 0xFFFFFF9D
        for i in range(1, 17):
            putInt32(int(players[i]._unused_resource.gold))
            putInt32(int(players[i]._unused_resource.wood))
            putInt32(int(players[i]._unused_resource.food))
            putInt32(int(players[i]._unused_resource.stone))
            putInt32(int(players[i]._unused_resource.ore))
            putInt32(int(players[i]._unused_resource.padding))
            putInt32(int(players[i]._unused_resource.index))

        putUInt32(4294967197)  # Separator, again 0xFFFFFF9D

        # section: Goals
        putInt32(scenario.goals.conquest)
        putInt32(scenario.goals.unknown1)
        putInt32(scenario.goals.relics)
        putInt32(scenario.goals.unknown2)
        putInt32(scenario.goals.exploration)
        putInt32(scenario.goals.unknown3)
        putInt32(scenario.goals.all)
        putInt32(scenario.goals.mode)
        putInt32(scenario.goals.score)
        putInt32(scenario.goals.time)

        # section: Diplomacy
        for i in range(1, 17):
            for j in range(1, 17):
                # print(players[i].diplomacy[j])
                putInt32(players[i].diplomacy[j])

        putBytes(scenario.big_skip_after_diplo)
        putUInt32(4294967197)  # separator

        for i in range(1, 17):  # allied victory
            putInt32(players[i].ally_vic)

        putInt32(67109120)

        ############
        # DISABLES #
        ############

        for i in range(1, 17):  # tech count
            putInt32(np.sum(np.where(np.asarray(players[i].disabledTechs) > -1)))
        for i in range(1, 17):  # techs
            for t in players[i].disabledTechs:
                putInt32(t)

        for i in range(1, 17):  # unit count
            putInt32(np.sum(np.where(np.asarray(players[i].disabledUnits) > -1)))
        for i in range(1, 17):  # units
            for t in players[i].disabledUnits:
                putInt32(t)

        for i in range(1, 17):  # building count
            putInt32(np.sum(np.where(np.asarray(players[i].disabledBuildings) > -1)))
        for i in range(1, 17):  # buildings
            for t in players[i].disabledBuildings:
                putInt32(t)

        putUInt32(scenario.unknown1_after_tech)
        putUInt32(scenario.unknown1_after_tech)
        putUInt32(scenario.is_all_tech)
        # AGE

        for i in range(1, 17):
            putInt32(players[i].age,"age for P{}".format(i))

        putUInt32(4294967197)

        # ======== MAP ========
        putInt32(scenario.map.camera[0])  # warning: doesn't match
        putInt32(scenario.map.camera[1])  # warning: doesn't match
        putUInt32(scenario.map.aiType)

        putBytes(scenario.unknown_bytes_before_w_h)

        putInt32(scenario.tiles.size()[0])
        putInt32(scenario.tiles.size()[1])

        for i, tile in enumerate(scenario.tiles):
            putInt8(tile.type)
            if tile.type > 100:
                raise Exception("impposible")
            putInt8(tile.elevation)
            putInt8(tile.unknown)

        putUInt32(9)  # number of units section

        for i in range(1, 9):
            putFloat(players[i].resource.food)
            putFloat(players[i].resource.wood)
            putFloat(players[i].resource.gold)
            putFloat(players[i].resource.stone)
            putFloat(players[i].resource.ore)
            putInt32(players[i].resource.padding)
            putFloat(players[i].population)

        # Units section
        for i in range(9):
            # warning: maybe not correct value
            putUInt32(len(players[i].units))
            for unit in players[i].units:
                putFloat(unit.x)
                putFloat(unit.y)
                putFloat(unit.unknown1)
                putUInt32(unit.id)
                putUInt16(unit.type)
                putInt8(unit.unknown2)
                putFloat(unit.angle)
                putUInt16(unit.frame)
                putInt32(unit.inId)

        putUInt32(9)  # number of playable players
        for i in range(1, 9):
            putStr16(players[i].constName)
            putFloat(players[i].camera.x)
            putFloat(players[i].camera.y)
            putInt16(players[i].camera.unknown1)
            putInt16(players[i].camera.unknown2)
            putInt8(players[i].allyVictory)
            putUInt16(9)  # players for diplomacy
            for j in range(1, 9):
                putInt8(players[i].diplomacy[j-1])
            putInt8(0)  # gaia player
            for j in range(9):  # for gaia
                putInt32(players[i].diplomacy.gaia[j])
            putUInt32(players[i].color)
            putFloat(2.0)
            putUInt16(0)
            for j in range(8):
                putInt8(0)
            for j in range(7):
                putInt8(0)
            putInt32(-1)
        putUInt32(2576980378)
        putUInt32(1073322393)
        putInt8(0)
        putInt32(len(triggers))

        for trigger in triggers:
            putUInt32(trigger.enable)
            putUInt32(trigger.loop)
            putInt8(trigger.unknown1)
            putInt8(trigger.objective)
            putUInt32(trigger.objectiveOrder)
            putUInt32(trigger.unknown2)
            putStr32(trigger.text)
            putStr32(trigger.name)
            putInt32(len(trigger.effects))
            for e in range(len(trigger.effects)):
                effect = trigger.effects[e]
                putInt32(effect.type)
                if effect.check is None:
                    effect.check = 24
                putInt32(effect.check)
                putInt32(effect.aiGoal)
                putInt32(effect.amount)
                putInt32(effect.resource)
                putInt32(effect.state)
                putInt32(len(effect.unitIds)) # selected count
                putInt32(effect.unitId)
                # print(effect.unitName)
                putInt32(effect.unitName)
                putInt32(effect.sourcePlayer)
                putInt32(effect.targetPlayer)
                putInt32(effect.tech)
                putInt32(effect.stringId)
                putInt32(effect.unknown1)
                putInt32(effect.time)
                putInt32(-1 if effect.trigger_to_activate is None else effect.trigger_to_activate.id)
                putInt32(effect.x)
                putInt32(effect.y)
                putInt32(effect.x1)
                putInt32(effect.y1)
                putInt32(effect.x2)
                putInt32(effect.y2)
                putInt32(effect.unitGroup)
                putInt32(effect.unitType)
                putInt32(effect.instructionId)
                putInt32(effect.unknown2)
                putStr32(effect.text, "effect.text")
                putStr32(effect.filename, "effect.filename")
                for id in effect.unitIds:
                    putInt32(id)
            for i in range(len(trigger.effects)):
                putInt32(i)
            putInt32(len(trigger.conditions))
            logger.debug("number of conditions : {}".format(len(trigger.conditions)))
            for c in range(len(trigger.conditions)):
                logger.debug(c.__repr__())
                condition = trigger.conditions[c]
                # print(condition)
                putUInt32(condition.type)
                putInt32(condition.check)
                putInt32(condition.amount)
                putInt32(condition.resource, "condition.resource")
                putInt32(condition.unitObject)
                putInt32(condition.unitId)
                putInt32(condition.unitName)
                putInt32(condition.sourcePlayer)
                putInt32(condition.tech)
                putInt32(condition.timer)
                putInt32(condition.unknown1)
                putInt32(condition.x1)
                putInt32(condition.y1)
                putInt32(condition.x2)
                putInt32(condition.y2)
                putInt32(condition.unitGroup)
                putInt32(condition.unitType)
                putInt32(condition.aiSignal)
                putInt32(condition.reversed, "condition.reversed")
                putInt32(condition.unknown2)
            for i in range(len(trigger.conditions)):
                putInt32(i)
        for i in range(len(triggers)):
            putInt32(i)
        putUInt32(0)
        putUInt32(0)


# = open('')
if __name__ == "__main__":
    pass
