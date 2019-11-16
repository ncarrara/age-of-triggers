from aot.model.enums.condition import *


class Condition:
    """Initialize Condition

    Attributes:
        conditionType (int): type of condition
        check (int): is checked ? (always)
        resource (int): resource type
        amount (int): amount of resource
        unitObject (int): unit object
        unitId (int): id of unit
        unit_cons (int): name of unit
        sourcePlayer (int): affected player
        tech (int): is tech discovered ?
        timer (int): how much time
        unknown1 (int): unknown1
        x1 (int): selected area start X position
        y1 (int): selected area start Y position
        x2 (int): selected area end X position
        y2 (int): selected area end Y position
        aiSinal (int): check signal from ai
    """

    def __init__(self, type=0, check=18,
                 amount=-1, resource=-1, unitObject=-1,
                 unitId=-1, unit_cons=-1, sourcePlayer=-1,
                 tech=-1, timer=-1, unknown1=-1,
                 x1=-1, y1=-1, x2=-1, y2=-1,
                 unitGroup=-1, unit_what=-1, aiSignal=-1, reversed=0, unknown2=-1):
        self.type = type  # condition type
        self.check = check
        self.reversed = reversed
        self.unknown2 = unknown2
        self.amount = amount
        self.resource = resource
        self.unitObject = unitObject
        self.unitId = unitId
        self.unitName = unit_cons
        self.sourcePlayer = sourcePlayer
        self.tech = tech
        self.timer = timer
        self.unknown1 = unknown1
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.unitGroup = unitGroup
        self.unitType = unit_what
        self.aiSignal = aiSignal

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
        data["unitObject"] = self.unitObject
        data["unitId"] = self.unitId
        data["unitName"] = self.unitName
        data["sourcePlayer"] = self.sourcePlayer
        data["tech"] = self.tech
        data["timer"] = self.timer
        data["x1"] = self.x1
        data["y1"] = self.y1
        data["x2"] = self.x2
        data["y2"] = self.y2
        data["unitGroup"] = self.unitGroup
        data["unitType"] = self.unitType
        data["aiSignal"] = self.aiSignal
        return data


class Timer(Condition):
    def __init__(self, timer):
        super().__init__(type=10, timer=timer)


def Not(condition):
    condition.reversed = not (condition.reversed)
    return condition


class ObjectInArea(Condition):
    def __init__(self, sourcePlayer, amount=0, unitObject=-1,
                 unitId=-1, unit_cons=-1,
                 x1=0, y1=0, x2=0, y2=0,
                 unitGroup=-1, unit_type=-1):
        super().__init__(type=5, amount=amount, unitObject=unitObject,
                         unitId=unitId, unit_cons=unit_cons, sourcePlayer=sourcePlayer,
                         x1=x1, y1=y1, x2=x2, y2=y2,
                         unitGroup=unitGroup, unit_what=unit_type)


class UnitInArea(Condition):
    def __init__(self, player, unit, x1=0, y1=0, x2=0, y2=0):
        super().__init__(type=1, unitObject=unit.id, sourcePlayer=player, x1=x1, y1=y1, x2=x2, y2=y2)

class CaptureUnit(Condition):
    def __init__(self, unit=-1, player=-1 ):
        super().__init__(type=7,unitObject=unit.id,sourcePlayer=player)


class OwnObjectInArea(Condition):
    def __init__(self, amount=0, unitObject=-1,
                 unitId=-1, unit_cons=-1, sourcePlayer=-1,
                 x1=0, y1=0, x2=0, y2=0,
                 unitGroup=-1, unit_type=-1):
        super().__init__(type=3, amount=amount, unitObject=unitObject,
                         unitId=unitId, unit_cons=unit_cons, sourcePlayer=sourcePlayer,
                         x1=x1, y1=y1, x2=x2, y2=y2,
                         unitGroup=unitGroup, unit_what=unit_type)
