from aot.model import *


class Triggers:

    def __init__(self):
        self.__triggers = list()

    def __iter__(self):
        return iter(self.__triggers)

    def __len__(self):
        return len(self.__triggers)

    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError()
        return self.__triggers[index]

    def __delitem__(self, index):
        if index >= len(self):
            raise IndexError()
        self.__triggers.pop(index)

    def __repr__(self):
        name = "TRIGGERS: \n"
        info1 = "\tCOUNT:{}".format(len(self))
        return name + info1

    def toJSON(self):
        """return JSON"""
        data = dict()
        data["triggers"] = list()
        for trigger in self.__triggers:
            data["triggers"].append(trigger.toJSON())
        return data

    def new(self, **config):
        """Create new trigger"""
        trigger = self.add(Trigger(**config))
        return trigger

    def add(self,trigger):
        trigger.id = len(self.__triggers)
        self.__triggers.append(trigger)
        return trigger
