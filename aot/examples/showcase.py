import logging
import numpy as np

from aot import Scenario, UnitConstant
from aot.model.enums.sizes import Size
from aot.utilities.configuration import Configuration

C = Configuration("aot/api/examples/configuration_de.json")
scn = Scenario(size=Size.GIANT)
y_area = 50
x_area = 50
castles = []
loots = []
quarries = []
lumbers = []
army_tents = []
pavilions = []
for p in range(0, 9):
    for unit in scn.players[p].units:
        x = int(unit.x)
        y = int(unit.y)
        if unit.type == UnitConstant.CASTLE.value:
            castles.append((x - 2, y - 2))
        elif unit.type == UnitConstant.LOOT.value:
            loots.append((x, y))
        elif unit.type == UnitConstant.LUMBER.value:
            lumbers.append((x, y))
        elif unit.type == UnitConstant.QUARRY.value:
            quarries.append((x, y))
        elif unit.type == UnitConstant.ARMY_TENT_1.value or unit.type == UnitConstant.ARMY_TENT_2.value:
            army_tents.append((x, y))
        elif unit.type == UnitConstant.PAVILION.value:
            pavilions.append((x, y))
for x, y in castles:
    castle_area = CaptureAreaWithCastle(
        x=x, y=y,
        x_area=x_area,
        y_area=y_area,
        use_flags=True,
        map_reveal=False,
        frontier_tile=EnumTile.ROCK.value,
        loop_convert=True,
        scn=scn)
    scn.add(castle_area)

for x, y in quarries:
    treasure = TreasureQuarry(x, y, 500, create_the_unit=False)
    scn.add(treasure)
for x, y in lumbers:
    treasure = TreasureLumber(x, y, 500, create_the_unit=False)
    scn.add(treasure)
for x, y in loots:
    treasure = TreasureLoot(x, y, 500, create_the_unit=False)
    scn.add(treasure)

for _ in range(120):
    n = np.random.random()
    x = int(np.random.random() * scn.get_width())
    y = int(np.random.random() * scn.get_height())
    if n < 0.33:
        treasure = TreasureLoot(x, y, 500)
    elif n < 0.66:
        treasure = TreasureLumber(x, y, 500)
    else:
        treasure = TreasureQuarry(x, y, 500)
    scn.add(treasure)

for x, y in army_tents:
    training_camp = TrainingCamp(
        x=x, y=y,
        radius=2,
        use_flags=True,
        frontier_tile=2,
        create_the_unit=False,
        scn=scn
    )
    scn.add(training_camp)

for x, y in pavilions:
    scn.add(MercenaryPavilion(x, y, create_the_unit=False))

scn.add(MercenaryPavilion(50, 50, create_the_unit=True))

scn.save(C.game_path_scenario, "2")

print("army_tents", army_tents)
print("loots", loots)
print("quarries", quarries)
print("lumbers", lumbers)
print("castles", castles)
# for unit in scn.players[1].units:
#     print(unit)
