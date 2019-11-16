import enum


class Color(enum.Enum):
    WHITE = 0
    BLUE = 1
    RED = 2
    GREEN = 3
    YELLOW = 4
    AQUA = 5
    PURPLE = 6
    GREY = 7
    ORANGE = 8

    def __str__(self):
        if self is self.WHITE:
            return ""
        return '<{0}>'.format(self.name)

    def __init__(self, str_code):
        self.str_code = str_code
