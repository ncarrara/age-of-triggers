import enum


class Size(enum.Enum):

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, w, h):
        self.w = w
        self.h = h

    TINY = 120, 120
    SMALL = 144, 144
    MEDIUM = 168, 168
    NORMAL = 200, 200
    LARGE = 220, 220
    GIANT = 240, 240
    LUDAKRIS = None, None # TODO
