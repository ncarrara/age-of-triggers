from abc import ABC


class Condition(ABC):

    def __init__(self, type=0,
                 amount=-1, resource=-1, unit_object=-1,
                 unit_id=-1, unit_cons=-1, source_player=-1,
                 tech=-1, timer=-1, x1=-1, y1=-1, x2=-1, y2=-1,
                 unit_group=-1, unit_type=-1, ai_signal=-1, reversed=0):
        self.type = type
        self.check = 21  # 18 for HD
        self.reversed = reversed
        self.unknown1 = -1
        self.unknown2 = -1
        self.unknown3 = -1
        self.unknown4 = -1
        self.unknown5 = -1
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


class Timer(Condition):
    def __init__(self, timer):
        super().__init__(type=10, timer=timer)


def Not(condition):
    condition.reversed = not (condition.reversed)
    return condition


class ObjectInArea(Condition):
    def __init__(self, source_player, x1, y1, x2, y2, amount=0, unit_object=-1,
                 unit_id=-1, unit_cons=-1, unit_group=-1, unit_type=-1):
        super().__init__(type=5, amount=amount, unit_object=unit_object,
                         unit_id=unit_id, unit_cons=unit_cons, source_player=source_player,
                         x1=x1, y1=y1, x2=x2, y2=y2,
                         unit_group=unit_group, unit_type=unit_type)


class UnitInArea(Condition):
    def __init__(self, player, unit, x1, y1, x2, y2):
        super().__init__(type=1, unit_object=unit.id, source_player=player, x1=x1, y1=y1, x2=x2, y2=y2)


class CaptureUnit(Condition):
    def __init__(self, unit, player):
        super().__init__(type=7, unit_object=unit.id, source_player=player)


class OwnObjectInArea(Condition):
    def __init__(self, player, x1, y1, x2, y2, amount=0, unit_object=-1,
                 unit_id=-1, unit_cons=-1, unit_group=-1, unit_type=-1):
        super().__init__(type=3, amount=amount, unit_object=unit_object,
                         unit_id=unit_id, unit_cons=unit_cons, source_player=player,
                         x1=x1, y1=y1, x2=x2, y2=y2,
                         unit_group=unit_group, unit_type=unit_type)
