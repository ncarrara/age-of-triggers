from collections import namedtuple

from aot.meta_triggers.metatrigger import MetaTrigger
from aot.model.condition import Timer
from aot.model.effect import MoveCamera, SendChat, ActivateTrigger, SendInstruction
from aot.model.trigger import Trigger

DisplayMessage = namedtuple("DisplayMessage", ["text", "camera", "timer"])


class DisplayMessages(MetaTrigger):
    def __init__(self, messages, enable=True, name="DisplayMessages", players=range(1, 9),as_instruction=False):
        super().__init__()
        self._messages = messages
        self._triggers = None
        self._enable = enable
        self._name = name
        self._players = players
        self._triggers = []
        for player in self._players:
            p_triggers = []
            for i, (message, camera, timer) in enumerate(self._messages):
                t = Trigger(enable=self._enable, name="[{}] display {}th message (P{})".format(self._name, i, player))
                t.if_(Timer(timer))
                if camera is not None:
                    x, y = camera
                    t.then_(MoveCamera(player, x, y))
                if as_instruction:
                    t.then_(SendInstruction(message=message,time=3))
                else:
                    t.then_(SendChat(player=player, message=message))
                p_triggers.append(t)

            # for i in range(len(p_triggers) - 1):
            #     print(p_triggers[i].name)
            #     p_triggers[i].then_(ActivateTrigger(p_triggers[i + 1]))

            self._triggers.extend(p_triggers)

    def setup(self, scenario):
        for t in self._triggers:
            scenario.add(t)
        super().setup(scenario)

    def triggers_to_activate(self):
        return self._triggers
