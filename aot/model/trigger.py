from collections.abc import Iterable


class Trigger:

    @property
    def effects(self):
        return self.__effects

    @property
    def conditions(self):
        return self.__conditions

    def __init__(self, name="", enable=False, loop=False, make_header=0,
                 objective=False, description_order=0, id=-1, display_as_objective=0, mute_objectives=0):
        """Initialize examples trigger"""
        self.make_header = make_header
        self.id = id
        self.name = name  # name of trigger
        self.enable = enable  # ? enabled from start
        self.loop = loop  # ? loop trigger
        self.objective = objective  # ? objective
        self.display_as_objective = display_as_objective
        self.mute_objectives = mute_objectives
        self.description_order = description_order  # line number in objectives menu
        self.short_description = {"text": "", "display_on_screen": 0, "string_table_id": 0}
        self.trigger_description = {"text": "", "display_as_objective": 0, "string_table_id": 0}
        self.__effects = list()
        self.__conditions = list()
        self.unknowns = [0] * 11

    def __repr__(self):
        name = "TRIGGER: \n"
        info1 = "\tNAME: {}\n\tENABLED: {}\n".format(self.name, self.enable)
        info2 = "\tLOOP: {}\n\tOBJECTIVES: {}\n".format(
            self.loop, self.objective)
        info3 = "\tOBJECTIVES ORDER: {}\n".format(self.description_order)
        info4 = "\tTEXT: {}".format(self.text)
        return name + info1 + info2 + info3 + info4

    def toJSON(self):
        """return JSON"""
        data = dict()
        data["name"] = self.name
        data["enable"] = self.enable
        data["loop"] = self.loop
        data["objective"] = self.objective
        data["objectiveOrder"] = self.description_order
        data["text"] = self.text
        data["effects"] = list()
        for effect in self.__effects:
            data["effects"].append(effect.toJSON())
        data["conditions"] = list()
        for condition in self.__conditions:
            data["conditions"].append(condition.toJSON())
        return data

    def then_(self, effect):
        if isinstance(effect, Iterable):
            self.__effects.extend(effect)
        else:
            self.__effects.append(effect)
        return self

    def if_(self, condition):

        if isinstance(condition, Iterable):
            self.__effects.extend(condition)
        else:
            self.__effects.append(condition)
        return self
