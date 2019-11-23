from abc import ABC
from aot.model.enums.color import Color
from aot.model.enums.resource import EnumResource


class Effect(ABC):

    def __init__(self, type=0, ai_goal=-1, amount=-1, resource=-1, state=-1,
                 selected_count=-1, unit_id=-1, unit_cons=-1,
                 source_player=-1, target_player=-1, tech=-1, facet=-1,
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
        self.source_player = source_player
        self.target_player = target_player
        self.tech = tech
        self.string_table_id = stringId
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


class ChangeObjectAttackByType(Effect):
    def __init__(self, player, amount, unit_type, x1=-1, x2=-1, y1=-1, y2=-1):
        super().__init__(type=28, x1=x1, x2=x2, y1=y1, y2=y2, source_player=player, amount=amount, unit_type=unit_type)


class RemoveObject(Effect):
    def __init__(self, player, unit_cons, unit_type, unit_group, unit_id, x1=-1, x2=-1, y1=-1, y2=-1):
        super().__init__(type=15, x1=x1, x2=x2, y1=y1, y2=y2, source_player=player,
                         unit_cons=unit_cons, unit_type=unit_type, unit_group=unit_group, unit_id=unit_id)


class RemoveObjectByConstant(RemoveObject):
    def __init__(self, player, unit_cons, x1=-1, x2=-1, y1=-1, y2=-1):
        super().__init__(x1=x1, x2=x2, y1=y1, y2=y2, player=player, unit_cons=unit_cons, unit_type=-1, unit_group=-1,unit_id=-1)


class RemoveObjectByType(RemoveObject):
    def __init__(self, player, unit_type, x1=-1, x2=-1, y1=-1, y2=-1):
        super().__init__(x1=x1, x2=x2, y1=y1, y2=y2, player=player, unit_type=unit_type, unit_cons=-1, unit_group=-1,unit_id=-1)


class RemoveObjectByGroup(RemoveObject):
    def __init__(self, player, unit_group, x1=-1, x2=-1, y1=-1, y2=-1):
        super().__init__(x1=x1, x2=x2, y1=y1, y2=y2, player=player, unit_group=unit_group, unit_type=-1, unit_cons=-1,unit_id=-1)


class RenameByUnit(Effect):
    def __init__(self, name, unit):
        super().__init__(type=26, unit_ids=[unit.id], text=name, source_player=unit.owner)


class KillUnitsByConstant(Effect):
    def __init__(self, player, unit_cons, x1=-1, x2=-1, y1=-1, y2=-1):
        super().__init__(type=14, x1=x1, x2=x2, y1=y1, y2=y2, source_player=player, unit_cons=unit_cons)


class Tribute(Effect):
    def __init__(self, player, amount, resource, silent=True, receive=True):
        if receive:
            if silent:
                super().__init__(type=5, source_player=player, target_player=0, amount=-amount, resource=resource)
            else:
                super().__init__(type=5, source_player=0, target_player=player, amount=amount, resource=resource)
        else:
            if silent:
                super().__init__(type=5, source_player=player, target_player=0, amount=amount, resource=resource)
            else:
                super().__init__(type=5, source_player=0, target_player=player, amount=-amount, resource=resource)


class GiveExtraPop(Effect):
    def __init__(self, player, amount):
        super().__init__(type=5, source_player=player, target_player=0, amount=-amount,
                         resource=EnumResource.BONUS_POPULATION.value)


class GiveHeadroom(Effect):
    def __init__(self, player, amount):
        super().__init__(type=5, source_player=player, target_player=0, amount=-amount,
                         resource=EnumResource.POPULATION_HEADROOM.value)


class MoveCamera(Effect):
    def __init__(self, player, x, y):
        super().__init__(type=16, source_player=player, x=x, y=y)


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
        self._triggers = meta_trigger.triggers_to_deactivate()
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
        super().__init__(type=12, source_player=player, unit_ids=[unit.id], x=x, y=y)


class DamageObject(Effect):
    def __init__(self, player, amount, unit):
        super().__init__(source_player=player, type=24, amount=amount, unit_ids=[unit.id])


class DamageObjectByConstant(Effect):
    def __init__(self, player, amount, unit_cons):
        super().__init__(source_player=player, type=24, amount=amount, unit_cons=unit_cons)


class BuffHPByConstant(Effect):
    def __init__(self, player, amount, unit_cons):
        super().__init__(source_player=player, type=27, amount=amount, unit_cons=unit_cons)


class BuffHPByUnit(Effect):
    def __init__(self, player, amount, unit):
        super().__init__(source_player=player, type=27, amount=amount, unit_ids=[unit.id])


class DesactivateTrigger(Effect):
    def __init__(self, trigger_to_desactivate):
        super().__init__(type=9, trigger_to_activate=trigger_to_desactivate)


class SendChat(Effect):

    def __init__(self, player=0, stringId=-1, message="", filename="", color=Color.WHITE):
        super().__init__(type=3, source_player=player, stringId=stringId, message=str(color) + message,
                         filename=filename)


class SendInstruction(Effect):

    def __init__(self, message, stringId=-1, filename="", color=Color.WHITE, time=10,panel_location=0,player=0):
        super().__init__(type=20, time=time, stringId=stringId, message=str(color) + message,
                         filename=filename, source_player=player,panel_location=panel_location)  # default source player when adding this effect in editor


class CreateObject(Effect):
    def __init__(self, x, y, unit_cons, player):
        super().__init__(type=11, source_player=player, x=x, y=y, unit_cons=unit_cons)


class ChangeDiplomacy(Effect):
    def __init__(self,source_player,target_player,diplomacy):
        super().__init__(type=1,source_player=source_player,target_player=target_player,state=diplomacy)

class ChangeOwnership(Effect):
    def __init__(self, target_player=0, unit_cons=-1, unit_group=-1, unit_type=-1,
                 unit_ids=None, source_player=-1, x1=-1, y1=-1, x2=-1, y2=-1):
        if unit_ids is None:
            unit_ids = []
        super().__init__(type=18, target_player=target_player,
                         unit_ids=unit_ids, unit_cons=unit_cons, source_player=source_player,
                         x1=x1, y1=y1, x2=x2, y2=y2, unit_group=unit_group, unit_type=unit_type)


class ChangeOwnershipByUnit(ChangeOwnership):
    def __init__(self, target_player, source_player, unit):
        super().__init__(target_player=target_player, source_player=source_player, unit_ids=[unit.id])
