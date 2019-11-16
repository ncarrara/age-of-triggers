from abc import ABC, abstractmethod



class MetaTrigger(ABC):
    pass

    @abstractmethod
    def setup(self, scenario):
        pass


class EffectGenerator(ABC):

    @abstractmethod
    def generate(self, player_id, info={}):
        pass


class ConditionGenerator(ABC):

    @abstractmethod
    def generate(self, player_id, info={}):
        pass

