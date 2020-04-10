import re
from enum import Enum
from pathlib import Path


RECORDINGS_DIR = Path(__file__).parent.parent / 'recordings'


class Action(Enum):
    on = "ON"
    off = "OFF"

    def __str__(self):
        return self.value


def get_recordings(dir):
    recordings = {}
    files = dir.glob('*')
    for file in files:
        m = re.search(r'(.*)_(.*)\.csv', str(file.name))
        if m is None:
            continue
        if not recordings.get(m.group(1)):
            recordings[m.group(1)] = []
        recordings[m.group(1)].append(m.group(2))
    return recordings