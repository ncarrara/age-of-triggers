from aot import Trigger, ActivateTrigger, Not
from aot.meta_triggers.metatrigger import MetaTrigger


class Capture(MetaTrigger):

    def __init__(self, capture_conditions, text_id="Capture_",
                 lost_conditions=None,
                 capture_effects=None,
                 lost_effects=None,
                 players=range(1, 9)):
        """
        if "capture_conditions" condition hold, then trigger capture_effects
        when "lost_conditions" condition hold, then trigger lost_effects
        :param capture_conditions:
        :param capture_effects:
        :param lost_conditions: if None, lost_conditions will be not(capture_conditions)
        :param lost_effects:
        :param players:
        """
        if lost_effects is None:
            lost_effects = []
        if capture_effects is None:
            capture_effects = []
        if lost_conditions is None:
            lost_conditions = [lambda p: Not(capture_condition(p)) for capture_condition in capture_conditions]
        self.lost_conditions = lost_conditions
        self.capture_conditions = capture_conditions
        self.capture_effects = capture_effects
        self.lost_effects = lost_effects
        self.players = players
        self.text_id = text_id

    def setup(self, scenario):
        for player in self.players:
            if_trigger = Trigger(self.text_id + "if_(p{})".format(player), enable=True)
            else_trigger = Trigger(self.text_id + "else_(p{})".format(player))
            then_trigger = Trigger(self.text_id + "then_(p{})".format(player))
            if_not_trigger = Trigger(self.text_id + "if_not_(p{})".format(player))

            then_trigger.then_(ActivateTrigger(if_not_trigger))
            for then_ in self.capture_effects:
                then_trigger.then_(then_(player))

            else_trigger.then_(ActivateTrigger(if_trigger))
            for then_ in self.lost_effects:
                else_trigger.then_(then_(player))

            for condition in self.capture_conditions:
                if_trigger.if_(condition(player))
            if_trigger.then_(ActivateTrigger(then_trigger))

            for condition in self.lost_conditions:
                if_not_trigger.if_(condition(player))
            if_not_trigger.then_(ActivateTrigger(else_trigger))

            scenario.triggers.add(if_trigger)
            scenario.triggers.add(if_not_trigger)
            scenario.triggers.add(then_trigger)
            scenario.triggers.add(else_trigger)


