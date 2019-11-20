from aot.meta_triggers.metatrigger import MetaTrigger
from aot.model.effect import GiveExtraPop, GiveHeadroom, SendChat
from aot.model.trigger import Trigger


class NoHouseNeeded(MetaTrigger):
    def __init__(self, population, player):
        self.population = population
        self.player = player

    def setup(self, scenario):
        t = Trigger("NoHouseNeeded ({} pop for P{})".format(self.population, self.player), enable=True)
        if self.population > 500:
            t.then_(GiveExtraPop(player=self.player, amount=self.population- 500))

        t.then_(GiveHeadroom(player=self.player, amount=self.population ))
        t.then_(SendChat(player=self.player,
                         text="No house needed, you have a population capacity of {}".format(self.population)))
        scenario.add(t)
