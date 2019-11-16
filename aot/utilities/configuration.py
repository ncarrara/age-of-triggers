import json

class Configuration(dict):

    def __init__(self,path):
        self.game_path_scenario = None
        self.temp_path = None
        self.test_path_scenario = None
        self.load(path)



    def load(self,path):
        with open(path) as json_file:
            self.__dict__ = json.load(json_file)
        return self
