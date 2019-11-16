from aot import MetaTrigger, GiveExtraPop, GiveHeadroom
from aot import Trigger, SendChat


class NoHouseNeeded(MetaTrigger):
    def __init__(self, population, player):
        self.population = population
        self.player = player

    def setup(self, scenario):
        t = Trigger("NoHouseNeeded ({} pop for P{})".format(self.population, self.player), enable=True)
        t.then_(GiveExtraPop(player=self.player, amount=self.population - 20))
        t.then_(GiveHeadroom(player=self.player, amount=self.population - 20))
        t.then_(SendChat(player=self.player,
                         text="No house needed, you have a population capacity of {}".format(self.population)))
        scenario.add(t)
