from collections import namedtuple

from aot.meta_triggers.metatrigger import MetaTrigger
from aot.model.condition import Timer
from aot.model.effect import MoveCamera, SendChat, ActivateTrigger, SendInstruction
from aot.model.enums.color import Color
from aot.model.trigger import Trigger

InstructionParameters = namedtuple("DisplayMessage", ["message", "camera", "duration","color"])


class DisplayInstructions(MetaTrigger):
    def __init__(self,player, messages, enable=True, name="", panel_location=None):
        super().__init__()
        self._messages = messages
        self._triggers = None
        self._enable = enable
        self._name = name
        self._triggers = []
        self.panel_location = panel_location
        self.player = player
        # for player in self._players:
        p_triggers = []
        for i in range(len(self._messages)):
            message, camera, duration,color = self._messages[i]
            if color is None:
                color = Color.WHITE
            t = Trigger(enable=False, name="{} {}th instruction".format(self._name, i))
            if i > 0:
                _, _, duration_previous_message,_ = self._messages[i - 1]
                t.if_(Timer(duration_previous_message))
            if camera is not None:
                x, y = camera
                t.then_(MoveCamera(self.player, x, y))
            t.then_(SendInstruction(message=message, time=duration, panel_location=self.panel_location,player=self.player,color=color))
            p_triggers.append(t)

        for i in range(len(p_triggers) - 1):
            p_triggers[i].then_(ActivateTrigger(p_triggers[i + 1]))
        p_triggers[0].enable = self._enable
        self._triggers.extend(p_triggers)

    def setup(self, scenario):
        for t in self._triggers:
            scenario.add(t)
        super().setup(scenario)

    def triggers_to_activate(self):
        return [self._triggers[0]]


    def triggers_to_deactivate(self):
        return self._triggers