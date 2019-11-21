from collections import namedtuple

from aot.meta_triggers.metatrigger import MetaTrigger
from aot.model.condition import Timer
from aot.model.effect import MoveCamera, SendChat, ActivateTrigger
from aot.model.trigger import Trigger

DisplayMessage = namedtuple("DisplayMessage", ["text", "camera", "offset_timer"])


class DisplayMessages(MetaTrigger):
    def __init__(self, messages, enable=True, name="", players=range(1, 9)):
        super().__init__()
        self._messages = messages
        self._triggers = None
        self._enable = enable
        self._name = name
        self._players = players

    def setup(self, scenario):
        self._triggers = []
        for player in self._players:
            p_triggers = []
            for i, (text, camera, offset_timer) in enumerate(self._messages):
                t = Trigger(enable=False, name="[] display {}th message (P{})".format(self._name, i, player))
                t.if_(Timer(offset_timer))
                if camera is not None:
                    x, y = camera
                    t.then_(MoveCamera(player, x, y))
                t.then_(SendChat(player=player, text=text))
                p_triggers.append(t)
            for i in range(len(p_triggers) - 1):
                p_triggers[i].then_(ActivateTrigger(p_triggers[i + 1]))

        self._triggers[0].enable = self._enable

    def triggers_to_activate(self):
        return self._triggers
