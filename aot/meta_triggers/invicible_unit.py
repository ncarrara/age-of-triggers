from aot.meta_triggers.metatrigger import MetaTrigger
from aot.model.effect import DamageObject, BuffHP, DamageObjectByUnitConstant, BuffHPByUnitConstant
from aot.model.trigger import Trigger


class InvicibleUnit(MetaTrigger):
    def __init__(self, unit_hp, player, unit =None,unit_cons=None):
        self.unit_hp = unit_hp
        self.unit = unit
        self.player = player
        self.unit_cons=unit_cons
        if self.unit_cons is None:
            self.t = Trigger("make unit {} invisible".format(self.unit.id), enable=True)
            self.t.then_(DamageObject(amount=self.unit_hp, unit=self.unit, player=self.player))
            self.t.then_(BuffHP(amount=-self.unit_hp, unit=self.unit, player=self.player))
            self.t.then_(BuffHP(amount=self.unit_hp, unit=self.unit, player=self.player))
            self.t.then_(DamageObject(amount=-self.unit_hp, unit=self.unit, player=self.player))
        else:
            self.t = Trigger("make unit {} invisible".format(self.unit_cons), enable=True)
            self.t.then_(DamageObjectByUnitConstant(amount=self.unit_hp, unit_cons=self.unit_cons, player=self.player))
            self.t.then_(BuffHPByUnitConstant(amount=-self.unit_hp, unit_cons=self.unit_cons, player=self.player))
            self.t.then_(BuffHPByUnitConstant(amount=self.unit_hp, unit_cons=self.unit_cons, player=self.player))
            self.t.then_(DamageObjectByUnitConstant(amount=-self.unit_hp, unit_cons=self.unit_cons, player=self.player))


    def setup(self, scenario):
        scenario.add(self.t)

    def triggers_to_activate(self):
        return [self.t]
