from aot import MetaTrigger, UnitConstant, Trigger, ObjectInArea, EnumTile,  SendChat, PayGold, \
    Timer, RenameUnit
from aot.model.enums.unit import UnitType


class MercenaryPavilion(MetaTrigger):
    def __init__(self, x, y, mercenary_constant=UnitConstant.ROYAL_JANISSARY, create_the_unit=True,
                 players=range(1, 9), price=50):
        self.x = x
        self.y = y
        self.price = price
        self.mercenary_constant = mercenary_constant
        self.create_pavilion = create_the_unit
        self.players = players

    def setup(self, scenario):
        # # for i in range(0,14):
        if self.create_pavilion:
            scenario.units.new(owner=0, x=self.x, y=self.y, type=UnitConstant.PAVILION.value)
        unit = scenario.units.new(owner=0, x=self.x - 1, y=self.y + 0.5, type=self.mercenary_constant.value, angle=1)
        # unit = examples.units.new(owner=0, x=self.x - 4, y=self.y -2, type=self.mercenary_constant.value, angle=1)
        scenario.units.new(owner=0, x=self.x + 1.5, y=self.y + 0.5, type=UnitConstant.FLAG_B.value)
        if self.create_pavilion:
            scenario.units.new(owner=0, x=self.x, y=self.y, type=UnitConstant.PAVILION.value)
        for tile in scenario.map.tiles.getArea(self.x - 2, self.y - 2, self.x + 1, self.y + 1):
            if (tile.x, tile.y) not in [(self.x - 2, self.y - 2), (self.x + 1, self.y + 1), (self.x - 2, self.y + 1),
                                        (self.x + 1, self.y - 2)]:
                tile.type = EnumTile.ROCK.value
        for p in self.players:
            t = Trigger("{}({},{})(P{})".format(self.mercenary_constant.name, self.x, self.y, p), enable=True,
                        loop=True)
            t.if_(ObjectInArea(sourcePlayer=p, amount=1, x1=self.x + 1, y1=self.y, x2=self.x + 1, y2=self.y,
                               unit_type=UnitType.MILITARY.value))
            t.if_(Timer(5))
            t.then_(
                SendChat(player=p, text="Recruting {} for {} gold".format(self.mercenary_constant.name, self.price)))
            t.then_(PayGold(player=p, amount=self.price))
            scenario.add(t)

        t = Trigger("setup({},{})".format(self.x,self.y), enable=True)\
            .then_(RenameUnit("Recruit me for {} gold".format(self.price), unit))
        print(t)
        scenario.add(t)

