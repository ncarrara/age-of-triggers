from aot import SendChat, UnitConstant, ObjectInArea, ChangeOwnership, Trigger, ActivateTrigger, Not, EnumTile, \
    DesactivateTrigger, Timer, ChangeObjectAttack
from aot.meta_triggers.capture import Capture


class TrainingCamp(Capture):
    def __init__(self, scn,
                 x, y,
                 radius,
                 bonus_attack_per_min=1,
                 loop_convert=False,
                 use_flags=True,
                 frontier_tile=EnumTile.ROCK.value,
                 create_the_unit=True):
        self.add_army_tent = create_the_unit
        self.bonus_attack_per_min = bonus_attack_per_min
        self.boosting_triggers = [Trigger("boosting ({},{}) P{}".format(x, y, p), loop=True) for p in range(1, 9)]
        self.radius = radius
        self.use_flags = use_flags
        self.frontier_tile = frontier_tile
        self.x = x
        self.loop_convert = loop_convert
        self.y = y

        self.x1 = max(0, self.x - self.radius)
        self.y1 = max(0, self.y - self.radius)
        self.x2 = min(scn.get_width() - 1, self.x + self.radius)
        self.y2 = min(scn.get_height() - 1, self.y + self.radius)
        conditions = []
        condition = lambda p: ObjectInArea(amount=1, sourcePlayer=p,
                                           x1=self.x1, y1=self.y1, x2=self.x2 - 1, y2=self.y2 - 1,
                                           unit_type=UnitType.MILITARY.value)
        loss_condition = lambda p: Not(ObjectInArea(amount=1, sourcePlayer=p,
                                                    x1=self.x1, y1=self.y1, x2=self.x2 - 1, y2=self.y2 - 1,
                                                    unit_type=UnitType.MILITARY.value))
        conditions.append(condition)
        for pp in range(1, 9):
            condition = lambda p, other_player=pp: Not(
                ObjectInArea(amount=1, sourcePlayer=(other_player if other_player != p else 0),
                             x1=self.x1, y1=self.y1, x2=self.x2 - 1,
                             y2=self.y2 - 1,
                             unit_type=UnitType.MILITARY.value))
            conditions.append(condition)

        then_effects = []
        then_ = lambda p: SendChat(player=p, text="You captured the training camp")
        then_effects.append(then_)
        then_effects.append(lambda p, trigs=self.boosting_triggers: ActivateTrigger(trigs[p - 1]))
        else_effects = []
        else_ = lambda p: SendChat(player=p, text="You've lost the training camp")
        else_effects.append(else_)
        else_effects.append(lambda p, trigs=self.boosting_triggers: DesactivateTrigger(trigs[p - 1]))

        if self.use_flags:
            else_effects.append(lambda p: ChangeOwnership(sourcePlayer=p, targetPlayer=0,
                                                          x1=self.x1, y1=self.y1, x2=self.x2, y2=self.y2,
                                                          unit_cons=UnitConstant.FLAG_A.value))
            then_effects.append(lambda p: ChangeOwnership(sourcePlayer=0, targetPlayer=p,
                                                          x1=self.x1, y1=self.y1, x2=self.x2, y2=self.y2,
                                                          unit_cons=UnitConstant.FLAG_A.value))

        for unit in [UnitConstant.ARMY_TENT_1.value, UnitConstant.ARMY_TENT_2.value]:
            else_effects.append(lambda p, u=unit: ChangeOwnership(sourcePlayer=p, targetPlayer=0,
                                                                  x1=self.x1, y1=self.y1, x2=self.x2 - 1,
                                                                  y2=self.y2 - 1,
                                                                  unit_cons=u))
            for pp in range(0, 9):
                then_effects.append(lambda p, u=unit, tp=pp: ChangeOwnership(sourcePlayer=tp, targetPlayer=p,
                                                                             x1=self.x1, y1=self.y1, x2=self.x2 - 1,
                                                                             y2=self.y2 - 1,
                                                                             unit_cons=u))

        super().__init__(capture_conditions=conditions, lost_conditions=[loss_condition],
                         capture_effects=then_effects, lost_effects=else_effects,
                         text_id="TrainingCamp({},{})_".format(x, y))

    def setup(self, scenario):

        if self.use_flags:
            scenario.units.new(owner=0, x=self.x1, y=self.y1, type=UnitConstant.FLAG_A.value)
            scenario.units.new(owner=0, x=self.x1, y=self.y2, type=UnitConstant.FLAG_A.value)
            scenario.units.new(owner=0, x=self.x2, y=self.y1, type=UnitConstant.FLAG_A.value)
            scenario.units.new(owner=0, x=self.x2, y=self.y2, type=UnitConstant.FLAG_A.value)

        if self.add_army_tent:
            scenario.units.new(owner=0, x=self.x, y=self.y, type=UnitConstant.ARMY_TENT_1.value)

        if self.frontier_tile:
            scenario.build_rectangle(self.x1, self.y1, self.x2 - 1, self.y2 - 1, tile_type=self.frontier_tile)

        for p, t in enumerate(self.boosting_triggers):
            p = p + 1
            t.if_(Timer(60)) \
                .then_(
                SendChat(player=p, text="Boosting units of P{} from Training Camp ({},{})".format(p, self.x, self.y))) \
                .then_(ChangeObjectAttack(p, self.bonus_attack_per_min, x1=self.x1, x2=self.x2 - 1, y1=self.y1,
                                          y2=self.y2 - 1))

            scenario.add(t)
        super().setup(scenario)
