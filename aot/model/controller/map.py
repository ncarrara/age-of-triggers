from aot.model import *
from .tiles import *


class Map:

    """Map structure

    Attributes:
        width (int, readonly): map width
        height (int, readonly): map height
        camera (int, int): starting camera
        tiles (Tiles): tiles section
        ai_type (int): type of AI on this map
    """

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def __init__(self, width=0, height=0, camera=(-1, -1), ai_type=4294967294):
        self._width = width
        self._height = height
        self.camera = camera
        self.tiles = Tiles(width, height)
        self.ai_type = ai_type  # type of AI for this examples

    def __repr__(self):
        name = "MAP INFO:\n"
        info1 = "\tSize: width:{} height:{}\n".format(self.width, self.height)
        info2 = "\tStarting Camera: x:{} y:{}\n".format(
            self.camera[0], self.camera[1])
        info3 = "\tAI Type: {}".format(self.ai_type)
        return name + info1 + info2 + info3

    def centerCamera(self):
        """Starting camera will be at center of map

        Todo:
            check function
        """
        self.camera = (self.width / 2, self.height / 2)

    def resize(self, newWidth, newHeight):
        """Resize map

        Todo:
            if resizing, insert directions NE, NW, SE...
        """
        self._width = newWidth
        self._height = newHeight
        self.tiles.resize(newWidth, newHeight)
