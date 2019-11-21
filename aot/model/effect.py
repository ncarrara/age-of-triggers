from aot.model.enums.color import Color
from aot.model.enums.effect import *
from aot.model.enums.resource import EnumResource


class Effect:
    """Trigger Effect

    Attributes:
        effectType (int): type of effect
        check (int): is checked ?
        ai_goal (int): ai goal
        state (int): diplomacy state
        resource (int): player resource like food, wood, gold, stone,
            kills, death, score
        amount (int): amount of resource
        selected_count (int): number of selected units
        unit_id (int): id of selected unit
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
        unit_group (int): unit group type to affect
        unit_type (int): unit type to affect
        panel_location (str): instruction panel
        unknown2=None if not examples.is_aoe2scenario else getInt32(),
        text (str): instruction text
        filename (str): filename (used for sounds)
        unit_ids (list(int)): list with selected units
    """

    def __init__(self, type=0, ai_goal=-1, amount=-1, resource=-1, state=-1,
                 selected_count=-1, unit_id=-1, unit_cons=-1,
                 sourcePlayer=-1, targetPlayer=-1, tech=-1, facet=-1,
                 stringId=-1, time=-1, trigger_to_activate=None,
                 x=-1, y=-1, x1=-1, y1=-1, x2=-1, y2=-1,
                 unit_group=-1, unit_type=-1,
                 panel_location=0, text="", filename="", message="", unit_ids=None, sound_event_name=""):
        if unit_ids is None:
            unit_ids = []
        self.facet = facet
        self.panel_location = 0
        self.sound_event_name = sound_event_name
        self.unknown1 = -1
        # self.unknown2 = -1
        self.unknown3 = bytes([255] * 80)
        self.unknown4 = -1
        self.unknown5 = 0
        self.message = message
        self.type = type  # effect type
        self.check = 46  # check
        self.ai_goal = ai_goal
        self.amount = amount
        self.resource = resource
        self.state = state  # state of trigger
        self.selected_count = selected_count
        self.unit_id = unit_id
        self.unit_cons = unit_cons
        self.source_player = sourcePlayer
        self.target_player = targetPlayer
        self.tech = tech
        self.string_table_id = stringId
        # self.unknown2 = unknown2
        self.time = time
        self.trigger_to_activate = trigger_to_activate
        self.x, self.y = x, y
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.unit_group = unit_group
        self.unit_type = unit_type
        self.panel_location = panel_location
        self.text = text
        self.filename = filename
        self.unit_ids = unit_ids

    def __repr__(self):
        name = "EFFECT:\n"
        info1 = "\tTYPE:{} - {}\nunitId:{}\nunitIds:{}\n".format(self.type, eEffect[self.type], self.unit_id,
                                                                 self.unit_ids)
        return name + info1

    def toJSON(self):
        """return JSON"""
        data = dict()
        data["type"] = self.type
        data["check"] = self.check
        data["aiGoal"] = self.ai_goal
        data["amount"] = self.amount
        data["resource"] = self.resource
        data["state"] = self.state
        data["selectedCount"] = self.selected_count
        data["unitId"] = self.unit_id
        data["unitName"] = self.unit_cons
        data["sourcePlayer"] = self.source_player
        data["targetPlayer"] = self.target_player
        data["tech"] = self.tech
        data["stringId"] = self.string_table_id
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
        data["unitGroup"] = self.unit_group
        data["unitType"] = self.unit_type
        data["instructionId"] = self.panel_location
        data["text"] = self.text
        data["filename"] = self.filename
        data["unitIds"] = self.unit_ids
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
                         amount=amount, unit_type=unit_type)


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
                         unit_type=type)


class RenameUnit(Effect):
    def __init__(self, name, unit):
        super().__init__(type=26, unit_ids=[unit.id], text=name, sourcePlayer=unit.owner)


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
    def __init__(self, player, x, y):
        super().__init__(type=16, sourcePlayer=player, x=x, y=y)


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


class ActivateMetaTrigger:
    def __init__(self, meta_trigger):
        self._triggers = meta_trigger.triggers_to_activate()
        self._i = -1

    def __iter__(self):
        return self

    def __next__(self):
        self._i += 1
        if self._i < len(self._triggers):
            return ActivateTrigger(self._triggers[self._i])
        raise StopIteration


class DesactivateMetaTrigger:
    def __init__(self, meta_trigger):
        self._triggers = meta_trigger.triggers_to_activate()
        self._i = -1

    def __iter__(self):
        return self

    def __next__(self):
        self._i += 1
        if self._i < len(self._triggers):
            return DesactivateTrigger(self._triggers[self._i])
        raise StopIteration


class MoveObjectToPoint(Effect):
    def __init__(self, player, unit, x, y):
        super().__init__(type=12, sourcePlayer=player, unit_ids=[unit.id], x=x, y=y)


class DamageObject(Effect):
    def __init__(self, player, amount, unit):
        super().__init__(sourcePlayer=player, type=24, amount=amount, unit_ids=[unit.id])

class DamageObjectByUnitConstant(Effect):
    def __init__(self, player, amount, unit_cons):
        super().__init__(sourcePlayer=player, type=24, amount=amount, unit_cons=unit_cons)

class BuffHPByUnitConstant(Effect):
    def __init__(self, player, amount, unit_cons):
        super().__init__(sourcePlayer=player, type=27, amount=amount, unit_cons=unit_cons)

class BuffHP(Effect):
    def __init__(self, player, amount, unit):
        super().__init__(sourcePlayer=player, type=27, amount=amount, unit_ids=[unit.id])


class DesactivateTrigger(Effect):
    def __init__(self, trigger_to_desactivate):
        super().__init__(type=9, trigger_to_activate=trigger_to_desactivate)


class SendChat(Effect):

    def __init__(self, player=0, stringId=-1, message="", filename="", color=Color.WHITE):
        super().__init__(type=3, sourcePlayer=player, stringId=stringId, message=str(color) + message,
                         filename=filename)


class SendInstruction(Effect):

    def __init__(self, message, stringId=-1, filename="", color=Color.WHITE, time=10):
        super().__init__(type=20, time=time, stringId=stringId, message=str(color) + message,
                         filename=filename,sourcePlayer=1) # default source player when adding this effect in editor


class CreateObject(Effect):
    def __init__(self, x, y, unit_cons, player):
        super().__init__(type=11, sourcePlayer=player, x=x, y=y, unit_cons=unit_cons)


class ChangeOwnership(Effect):
    def __init__(self, targetPlayer=0, unit_cons=-1,
                 unit_id=-1, sourcePlayer=-1,
                 x1=0, y1=0, x2=0, y2=0,
                 unit_group=-1, unit_type=-1):
        super().__init__(type=18, targetPlayer=targetPlayer,
                         unit_id=unit_id, unit_cons=unit_cons, sourcePlayer=sourcePlayer,
                         x1=x1, y1=y1, x2=x2, y2=y2, unit_group=unit_group, unit_type=unit_type)


class ChangeUnitOwnership(Effect):
    def __init__(self, targetPlayer, sourcePlayer, unit):
        super().__init__(type=18, targetPlayer=targetPlayer,
                         sourcePlayer=sourcePlayer, unit_ids=[unit.id])
