from aot import *
from aot.model.enums.resource import EnumResource


class Treasure(MetaTrigger):
    def __init__(self, x, y, unit, amount, resource, players=range(1, 9), create_the_unit=False,
                 trigger_name="treasure"):
        self.players = players
        self.trigger_name = trigger_name
        self.x = x
        self.amount = amount
        self.resource = resource
        self.unit = unit
        self.y = y
        self.create_the_unit = create_the_unit

    def setup(self, scenario):
        if self.create_the_unit:
            scenario.units.new(owner=0, x=self.x, y=self.y, type=self.unit)

        for p in self.players:
            t = Trigger(self.trigger_name+" (P{})".format(p), enable=True)
            t.if_(ObjectInArea(amount=1,
                               unit_cons=self.unit,
                               sourcePlayer=0,
                               x1=max(0, self.x - 1), y1=max(0, self.y - 1),
                               x2=min(scenario.map.width, self.x + 1),
                               y2=min(scenario.map.height, self.y + 1)))\
                .if_(ObjectInArea(amount=1,
                               sourcePlayer=p,
                               x1=max(0, self.x - 1), y1=max(0, self.y - 1),
                               x2=min(scenario.map.width, self.x + 1),
                               y2=min(scenario.map.height, self.y + 1))) \
                .then_(Tribute(p, self.amount, self.resource, silent=False)) \
                .then_(SendChat(player=p, text="You found a treasure !")) \
                .then_(RemoveObject(player=PlayerEnum.GAIA.value,
                                    unit_cons=self.unit, x1=self.x, x2=self.x, y1=self.y, y2=self.y))

            scenario.triggers.add(t)


class TreasureLoot(Treasure):
    def __init__(self, x, y, amount, players=range(1, 9), create_the_unit=True):
        super().__init__(x=x, y=y, unit=UnitConstant.LOOT.value,
                         amount=amount,
                         create_the_unit=create_the_unit,
                         players=players, resource=EnumResource.GOLD.value,
                         trigger_name="TreasureLoot({},{})".format(x,y))


class TreasureLumber(Treasure):
    def __init__(self, x, y, amount, players=range(1, 9), create_the_unit=True):
        super().__init__(x=x, y=y, unit=UnitConstant.LUMBER.value,
                         create_the_unit=create_the_unit,
                         amount=amount,
                         players=players, resource=EnumResource.WOOD.value,
                         trigger_name="TreasureLumber({},{})".format(x,y))


class TreasureQuarry(Treasure):
    def __init__(self, x, y, amount, players=range(1, 9), create_the_unit=True, ):
        super().__init__(x=x, y=y, unit=UnitConstant.QUARRY.value,
                         create_the_unit=create_the_unit,
                         amount=amount,
                         players=players, resource=EnumResource.STONE.value,
                         trigger_name="TreasureQuarry({},{})".format(x,y))
