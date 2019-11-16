import json

# singleton, a bit ugly
class Configuration(dict):
    C = None

    def __init__(self, path):
        self.game_path_scenario = None
        self.temp_path = None
        self.test_path_scenario = None
        self.per_path = None
        self.load(path)
        Configuration.C = self

    def load(self, path):
        with open(path) as json_file:
            self.__dict__ = json.load(json_file)

        return self
