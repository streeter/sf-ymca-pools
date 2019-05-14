from enum import Enum

class Branch(Enum):
    Embarcadero = 417
    Marin = 425
    Peninsula = 454
    Presidio = 464
    Stonestown = 512


class Event(object):
    def __init__(self, id, name, branch, start, end):
        self.id = id
        self.name = name
        self.branch = branch
        self.start = start
        self.end = end
