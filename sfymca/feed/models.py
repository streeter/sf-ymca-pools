from enum import Enum
import re


class Branch(Enum):
    Chinatown = 408
    Embarcadero = 417
    Marin = 425
    Peninsula = 454
    Presidio = 464
    Stonestown = 512


class Event(object):
    def __init__(self, eid, name, branch, studio, start, end, url=None):
        self.eid = eid

        parts = re.split(r'[\|\-]', name)
        parts = reversed([p.strip() for p in parts])
        name = ' '.join(parts)

        if studio:
            location = f'{studio}, {branch.name} YMCA'
        else:
            location = f'{branch.name} YMCA'

        self.name = name
        self.branch = branch
        self.location = location
        self.start = start
        self.end = end
        self.url = url
