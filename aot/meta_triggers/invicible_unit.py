from aot import Trigger, DamageObject, BuffHP
from aot.meta_triggers.metatrigger import MetaTrigger


class InvicibleUnit(MetaTrigger):
    def __init__(self, unit_hp, unit, player):
        self.unit_hp = unit_hp
        self.unit = unit
        self.player = player

    def setup(self, scenario):
        t = Trigger("make unit {} invisible".format(self.unit.id), enable=True)
        t.then_(DamageObject(amount=self.unit_hp, unit=self.unit, player=self.player))
        t.then_(BuffHP(amount=-self.unit_hp, unit=self.unit, player=self.player))
        t.then_(BuffHP(amount=self.unit_hp, unit=self.unit, player=self.player))
        t.then_(DamageObject(amount=-self.unit_hp, unit=self.unit, player=self.player))
        scenario.add(t)
