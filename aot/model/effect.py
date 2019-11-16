from aot.model.enums.color import Color
from aot.model.enums.effect import *
from aot.model.enums import EnumResource


class Effect:
    """Trigger Effect

    Attributes:
        effectType (int): type of effect
        check (int): is checked ?
        aiGoal (int): ai goal
        state (int): diplomacy state
        resource (int): player resource like food, wood, gold, stone,
            kills, death, score
        amount (int): amount of resource
        selectedCount (int): number of selected units
        unitId (int): id of selected unit
        unit_cons (int): unit new name
        sourcePlayer (int): source player
        targetPlayer (int): target player
        tech (int): technology id to research
        stringId (int): id of string
        unknown1 (int): unknown1
        time (int): display time
        triggerId (int): id of trigger to enable/disable
        x (int): x position
        y (int): y position
        x1 (int): affected area start X position
        y1 (int): affected area start Y position
        x2 (int): affected area end X position
        y2 (int): affected area end Y position
        unitGroup (int): unit group type to affect
        unitType (int): unit type to affect
        instructionId (str): instruction panel
        unknown2=None if not examples.is_aoe2scenario else getInt32(),
        text (str): instruction text
        filename (str): filename (used for sounds)
        unitIds (list(int)): list with selected units
    """

    def __init__(self, type=0, check=None,
                 aiGoal=-1, amount=-1, resource=-1, state=-1,
                 selectedCount=-1, unitId=-1, unit_cons=-1,
                 sourcePlayer=-1, targetPlayer=-1, tech=-1,
                 stringId=-1, unknown1=-1, time=-1, trigger_to_activate=None,
                 x=-1, y=-1, x1=-1, y1=-1, x2=-1, y2=-1,
                 unitGroup=-1, unitType=-1,
                 instructionId=-1, unknown2=-1,
                 # unknown2=-1,
                 text="", filename="", unitIds=None):
        if unitIds is None:
            unitIds = []
        self.type = type  # effect type
        self.check = None  # check
        self.aiGoal = aiGoal
        self.amount = amount
        self.resource = resource
        self.state = state  # state of trigger
        self.selectedCount = selectedCount
        self.unitId = unitId
        self.unitName = unit_cons
        self.sourcePlayer = sourcePlayer
        self.targetPlayer = targetPlayer
        self.tech = tech
        self.stringId = stringId
        self.unknown1 = unknown1
        self.unknown2 = unknown2
        # self.unknown2 = unknown2
        self.time = time
        self.trigger_to_activate = trigger_to_activate
        self.x, self.y = x, y
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.unitGroup = unitGroup
        self.unitType = unitType
        self.instructionId = instructionId
        self.text = text
        self.filename = filename
        self.unitIds = unitIds

    def __repr__(self):
        name = "EFFECT:\n"
        info1 = "\tTYPE:{} - {}\nunitId:{}\nunitIds:{}\n".format(self.type, eEffect[self.type], self.unitId,
                                                                 self.unitIds)
        return name + info1

    def toJSON(self):
        """return JSON"""
        data = dict()
        data["type"] = self.type
        data["check"] = self.check
        data["aiGoal"] = self.aiGoal
        data["amount"] = self.amount
        data["resource"] = self.resource
        data["state"] = self.state
        data["selectedCount"] = self.selectedCount
        data["unitId"] = self.unitId
        data["unitName"] = self.unitName
        data["sourcePlayer"] = self.sourcePlayer
        data["targetPlayer"] = self.targetPlayer
        data["tech"] = self.tech
        data["stringId"] = self.stringId
        data["unknown1"] = self.unknown1
        # data["unknown2"] = self.unknown2

        data["time"] = self.time
        data["trigger_to_activate"] = self.trigger_to_activate
        data["x"] = self.x
        data["y"] = self.y
        data["x1"] = self.x1
        data["y1"] = self.y1
        data["x2"] = self.x2
        data["y2"] = self.y2
        data["unitGroup"] = self.unitGroup
        data["unitType"] = self.unitType
        data["instructionId"] = self.instructionId
        data["text"] = self.text
        data["filename"] = self.filename
        data["unitIds"] = self.unitIds
        return data


class ChangeObjectAttack(Effect):
    def __init__(self, player, amount,
                 unit_type=-1,
                 x1=-1, x2=-1, y1=-1, y2=-1):
        super().__init__(type=28,
                         x1=x1,
                         x2=x2,
                         y1=y1,
                         y2=y2,
                         sourcePlayer=player,
                         amount=amount, unitType=unit_type)


class RemoveObject(Effect):
    def __init__(self, player, unit_cons, x1, x2, y1, y2):
        super().__init__(type=15,
                         x1=x1,
                         x2=x2,
                         y1=y1,
                         y2=y2,
                         sourcePlayer=player,
                         unit_cons=unit_cons)

class RemoveObjectByType(Effect):
    def __init__(self, player, type, x1, x2, y1, y2):
        super().__init__(type=15,
                         x1=x1,
                         x2=x2,
                         y1=y1,
                         y2=y2,
                         sourcePlayer=player,
                         unitType=type)

class RenameUnit(Effect):
    def __init__(self, name, unit):
        super().__init__(type=26, unitIds=[unit.id], text=name, sourcePlayer=unit.owner)


class KillUnitsByConstantInArea(Effect):
    def __init__(self, player, unit_cons, x1, x2, y1, y2):
        super().__init__(type=14,
                         x1=x1,
                         x2=x2,
                         y1=y1,
                         y2=y2,
                         sourcePlayer=player,
                         unit_cons=unit_cons)


class Tribute(Effect):
    def __init__(self, player, amount, resource, silent=True, receive=True):

        if receive:
            if silent:
                super().__init__(type=5, sourcePlayer=player, targetPlayer=0, amount=-amount, resource=resource)
            else:
                super().__init__(type=5, sourcePlayer=0, targetPlayer=player, amount=amount, resource=resource)
        else:
            if silent:
                super().__init__(type=5, sourcePlayer=player, targetPlayer=0, amount=amount, resource=resource)
            else:
                super().__init__(type=5, sourcePlayer=0, targetPlayer=player, amount=-amount, resource=resource)


class GiveExtraPop(Effect):
    def __init__(self, player, amount):
        super().__init__(type=5, sourcePlayer=player, targetPlayer=0, amount=-amount,
                         resource=EnumResource.BONUS_POPULATION.value)


class GiveHeadroom(Effect):
    def __init__(self, player, amount):
        super().__init__(type=5, sourcePlayer=player, targetPlayer=0, amount=-amount,
                         resource=EnumResource.POPULATION_HEADROOM.value)


class MoveCamera(Effect):
    def __init__(self,player,x,y):
        super().__init__(type=16,sourcePlayer=player,x=x,y=y)

class PayGold(Tribute):
    def __init__(self, player, amount, silent=True):
        super().__init__(player=player, amount=amount, resource=EnumResource.GOLD.value, silent=silent, receive=False)
class PayFood(Tribute):
    def __init__(self, player, amount, silent=True):
        super().__init__(player=player, amount=amount, resource=EnumResource.FOOD.value, silent=silent, receive=False)
class PayStone(Tribute):
    def __init__(self, player, amount, silent=True):
        super().__init__(player=player, amount=amount, resource=EnumResource.STONE.value, silent=silent, receive=False)
class PayWood(Tribute):
    def __init__(self, player, amount, silent=True):
        super().__init__(player=player, amount=amount, resource=EnumResource.WOOD.value, silent=silent, receive=False)


class GiveWood(Tribute):
    def __init__(self, player, amount, silent=True):
        super().__init__(player=player, amount=amount, resource=EnumResource.WOOD.value, silent=silent, receive=True)


class GiveFood(Tribute):
    def __init__(self, player, amount, silent=True):
        super().__init__(player=player, amount=amount, resource=EnumResource.FOOD.value, silent=silent, receive=True)


class GiveGold(Tribute):
    def __init__(self, player, amount, silent=True):
        super().__init__(player=player, amount=amount, resource=EnumResource.GOLD.value, silent=silent,
                         receive=True)


class GiveStone(Tribute):
    def __init__(self, player, amount, silent=True):
        super().__init__(player=player, amount=amount, resource=EnumResource.STONE.value, silent=silent, receive=True)


class ActivateTrigger(Effect):
    def __init__(self, trigger_to_activate):
        super().__init__(type=8, trigger_to_activate=trigger_to_activate)


class MoveObjectToPoint(Effect):
    def __init__(self, player, unit, x, y):
        super().__init__(type=12, sourcePlayer=player, unitIds=[unit.id], x=x, y=y)


class DamageObject(Effect):
    def __init__(self,player,amount,  unit):
        super().__init__(sourcePlayer=player,type=24,amount=amount,  unitIds=[unit.id])
class BuffHP(Effect):
    def __init__(self,player,amount,  unit):
        super().__init__(sourcePlayer=player,type=27,amount=amount,  unitIds=[unit.id])



class DesactivateTrigger(Effect):
    def __init__(self, trigger_to_desactivate):
        super().__init__(type=9, trigger_to_activate=trigger_to_desactivate)


class SendChat(Effect):

    def __init__(self, player=0, stringId=-1, text="", filename="", color=Color.WHITE):
        super().__init__(type=3, sourcePlayer=player, stringId=stringId, text=str(color) + text,
                         filename=filename)


class SendInstruction(Effect):

    def __init__(self, stringId=-1, text="", filename="", color=Color.WHITE, time=5):
        super().__init__(type=20, time=time, stringId=stringId, text=str(color) + text,
                         filename=filename)


class CreateObject(Effect):
    def __init__(self, x, y, unit_cons, player):
        super().__init__(type=11, sourcePlayer=player, x=x, y=y, unit_cons=unit_cons)


class ChangeOwnership(Effect):
    def __init__(self, targetPlayer=0, unit_cons=-1,
                 unitId=-1, sourcePlayer=-1,
                 x1=0, y1=0, x2=0, y2=0,
                 unitGroup=-1, unitType=-1):
        super().__init__(type=18, targetPlayer=targetPlayer,
                         unitId=unitId, unit_cons=unit_cons, sourcePlayer=sourcePlayer,
                         x1=x1, y1=y1, x2=x2, y2=y2, unitGroup=unitGroup, unitType=unitType)


class ChangeUnitOwnership(Effect):
    def __init__(self, targetPlayer,sourcePlayer,unit):
        super().__init__(type=18, targetPlayer=targetPlayer,
                         sourcePlayer=sourcePlayer,unitIds=[unit.id])
