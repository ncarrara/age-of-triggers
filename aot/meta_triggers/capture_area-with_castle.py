from aot import *
from aot.meta_triggers.capture import Capture
from aot.model.enums.unit import UnitGroup


class CaptureAreaWithCastle(Capture):
    def __init__(self, x, y, x_area, y_area, loop_convert=False, use_flags=True, map_reveal=True,
                 frontier_tile=EnumTile.ROCK.value, scn=None):
        self.x1 = max(0, x - int(x_area / 2)) + 3
        self.y1 = max(0, y - int(y_area / 2)) + 3
        self.x2 = min(scn.get_width() - 1, x + int(x_area / 2))
        self.y2 = min(scn.get_height() - 1, y + int(y_area / 2))
        self.map_reveal = map_reveal
        self.use_flags = use_flags
        self.frontier_tile = frontier_tile
        self.x = x
        self.loop_convert = loop_convert
        self.y = y
        if_ = lambda p: ObjectInArea(amount=1, sourcePlayer=p,
                                     x1=x, y1=y, x2=x + 3, y2=y + 3,
                                     unit_cons=UnitConstant.CASTLE.value)
        then_effects = []
        then_ = lambda p: SendChat(player=p, text="A castle has been built")
        then_effects.append(then_)
        # then_2 = lambda p:
        else_effects = []
        else_ = lambda p: SendChat(player=p, text="A castle has been destroyed")
        else_effects.append(else_)
        if use_flags:
            else_effects.append(lambda p: ChangeOwnership(sourcePlayer=p, targetPlayer=0,
                                                          x1=x, y1=y, x2=x + 4, y2=y + 4,
                                                          unit_cons=UnitConstant.FLAG_B.value))
            then_effects.append(lambda p: ChangeOwnership(sourcePlayer=0, targetPlayer=p,
                                                          x1=x, y1=y, x2=x + 4, y2=y + 4,
                                                          unit_cons=UnitConstant.FLAG_B.value))

        what_to_convert = [UnitGroup.BUILDING.value,
                           UnitGroup.WALL.value,
                           UnitGroup.FARM_FISH_TRAP.value,
                           UnitGroup.GATE.value,
                           UnitGroup.TOWER.value,
                           ]

        if self.loop_convert:
            self.loop_triggers = []
            for p in range(1, 9):
                loop_trigger = Trigger("loop convert ({},{}) (P{})".format(x, y, p), loop=True)
                for pp in range(0, 9):
                    if pp != p:
                        for group in what_to_convert:
                            loop_trigger.then_(ChangeOwnership(sourcePlayer=pp, targetPlayer=p,
                                                               x1=self.x1, y1=self.y1, x2=self.x2, y2=self.y2,
                                                               unitGroup=group))
                # loop_trigger.then_(SendChat(sourcePlayer=p,text="looping for {}".format(p)))
                self.loop_triggers.append(loop_trigger)

        if self.loop_convert:
            else_effects.append(lambda p, trigs=self.loop_triggers: DesactivateTrigger(trigs[p - 1]))
            then_effects.append(lambda p, trigs=self.loop_triggers: ActivateTrigger(trigs[p - 1]))
            for group in what_to_convert:
                else_effects.append(lambda p, g=group: ChangeOwnership(sourcePlayer=p, targetPlayer=0,
                                                                       x1=self.x1, y1=self.y1, x2=self.x2, y2=self.y2,
                                                                       unitGroup=g))
        else:
            for p in range(1, 9):
                for group in what_to_convert:
                    else_effects.append(lambda _, x=p, g=group: ChangeOwnership(sourcePlayer=x, targetPlayer=0,
                                                                                x1=self.x1, y1=self.y1, x2=self.x2,
                                                                                y2=self.y2,
                                                                                unitGroup=g))

            for p in range(1, 9):
                for group in what_to_convert:
                    then_effects.append(lambda p2, x=p, g=group: ChangeOwnership(sourcePlayer=x, targetPlayer=p2,
                                                                                 x1=self.x1, y1=self.y1, x2=self.x2,
                                                                                 y2=self.y2,
                                                                                 unitGroup=g))

        super().__init__(capture_conditions=[if_], capture_effects=then_effects, lost_effects=else_effects,
                         text_id="CaptureAreaWithCastle({},{})_".format(x, y))

    def setup(self, scenario):
        if self.use_flags:
            scenario.units.new(owner=0, x=self.x, y=self.y, type=UnitConstant.FLAG_B.value)
            scenario.units.new(owner=0, x=self.x + 4, y=self.y, type=UnitConstant.FLAG_B.value)
            scenario.units.new(owner=0, x=self.x, y=self.y + 4, type=UnitConstant.FLAG_B.value)
            scenario.units.new(owner=0, x=self.x + 4, y=self.y + 4, type=UnitConstant.FLAG_B.value)

        if self.map_reveal:
            for p in self.players:
                scenario.players[p].units.new(owner=p, x=self.x + 2, y=self.y + 2, type=UnitConstant.MAP_REVEAL.value)
        if self.frontier_tile:
            scenario.build_rectangle(self.x1, self.y1, self.x2, self.y2, tile_type=self.frontier_tile)
        if self.loop_convert:
            for y in self.loop_triggers:
                scenario.add(y)
        super().setup(scenario)
