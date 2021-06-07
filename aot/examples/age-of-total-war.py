from aot.meta_triggers.DisplayInstructions import DisplayInstructions, InstructionParameters
from aot.meta_triggers.invicible_unit import InvicibleUnit
from aot.meta_triggers.no_house_needed import NoHouseNeeded
from aot.model.condition import *
from aot.model.effect import *
from aot.model.enums.player import PlayerEnum
from aot.model.enums.sizes import Size
from aot.model.enums.tile import EnumTile
from aot.model.enums.unit import UnitConstant, UnitType
from aot.model.scenario import Scenario
from aot.model.trigger import Trigger
from aot.utilities.configuration import Configuration
import logging
import numpy as np

logging.basicConfig(level=logging.DEBUG)
C = Configuration("examples/configuration_de.json")

scn = Scenario(size=Size.NORMAL)
# scn.load(C.game_path_scenario, "template-aotw")
scn.load_template(Size.NORMAL)
#
TIME_TO_TRAIN_UNITS = 150
NUMBER_OF_MESSAGES_OPEN_AREA_COUNTDOWN = int(TIME_TO_TRAIN_UNITS / 5)  # int(TIME_TO_TRAIN_UNITS / 20)
MAX_TIME_OF_A_ROUND = 600
EXTRA_POPULATION = 60
WIN_AREA_POSITION_RELATIVE_TO_SPAWN = 15
SPAWN_LENGTH = 50
GOLD = 10000
FOOD = 10000
STONE = 0
WOOD = 10000
NUMBER_OF_WARNING = 10
SEP_BETWEEN_BUILDING = 5
NB_OF_COPY_BUILDINGS = 6
OFFSET_TUTO = 3

# if True:
#     TIME_TO_TRAIN_UNITS = 50
#     NUMBER_OF_MESSAGES_OPEN_AREA_COUNTDOWN = 5  # int(TIME_TO_TRAIN_UNITS / 2)
#     MAX_TIME_OF_A_ROUND = 60
#     EXTRA_POPULATION = 60
#     WIN_AREA_POSITION_RELATIVE_TO_SPAWN = 15
#     SPAWN_LENGTH = 50
#     GOLD = 10000
#     FOOD = 10000
#     STONE = 0
#     WOOD = 10000
#     NUMBER_OF_WARNING = 10
#     SEP_BETWEEN_BUILDING = 5
#     NB_OF_COPY_BUILDINGS = 6
#     OFFSET_TUTO = 1
NUMBER_OF_HILLS = 125
NUMBER_OF_FOREST = 15
NUMBER_OF_LACS = 15


class Team:
    def __init__(self, name):
        self.name = name

        self.x1_win = None
        self.x2_win = None
        self.y1_win = None
        self.y2_win = None
        self.players = None
        self.other_team = None
        self.players_starts = [None] * 4


class Player:

    def __init__(self, id):
        self.id = id
        self.position = (None, None)


team1 = Team("TEAM 1")
team1.players = [Player(i) for i in range(1, 5)]
team2 = Team("TEAM 2")
team2.players = [Player(i) for i in range(5, 9)]
team1.other_team = team2
team2.other_team = team1

diplomacy = Trigger("Set Diplomacy", enable=1).if_(Timer(5)).then_(
    SendInstruction(message="Setting Diplomacy 1234 vs 5678",
                    color=Color.ORANGE,
                    panel_location=1, time=5))

for team in [team1, team2]:
    for player in team.players:
        for target_player in team.other_team.players:
            diplomacy.then_(ChangeDiplomacy(source_player=player.id, target_player=target_player.id, diplomacy=3))
        for target_player in team.players:
            diplomacy.then_(ChangeDiplomacy(source_player=player.id, target_player=target_player.id, diplomacy=0))

scn.add(diplomacy)

HEIGHT_BATTEFIELD = scn.get_height() - 2 * SPAWN_LENGTH
WIDTH_BATTLE_FIELD = scn.get_width() - 1

# generate terrain
x_offset = 0
y_offset = SPAWN_LENGTH

# for w in range(NUMBER_OF_LACS):
#     i = np.random.randint(3, WIDTH_BATTLE_FIELD - 3)
#     j = np.random.randint(3, HEIGHT_BATTEFIELD - 3)
#     for _ in range(200):
#         sigma = 4
#         x = min(max(3, int(np.random.normal(i, sigma, 1))), WIDTH_BATTLE_FIELD - 3)
#         y = min(max(3, int(np.random.normal(j, sigma, 1))), HEIGHT_BATTEFIELD - 3)
#         scn.map.tiles[x + x_offset][y + y_offset].type = EnumTile.WATER_SHALLOW.value

for i in range(1, WIDTH_BATTLE_FIELD - 1):
    for j in range(1, HEIGHT_BATTEFIELD - 1):
        if np.random.random() > 0.9:
            scn.map.tiles[x_offset + i][y_offset + j].type = EnumTile.PALM_DESERT.value

for i in range(1, WIDTH_BATTLE_FIELD - 1):
    for j in range(1, HEIGHT_BATTEFIELD - 1):
        if np.random.random() > 0.9:
            scn.map.tiles[x_offset + i][y_offset + j].type = EnumTile.FOREST.value
            scn.units.new(owner=team.players[0].id, x=j + y_offset, y=i + x_offset,
                          unit_cons=UnitConstant.PALM_TREE.value, frame=np.random.randint(1, 5))

for hill in range(NUMBER_OF_HILLS):
    x1 = np.random.randint(2, WIDTH_BATTLE_FIELD - 2)
    y1 = np.random.randint(2, HEIGHT_BATTEFIELD - 2)
    w = 2 + int(np.random.random() * 5)
    h = 2 + int(np.random.random() * 5)
    x2 = min(x1 + w, scn.get_width())
    y2 = min(y1 + h, scn.get_height() - 2 * SPAWN_LENGTH)
    print(x1, x2, y1, y2)
    for i in range(x1, x2):
        for j in range(y1, y2):
            scn.map.tiles[x_offset + i][
                y_offset + j].elevation = 1  # np.random.randint(1,1) #maybe more but it crashes the game at launch ?
            scn.map.tiles[x_offset + i][y_offset + j].type = EnumTile.BLACK_GRASS.value
            for v in [1, 2]:
                for x, y in [(v, v), (-v, v), (v, -v), (-v, -v)]:
                    scn.map.tiles[x_offset + i + x][y_offset + j + y].type = EnumTile.BLACK_GRASS.value

for x in list(range(0, int(SPAWN_LENGTH))) + list(range(scn.get_width() - int(SPAWN_LENGTH), scn.get_width())):
    for y in range(0, scn.get_height() - 1):
        scn.map.tiles[y][x].type = EnumTile.LEAVES.value
        scn.map.tiles[y][x].elevation = 1

relics = []
for r in range(1, 4):
    x = int(scn.get_width() / 2)
    y = int(r * (scn.get_height() / 4))
    relic = scn.units.new(owner=0, x=x, y=y, unit_cons=UnitConstant.RELIC_CART.value)
    relic.reset_position = (x, y)
    relics.append(relic)
    for player in range(1, 9):
        scn.units.new(owner=player, x=x, y=y, unit_cons=UnitConstant.MAP_REVEAL.value)

create_kings = Trigger("create kings").if_(Timer(10))
scn.add(create_kings)

for player in range(1, 9):
    x = int(scn.get_height() / 2) - 4 + player
    create_kings.then_(CreateObject(unit_cons=UnitConstant.KING.value, player=player, x=x, y=0))
    create_kings.then_(CreateObject(unit_cons=UnitConstant.HAY_STACK.value, player=0, x=x, y=1))
    mt = InvicibleUnit(unit_hp=75, unit_cons=UnitConstant.KING.value, player=player)
    scn.add(mt)
    # create king prison
    create_kings.then_(ActivateMetaTrigger(mt))
create_kings.then_(CreateObject(unit_cons=UnitConstant.HAY_STACK.value, player=0, x=int(scn.get_height() / 2) - 4, y=0))
create_kings.then_(CreateObject(unit_cons=UnitConstant.HAY_STACK.value, player=0, x=int(scn.get_height() / 2) + 5, y=0))


def create_win_area(x, y, sep=4, team=None):
    for unit_constant in [UnitConstant.FLAG_A.value]:
        uns = [scn.units.new(owner=team.players[0].id, x=x, y=y, unit_cons=unit_constant),
               scn.units.new(owner=team.players[1].id, x=x + sep, y=y + sep, unit_cons=unit_constant),
               scn.units.new(owner=team.players[2].id, x=x, y=y + sep, unit_cons=unit_constant),
               scn.units.new(owner=team.players[3].id, x=x + sep, y=y, unit_cons=unit_constant)]

    for unit_constant in [UnitConstant.KING.value]:
        uns = [scn.units.new(owner=team.players[0].id, x=x + 1, y=y + 1, unit_cons=unit_constant),
               scn.units.new(owner=team.players[1].id, x=x + sep - 1, y=y + sep - 1, unit_cons=unit_constant),
               scn.units.new(owner=team.players[2].id, x=x + 1, y=y + sep - 1, unit_cons=unit_constant),
               scn.units.new(owner=team.players[3].id, x=x + sep - 1, y=y + 1, unit_cons=unit_constant)]

    for tile in scn.map.tiles.getArea(x, y, x + sep - 1, y + sep - 1):
        tile.type = EnumTile.ROCK.value
    for player in range(1, 9):
        scn.units.new(owner=player, x=x + int(sep / 2), y=y + int(sep / 2), unit_cons=UnitConstant.MAP_REVEAL.value)

    for ir, relic in enumerate(relics):
        create_flag_score = Trigger("create_flag_score for relic {} ({})".format(ir, team.name), enable=True)
        remove_flag_score = Trigger("remove_flag_score for relic {} ({})".format(ir, team.name))

        create_flag_score.if_(UnitInArea(player=0, unit=relic, x1=x, x2=x + sep - 1, y1=y, y2=y + sep - 1))
        create_flag_score.then_(CreateObject(player=0, x=x + int(sep / 2), y=y + int(sep / 2) - 1 + ir,
                                             unit_cons=UnitConstant.FLAG_B.value))
        create_flag_score.then_(SendInstruction("{} captured a relic !".format(team.name)))
        create_flag_score.then_(ActivateTrigger(remove_flag_score))
        scn.add(create_flag_score)

        remove_flag_score.if_(Not(UnitInArea(player=0, unit=relic, x1=x, x2=x + sep - 1, y1=y, y2=y + sep - 1)))
        remove_flag_score.then_(RemoveObjectByConstant(player=0,
                                                       x1=x + int(sep / 2), y1=y + int(sep / 2) - 1 + ir,
                                                       x2=x + int(sep / 2), y2=y + int(sep / 2) - 1 + ir,
                                                       unit_cons=UnitConstant.FLAG_B.value))
        remove_flag_score.then_(ActivateTrigger(create_flag_score))
        remove_flag_score.then_(SendInstruction("{} lost a relic !".format(team.name)))
        scn.add(remove_flag_score)

    team.x1_win = x
    team.y1_win = y
    team.x2_win = x + sep
    team.y2_win = y + sep


position_win_area = WIN_AREA_POSITION_RELATIVE_TO_SPAWN + int(SPAWN_LENGTH)
sep_win_area = 5
create_win_area(x=position_win_area, y=int(scn.get_height() / 2 - sep_win_area / 2),
                sep=sep_win_area, team=team1)
create_win_area(x=scn.get_width() - position_win_area - sep_win_area, y=int(scn.get_height() / 2 - sep_win_area / 2),
                sep=sep_win_area, team=team2)

for team in [team1, team2]:
    for p in team.players:
        x, y = team.x1_win + int(sep_win_area / 2), team.y1_win + int(sep_win_area / 2)
        for ir, relic in enumerate(relics):
            t = Trigger("move relics {} (P{})".format(ir, p.id), enable=True, loop=True)
            t.if_(CaptureUnit(player=p.id, unit=relic))
            t.then_(MoveObjectToPoint(player=p.id, unit=relic, x=x, y=y - 1 + ir))
            scn.add(t)

reset_relics = Trigger("reset relics")

for ir, relic in enumerate(relics):
    reset_relics.then_(ChangeOwnershipByUnit(source_player=0, target_player=0, unit=relic))
    reset_relics.then_(MoveObjectToPoint(player=0, unit=relic, x=relic.reset_position[0], y=relic.reset_position[1]))

scn.add(reset_relics)

buildings = [UnitConstant.CASTLE.value,
             UnitConstant.ARCHERY_RANGE.value,
             UnitConstant.MONASTERY.value,
             UnitConstant.BARRACKS.value,
             UnitConstant.SIEGE_WORKSHOP.value,
             UnitConstant.STABLE.value

             ]

OFFSET = int(((len(buildings) - 1) * SEP_BETWEEN_BUILDING) / 2)

# CREATE OR REMOVE BUILDINGS
create_buildings = Trigger("create buildings")
scn.add(create_buildings)
remove_buildings = Trigger("remove buildings")
scn.add(remove_buildings)
for team in [team1, team2]:
    for player in team.players:
        if player.id > 4:
            x = scn.get_width() - 4 - (NB_OF_COPY_BUILDINGS * SEP_BETWEEN_BUILDING)
        else:
            x = 4
        y = int(((player.id % 4) + 1) * (scn.get_height() / 5))
        player.position = (x, y)
        for _ in range(NB_OF_COPY_BUILDINGS):
            for i_unit, unit in enumerate(buildings):
                y_ = y + i_unit * SEP_BETWEEN_BUILDING - OFFSET
                create_buildings.then_(CreateObject(x=x, y=y_, unit_cons=unit, player=player.id))
                remove_buildings.then_(
                    RemoveObjectByConstant(player=player.id, unit_cons=unit, x1=x, x2=x, y1=y_, y2=y_))
            x = x + 5

# OPEN FIGHTING AREA
remove_haystacks = Trigger("open fighting area")
scn.add(remove_haystacks)
remove_haystacks.then_((RemoveObjectByConstant(player=PlayerEnum.GAIA.value,
                                               unit_cons=UnitConstant.HAY_STACK.value,
                                               x1=int(SPAWN_LENGTH),
                                               x2=int(SPAWN_LENGTH),
                                               y1=0,
                                               y2=scn.get_width() - 1)))
remove_haystacks.then_((RemoveObjectByConstant(player=PlayerEnum.GAIA.value,
                                               unit_cons=UnitConstant.HAY_STACK.value,
                                               x1=scn.get_width() - (int(SPAWN_LENGTH) + 1),
                                               x2=scn.get_width() - (int(SPAWN_LENGTH) + 1),
                                               y1=0,
                                               y2=scn.get_height() - 1)))
remove_haystacks.then_(
    SendInstruction(message="You may now fight ! Grab at least one relic quickly !", time=30, color=Color.RED,
                    panel_location=0))

# CLOSE FIGHTING AREA
create_haystacks = Trigger("create haystacks")
scn.add(create_haystacks)
for x in [SPAWN_LENGTH, scn.get_width() - SPAWN_LENGTH - 1]:
    for y in range(0, scn.get_height()):
        create_haystacks.then_(CreateObject(x=x, y=y, unit_cons=UnitConstant.HAY_STACK.value, player=0))

# CLEAN THE BATTLEFIELD OF MILITARY
kill_all_military = Trigger("kill all military")
scn.add(kill_all_military)

for p in range(1, 9):
    kill_all_military.then_(RemoveObjectByType(player=p, x1=-1, x2=-1, y2=-1, y1=-1,
                                               unit_type=UnitType.MILITARY.value))  # TODO it actually kill all, why ?
    kill_all_military.then_(RemoveObjectByType(player=p, x1=-1, x2=-1, y2=-1, y1=-1,
                                               unit_type=UnitType.MONK_WO_RELIC.value))  # TODO it actually kill all, why ?

# GIVE RESSOURCES
set_resource = Trigger("Resources")
scn.add(set_resource)

for p in range(1, 9):
    set_resource.then_(PayGold(player=p, amount=GOLD))
    set_resource.then_(PayFood(player=p, amount=FOOD))
    set_resource.then_(PayStone(player=p, amount=10000 if STONE == 0 else STONE))
    set_resource.then_(PayWood(player=p, amount=WOOD))
    set_resource.then_(GiveGold(player=p, amount=GOLD))
    set_resource.then_(GiveStone(player=p, amount=STONE))
    set_resource.then_(GiveWood(player=p, amount=WOOD))
    set_resource.then_(GiveFood(player=p, amount=FOOD))

# SET RESSOURCES TO ZERO
reset_resource = Trigger("reset Resources")
scn.add(reset_resource)
for p in range(1, 9):
    reset_resource.then_(PayGold(player=p, amount=GOLD))
    reset_resource.then_(PayFood(player=p, amount=FOOD))
    reset_resource.then_(PayStone(player=p, amount=10000 if STONE == 0 else STONE))
    reset_resource.then_(PayWood(player=p, amount=WOOD))

open_area = Trigger("Open Area")
scn.add(open_area)
open_area.then_(ActivateTrigger(reset_resource))
open_area.if_(Timer(TIME_TO_TRAIN_UNITS))
open_area.then_(ActivateTrigger(remove_haystacks))
open_area.then_(ActivateTrigger(remove_buildings))

# TRAINING TIME
messages = []
offset = int(TIME_TO_TRAIN_UNITS / NUMBER_OF_MESSAGES_OPEN_AREA_COUNTDOWN)
for n in range(0, NUMBER_OF_MESSAGES_OPEN_AREA_COUNTDOWN + 1):
    message = "You have {} game seconds remaining to train your units".format(TIME_TO_TRAIN_UNITS - n * offset)
    duration = offset
    if n == NUMBER_OF_MESSAGES_OPEN_AREA_COUNTDOWN:
        message = "Time's up ! Get ready !"
        duration = 3
    message = InstructionParameters(
        message=message,
        camera=None,
        duration=duration,
        color=Color.RED)
    messages.append(message)
display_open_area_countdown = []
for player in range(1, 9):
    mt = DisplayInstructions(messages=messages, enable=False, name="train cd (P{})".format(player), player=player,
                             panel_location=1)
    display_open_area_countdown.append(mt)
    scn.add(mt)

# START A NEW ROUND
new_round = Trigger("new_round", enable=False)
scn.add(new_round)
new_round.then_(ActivateTrigger(open_area))
for mt in display_open_area_countdown:
    new_round.then_(ActivateMetaTrigger(mt))
new_round.then_(ActivateTrigger(reset_relics))
for team in [team1, team2]:
    for p in team.players:
        new_round.then_(MoveCamera(player=p.id, x=p.position[0], y=p.position[1]))
new_round.then_(ActivateTrigger(set_resource))
new_round.then_(ActivateTrigger(create_buildings))
new_round.then_(ActivateTrigger(create_haystacks))
new_round.then_(ActivateTrigger(kill_all_military))
new_round.then_(ActivateTrigger(create_kings))

two_relic_warning_from_now_on = Trigger("warning from now on").if_(Timer(MAX_TIME_OF_A_ROUND)).then_(SendInstruction(message="From now on, the first team with two relics wins the round", color=Color.RED))
scn.add(two_relic_warning_from_now_on)
new_round.then_(DesactivateTrigger(two_relic_warning_from_now_on))
open_area.then_(ActivateTrigger(two_relic_warning_from_now_on))

# WINNING CONDITIONS
for team in [team1, team2]:
    have_X_relic = lambda amount: ObjectInArea(source_player=0, unit_cons=UnitConstant.FLAG_B.value, amount=amount,
                                               x1=team.x1_win + int((team.x2_win - team.x1_win) / 2),
                                               x2=team.x1_win + int((team.x2_win - team.x1_win) / 2),
                                               y1=team.y1_win + int((team.y2_win - team.y1_win) / 2) - 1,
                                               y2=team.y1_win + int((team.y2_win - team.y1_win) / 2) + 1)

    compute_win_2_relics = Trigger("compute_win ({})".format(team.name))
    compute_win_no_military = Trigger("compute_win_no_military ({})".format(team.name))
    compute_instant_win_3_relics = Trigger("compute_instant_win ({})".format(team.name))
    after_win = Trigger("win {}".format(team.name))
    after_win.if_(Timer(6))
    after_win.then_(
        SendInstruction(message="{} wins this round !".format(team.name, MAX_TIME_OF_A_ROUND), color=Color.RED))
    after_win.then_(DesactivateTrigger(compute_win_2_relics))
    after_win.then_(DesactivateTrigger(compute_instant_win_3_relics))
    after_win.then_(DesactivateTrigger(compute_win_no_military))
    after_win.then_(ActivateTrigger(new_round))
    ####################################################################################################################
    # win is less than 5 militry for each player T
    compute_win_no_military.if_(Timer(int(MAX_TIME_OF_A_ROUND / 10)))
    for p in team.other_team.players:
        compute_win_no_military.if_(
            Not(ObjectInArea(amount=5, source_player=p.id, unit_type=UnitType.MILITARY.value, x1=0,
                             x2=scn.get_width() - 1, y1=0, y2=scn.get_height() - 1)))
    for p in team.players:
        compute_win_no_military.if_(
            ObjectInArea(amount=5, source_player=p.id, unit_type=UnitType.MILITARY.value, x1=0, x2=scn.get_width() - 1,
                         y1=0, y2=scn.get_height() - 1))
    compute_win_no_military.then_(
        SendInstruction(message="No military left for {} !".format(team.other_team.name), color=Color.RED, time=10,
                        panel_location=1))
    compute_win_no_military.then_(ActivateTrigger(after_win))
    ####################################################################################################################
    ####################################################################################################################
    # win after 10 win for anyone with 2 relics
    compute_win_2_relics.if_(have_X_relic(2))
    compute_win_2_relics.if_(Timer(MAX_TIME_OF_A_ROUND))
    compute_win_2_relics.then_(
        SendInstruction(message="{} captured 2 relics after {}s !)".format(team.name, MAX_TIME_OF_A_ROUND),
                        color=Color.RED, time=10, panel_location=1))
    compute_win_2_relics.then_(ActivateTrigger(after_win))
    ####################################################################################################################
    ####################################################################################################################
    # instant win if 3 relics
    compute_instant_win_3_relics.if_(have_X_relic(3))
    compute_instant_win_3_relics.then_(
        SendInstruction(message="{} captured 3 relics !".format(team.name), color=Color.RED, time=10, panel_location=1))
    compute_instant_win_3_relics.then_(ActivateTrigger(after_win))
    ####################################################################################################################
    open_area.then_(ActivateTrigger(compute_win_2_relics))

    open_area.then_(ActivateTrigger(compute_instant_win_3_relics))
    open_area.then_(ActivateTrigger(compute_win_no_military))

    scn.add(after_win)
    scn.add(compute_win_2_relics)
    scn.add(compute_instant_win_3_relics)
    scn.add(compute_win_no_military)

setup_population = Trigger(enable=True,name="Setup population")
scn.add(setup_population)
for player in range(1, 9):
    setup_population.then_(GiveExtraPop(player=player, amount=EXTRA_POPULATION))
    setup_population.then_(GiveHeadroom(player=player, amount=200 + EXTRA_POPULATION))



# TUTORIAL
for team in [team1, team2]:
    for player in team.players:
        offset = 0
        m1 = InstructionParameters("Welcome to Age of Total War", None, 2 * OFFSET_TUTO, Color.BLUE)
        m2 = InstructionParameters("To win a round, you need to bring 3 relics cart to this area",
                                   (team.x1_win, team.y1_win), 3 * OFFSET_TUTO, Color.BLUE)
        m3 = InstructionParameters(
            "You also win a round if you hold 2 relics for {} seconds".format(MAX_TIME_OF_A_ROUND),
            (team.x1_win, team.y1_win), 3 * OFFSET_TUTO, Color.BLUE)
        m4 = InstructionParameters(
            "If you opponent has almost no military remaining, you can also win the round".format(MAX_TIME_OF_A_ROUND),
            (team.x1_win, team.y1_win), 3 * OFFSET_TUTO, Color.BLUE)
        messages = [m1, m2, m3, m4]
        for i, relic in enumerate(relics):
            messages.append(
                InstructionParameters("This is relic [{}]".format(i + 1), (relic.x, relic.y), OFFSET_TUTO, Color.BLUE))
        messages.append(
            InstructionParameters("Good Luck and Have Fun", (player.position[0], player.position[1]), OFFSET_TUTO,
                                  Color.BLUE))
        display_tutorial = DisplayInstructions(messages=messages, name="()".format(player.id), enable=True,
                                               player=player.id, panel_location=0)
        scn.add(display_tutorial)

time_tutorial = 13 * OFFSET_TUTO


start_first_round = Trigger("start_first_round", enable=True)
scn.add(start_first_round)
start_first_round.if_(Timer(time_tutorial-5)) # first round tends to be delayed
start_first_round.then_(ActivateTrigger(new_round))

for player in scn.players:
    player.age = 6

scn.save(C.game_path_scenario, "age-of-total-war [alpha]")

# TODO add meta trigger, "messages"
# TODO make such that we can activate desactivate meta triggers (using a list of activable triggers)
# TODO add a function to clean an area (with default tile and elevation ?)
# TODO add a function to remove all units of a player ?
# TODO add a function to remove all animals
