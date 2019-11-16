from aot import Scenario, DesactivateTrigger, Timer, CreateObject, KillUnitsByConstantInArea, Color, OwnObjectInArea, \
    MetaTrigger, \
    GiveExtraPop, GiveHeadroom, DamageObject, BuffHP
from aot import Scenario, Unit,  Trigger, Effect, SendChat, ChangeOwnership, Condition, \
    ActivateTrigger, Not, ObjectInArea, UnitConstant


def engineer_buff_hp(scenario, x, y, players):
    """
    Showcase trigger for a examples of Vince: https://steamcommunity.com/profiles/76561198032887388/
    :param x:
    :param y:
    :param players:
    :return:
    """
    for player in players:
        t = Trigger(name="engineer_buff_hp (p{})".format(player), enable=True, loop=True)
        t.if_(Timer(2))
        t.if_(OwnObjectInArea(amount=1, sourcePlayer=player,
                              x1=-1, y1=-1, x2=-1, y2=-1,
                              unit_cons=1380))
        t.then_(KillUnitsByConstantInArea(player=player, x1=-1, y1=-1, x2=-1, y2=-1, unit_cons=1380))
        for player2 in players:
            t.then_(CreateObject(player=player2, x=x, y=y, unit_cons=953))
        for player2 in players:
            t.then_(SendChat(player2, color=Color.GREEN,
                             text="P{} shares a permanent hitpoints upgrade with the team!".format(player)))
        scenario.triggers.add(t)


def if_castle(scenario, x, y, then=lambda player: None, use_flags=True):
    # TODO , if ifthenelse metatrigger instead of this
    """
    Activate a trigger if a castle if built in area (x,y):(x+4,y+4).
    If not, desactivate the trigger.
    :param x:
    :param y:
    :param then: create the trigger to activate/desactivate for the given player
    :return:
    """
    # create flags around the area
    if use_flags:
        scenario.players[0].units.new(x=x, y=y, type=UnitConstant.FLAG_B.type)
        scenario.players[0].units.new(x=x + 4, y=y, type=UnitConstant.FLAG_B.type)
        scenario.players[0].units.new(x=x, y=y + 4, type=UnitConstant.FLAG_B.type)
        scenario.players[0].units.new(x=x + 4, y=y + 4, type=UnitConstant.FLAG_B.type)
    players = range(1, 9)
    #
    bonus_areas = [Trigger(name="bonusArea({},{}) [start] (p{})".format(x, y, player), enable=True) for player in
                   players]
    bonus_areas_stopped = [Trigger(name="bonusArea({},{}) [stop] (p{})".format(x, y, player)) for player in players]
    for player in players:
        bonus_area_start = bonus_areas[player - 1]
        bonus_area_stop = bonus_areas_stopped[player - 1]
        scenario.triggers.add(bonus_area_start)
        scenario.triggers.add(bonus_area_stop)

        bonus_area_stop.if_(Not(ObjectInArea(amount=1, sourcePlayer=player,
                                             x1=x, y1=y, x2=x + 3, y2=y + 3,
                                             unit_cons=UnitConstant.CASTLE.type)))
        bonus_area_stop.then_(SendChat(text="You lost the area ({},{})".format(x, y), player=player))
        if use_flags:
            bonus_area_stop.then_(ChangeOwnership(sourcePlayer=player, targetPlayer=0,
                                                  x1=x, y1=y, x2=x + 4, y2=y + 4,
                                                  unit_cons=UnitConstant.FLAG_B.type))
        bonus_area_stop.then_(ActivateTrigger(bonus_area_start))

        bonus_area_start.if_(ObjectInArea(amount=1, sourcePlayer=player,
                                          x1=x, y1=y, x2=x + 3, y2=y + 3,
                                          unit_cons=UnitConstant.CASTLE.type))
        bonus_area_start.then_(SendChat(text="You captured the area ({},{})".format(x, y), player=player))
        if use_flags:
            bonus_area_start.then_(ChangeOwnership(sourcePlayer=0, targetPlayer=player,
                                                   x1=x, y1=y, x2=x + 4, y2=y + 4,
                                                   unit_cons=UnitConstant.FLAG_B.type))
        bonus_area_start.then_(ActivateTrigger(bonus_area_stop))

        if then:
            bonus_area_effect = then(player)
            if bonus_area_effect:
                scenario.triggers.add(bonus_area_effect)
                bonus_area_stop.then_(DesactivateTrigger(bonus_area_effect))
                bonus_area_start.then_(ActivateTrigger(bonus_area_effect))
            else:
                raise Exception("Bonus trigger returned by generator function should not be None")
