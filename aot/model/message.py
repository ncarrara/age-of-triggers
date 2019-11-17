class Message:

    """Messsage contains ID and Text

    Attributes:
        id (int): string ID
        text (str): text
    """

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    def __init__(self, text="", id=-2):
        self._id = id
        self._text = text
