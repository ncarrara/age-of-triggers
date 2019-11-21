from aot.model.enums.condition import *


class Condition:
    """Initialize Condition

    Attributes:
        conditionType (int): type of condition
        check (int): is checked ? (always)
        resource (int): resource type
        amount (int): amount of resource
        unit_object (int): unit object
        unit_id (int): id of unit
        unit_cons (int): name of unit
        source_player (int): affected player
        tech (int): is tech discovered ?
        timer (int): how much time
        unknown1 (int): unknown1
        x1 (int): selected area start X position
        y1 (int): selected area start Y position
        x2 (int): selected area end X position
        y2 (int): selected area end Y position
        aiSinal (int): check signal from ai
    """

    def __init__(self, type=0,
                 amount=-1, resource=-1, unit_object=-1,
                 unit_id=-1, unit_cons=-1, source_player=-1,
                 tech=-1, timer=-1, x1=-1, y1=-1, x2=-1, y2=-1,
                 unit_group=-1, unit_type=-1, ai_signal=-1, reversed=0):
        self.type = type
        self.check = 21 # 18 for HD
        self.reversed = reversed
        self.unknown1= -1
        self.unknown2= -1
        self.unknown3= -1
        self.unknown4= -1
        self.unknown5= -1
        self.amount = amount
        self.resource = resource
        self.unit_object = unit_object
        self.unitId = unit_id
        self.unit_cons = unit_cons
        self.source_player = source_player
        self.tech = tech
        self.timer = timer
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.unit_group = unit_group
        self.unit_type = unit_type
        self.ai_signal = ai_signal

    def __repr__(self):
        name = "CONDITION:\n"
        info1 = "\tTYPE:{} - {}".format(self.type, eCondition[self.type])
        return name + info1

    def toJSON(self):
        """return JSON"""
        data = dict()
        data["type"] = self.type
        data["check"] = self.check
        data["reversed"] = self.reversed
        data["amount"] = self.amount
        data["resource"] = self.resource
        data["unitObject"] = self.unit_object
        data["unitId"] = self.unitId
        data["unitName"] = self.unit_cons
        data["sourcePlayer"] = self.sourcePlayer
        data["tech"] = self.tech
        data["timer"] = self.timer
        data["x1"] = self.x1
        data["y1"] = self.y1
        data["x2"] = self.x2
        data["y2"] = self.y2
        data["unitGroup"] = self.unit_group
        data["unitType"] = self.unit_type
        data["aiSignal"] = self.ai_signal
        return data


class Timer(Condition):
    def __init__(self, timer):
        super().__init__(type=10, timer=timer)


def Not(condition):
    condition.reversed = not (condition.reversed)
    return condition


class ObjectInArea(Condition):
    def __init__(self, source_player, amount=0, unit_object=-1,
                 unit_id=-1, unit_cons=-1,
                 x1=0, y1=0, x2=0, y2=0,
                 unit_group=-1, unit_type=-1):
        super().__init__(type=5, amount=amount, unit_object=unit_object,
                         unit_id=unit_id, unit_cons=unit_cons, source_player=source_player,
                         x1=x1, y1=y1, x2=x2, y2=y2,
                         unit_group=unit_group, unit_type=unit_type)


class UnitInArea(Condition):
    def __init__(self, player, unit, x1=0, y1=0, x2=0, y2=0):
        super().__init__(type=1, unit_object=unit.id, source_player=player, x1=x1, y1=y1, x2=x2, y2=y2)


class CaptureUnit(Condition):
    def __init__(self, unit=-1, player=-1):
        super().__init__(type=7, unit_object=unit.id, source_player=player)


class OwnObjectInArea(Condition):
    def __init__(self, amount=0, unit_object=-1,
                 unit_id=-1, unit_cons=-1, source_player=-1,
                 x1=0, y1=0, x2=0, y2=0,
                 unit_group=-1, unit_type=-1):
        super().__init__(type=3, amount=amount, unit_object=unit_object,
                         unit_id=unit_id, unit_cons=unit_cons, source_player=source_player,
                         x1=x1, y1=y1, x2=x2, y2=y2,
                         unit_group=unit_group, unit_type=unit_type)
