from aot.model.enums.age import Age
from aot.model.enums.civilization import Civilization
from aot.utilities.configuration import Configuration
from .resource import *
from .ai import *
from .diplomacy import *
from .camera import *
from aot.model.enums import *
import logging
logger = logging.getLogger(__name__)



class Player:

    """Information about player,
        there's 9 player (including gaia, which number is 0)

        Attributes:
            name (str): player name
            nameID (int): player name, string ID
            civilization (int): civilization
            population (int): max population
            color (int): player color
            allyVictory (int): ally victory
            active (int): is player active ?
            human (int): is player human player ?
            cameraX (int): starting camera X position
            cameraY (int): starting camera Y position
            nCameraX (int): starting camera X position
            nCameraY (int): starting camera Y position

            unknown1 (int): unknown
            unknown2 (str): unknown
            unknown3 (int): unknown
            unknown4 (int): unknown

            diplomacy (Diplomacy, readonly): diplomacy
            ai (AI, readonly): player AI
            resource (Resource, readonly): player resource
            camera (Camera, readonly): initial camera positon
    """

    @property
    def name(self):
        return self._name.strip()

    @name.setter
    def name(self, value):
        self._name = value[:256]

    @property
    def diplomacy(self):
        return self._diplomacy

    @property
    def resource(self):
        return self._resource

    @property
    def ai(self):
        return self._ai

    @property
    def camera(self):
        return self._camera

    def __init__(self, name="", constName="", index=0, nameID=-2,
                 civilization=1, age=2, population=200,
                 color=0, allyVictory=1,
                 unknown1=4,
                 unknown2="", unknown3=0, unknown4=0,vc_names="",
                 cty_names="",per_names="",
                 vc=b'',cty=b'',per=b'',ally_vic=0,
                 ):
        """Create player

        Args:
            name (str, optional): player name, ""
            nameID (int, optional): player name, string ID, 0
            civilization (int, optional): civilization, 0
            population (int, optional): max population, 75
            color (int, optional): player color, 0
            allyVictory (int, optional): ally victory, 1
            active (int, optional): is player active ?, 1
            human (int, optional): is player human player ?, 1
            cameraX (int, optional): starting camera X position, 0
            cameraY (int, optional): starting camera Y position, 0
            nCameraX (int, optional): starting camera X position, 0
            nCameraY (int, optional): starting camera Y position, 0
            unknown1 (int, optional): unknown, 4
            unknown2 (str, optional): unknown, ""
            unknown3 (int, optional): unknown, 0
            unknown4 (int, optional): unknown, 0
        """
        #if index==2: # TODO when from scratch
        #    self.per_names="Promisory"
        #    with open(Configuration.C.per_path,"rb") as f:
        #        self.per = f.read()
        #else:
        self.per_names = per_names
        self.per = per


        if index==1:
            self.human=1
        else:
            self.human = 0
        if index > 8:
            self.active = 0
        else:
            self.active = 1
        self.disabledTechs = [-1] *30
        self.disabledUnits = [-1] *30
        self.disabledBuildings = [-1] *30
        self.ally_vic = ally_vic
        self.vc_names=vc_names
        self.cty_names=cty_names

        self.cty=cty
        self.vc=vc
        self._name = name
        self.nameID = nameID
        self.constName = constName
        self.index = index  # player index, 0 = gaia, 1 = player 1
        self.civilization = civilization  # TODO: Add enum
        self.color = color  # enums.ePlayerColor
        self.allyVictory = allyVictory

        self.unknown1 = unknown1
        self.unknown2 = unknown2
        self.unknown3 = unknown3
        self.unknown4 = unknown4
        self.age = age  # starting age
        self.population = population  # max population

        self.__init()
        # logger.debug(self)
    def __init(self):

        self._diplomacy = Diplomacy()
        self._resource = Resource(index=self.index)
        self._unused_resource = Resource(index=self.index-1)
        self._ai = AI()
        self._camera = Camera()
        self.units = None

    def __repr__(self):
        name = "Player: \n"
        index = ""
        if self.index == 0:
            index = "0 (GAIA)"
        else:
            index = str(self.index)
        ind = "\tindex:{}\n".format(index)
        info = "\tname:{} civilization:{}\n".format(
            self.name, Civilization(self.civilization).name)
        info2 = "\tage:{} active:{} human:{}\n".format(
            Age(self.age).name, self.active, self.human)
        info3 = "\tcolor:{} - {}\n".format(
            self.color, ePlayerColor[self.color])
        return name + ind + info + info2 + info3

    def toJSON(self):
        """return toJSON

        Todo:
            extend this method
        """
        data = dict()
        data["index"] = self.index
        data["name"] = self.name
        data["nameID"] = self.nameID
        data["constName"] = self.constName
        data["civilization"] = self.civilization
        data["active"] = self.active
        data["human"] = self.human
        data["population"] = self.population
        data["color"] = self.color
        data["age"] = self.age
        data["allyVictory"] = self.allyVictory
        data["diplomacy"] = self.diplomacy.toJSON()
        data["resource"] = self.resource.toJSON()
        data["ai"] = self.ai.toJSON()
        data["camera"] = self.camera.toJSON()
        return data

# class Gaia(Player):
#     def __init__(self):
#         super().__init(human=0,active=1)