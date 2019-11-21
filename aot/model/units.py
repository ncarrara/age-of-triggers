from .unit import *
# from .unit import *
import logging

logger = logging.getLogger(__name__)

class PlayerUnits:

    """Player units"""

    @property
    def playerIndex(self):
        return self.__player

    def __init__(self, playerIndex):
        self.__units = dict()
        self.__count = 0
        self.__player = playerIndex

    def __repr__(self):
        name = "PLAYER UNITS:\n"
        info1 = "\tPLAYER: {}\n".format(self.__player)
        info2 = "\tUNITS: {}".format(len(self.__units))
        return name + info1 + info2

    def __iter__(self):
        """iterate over all player's units"""
        for units in self.__units.values():
            for unit in units:
                yield unit

    def __len__(self):
        """return number of player's units"""
        return self.__count

    def delUnit(self, id):
        """delete unit(s) with given id from player

        Return:
            (int) number of deleted units
        """
        count = 0
        if self.existsId(id):
            count = len(self.__units[id])
            del self.__units[id]
        return count

    def delAll(self):
        """delete all unit(s) which belong to this player

        Return:
            int: count of deleted unit IDs (nut units)
        """
        count = 0
        keys = list(self.__units.keys()).copy()
        for key in keys:
            count += 1
            del self.__units[key]
        return count

    def getById(self, id):
        """get unit(s) by ID

        Args:
            id (int): unit(s) id

        Return:
            list(class.Unit): selected units
        """
        if id in self.__units:
            return self.__units[id]
        return None

    def getByType(self, unitType):
        """get unit(s) by unit type

        Args:
            unitType (int): unit type

        Return:
            list(class.Unit)" selected units
        """
        units = list()
        for unit in self:
            if unit.type == unitType:
                units.append(unit)
        return units

    def existsId(self, id):
        """check if id exits

        Args:
            id (int): unit id

        Return:
            (bool), True if exists
        """
        if id in self.__units:
            return True
        return False

    def _new(self, **unitConfig):
        """Create new unit for player

        class.Unit Attributes:
            id (int): unit ID
            x (int): unit X position
            y (int): unit Y position
            type (int): Unit type
            angle (int): Unit starting angle
            frame (int): Unit starting frame
            inID (int): in which ID is unit garissoned, -1 isn't
            unknown1 (int): Unknown variable
            unknown2 (int): Unknown variable

        Return:
            (class.Unit) unit
        """
        logger.debug("new units: {}".format(unitConfig))
        unitConfig['owner'] = self.__player
        unit = Unit(**unitConfig)

        if unit.id in self.__units:
            self.__units[unit.id].append(unit)
        else:
            self.__units[unit.id] = [unit]

        self.__count += 1
        return unit


class Units:

    """All player units included in examples"""

    @property
    def nextID(self):
        return self.__nextID

    @nextID.setter
    def nextID(self, value):
        self.__nextID = value

    def __init__(self):
        self.__playerUnits = [PlayerUnits(i) for i in range(17)]
        self.__nextID = 1

        # Unit.nextID = self.incrementNextID

    def __iter__(self):
        """iterate over all units in examples"""
        for pUnits in self.__playerUnits:
            for unit in pUnits:
                yield unit

    def __len__(self):
        """return number of units in examples"""
        count = 0
        for units in self.__playerUnits:
            count += len(units)
        return count

    def __getitem__(self, index):
        if index > 16:
            raise IndexError()
        return self.__playerUnits[index]

    def __repr__(self):
        name = "UNITS:\n"
        info1 = "\tCOUNT: {}\n".format(len(self))
        info2 = "\tNEXTID: {}".format(self.nextID)
        return name + info1 + info2

    def incrementNextID(self):
        while(self.existsId(self.__nextID)):
            self.__nextID += 1
        return self.__nextID

    def getNextID(self):
        return self.__nextID

    def toJSON(self):
        data = dict()
        data["units"] = list()
        for unit in self:
            data["units"].append(unit.toJSON())
        return data

    def delUnit(self, id):
        """delete unit(s) with given id in examples

        Return:
            (int) number of deleted units
        """
        count = 0
        for pUnits in self.__playerUnits:
            count += pUnits.delUnit(id)
        return count

    def delAll(self):
        """delete all units in examples

        Return:
            int: count of deleted unit IDs (nut units)
        """
        count = 0
        for pUnits in self.__playerUnits:
            count += pUnits.delAll()
        return count

    def getById(self, id):
        """get unit(s) by ID

        Args:
            id (int): unit(s) id

        Return:
            list(class.Unit): selected units
        """
        result = list()

        for pUnits in self.__playerUnits:
            units = pUnits.getById(id)
            if units:
                result.append(units)

        return result

    def existsId(self, id):
        """check if id exits

        Args:
            id (int): unit id

        Return:
            (bool), True if exists
        """
        for pUnits in self.__playerUnits:
            if (pUnits.existsId(id)):
                return True
        return False

    def new(self, **unitConfig):
        """Create new unit

        class.Unit Attributes:
            owner (int): player index
            id (int): unit ID
            x (int): unit X position
            y (int): unit Y position
            owner (int): Player, who owns this unit
            type (int): Unit type
            angle (int): Unit starting angle
            frame (int): Unit starting frame
            inID (int): in which ID is unit garissoned, -1 isn't
            unknown1 (int): Unknown variable
            unknown2 (int): Unknown variable

        Return:
            (class.Unit) unit
        """
        owner = unitConfig['owner']
        if (owner > 9) or (owner < 0):
            raise IndexError()
        if not "id" in unitConfig:
            unit = self[owner]._new(id=self.nextID, ** unitConfig)
            self.incrementNextID()
        else:
            unit = self[owner]._new(**unitConfig)
        return unit
