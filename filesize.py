"""
Get the size of a file or directory in a human
readable format.

Attributes:
    B (int): 1 byte
    K (TYPE): 2**10
    M (TYPE): 2**20
    G (TYPE): 2**30
    SIZE (TYPE): SIZE = [B, K, M, G]
    UNIT (list): UNIT = ["B", "K", "M", "G"]
    UNIT_MAP (TYPE): UNIT_MAP = dict(zip(UNIT, SIZE))
"""

__author__ = "Ricky L Wilson"
__version__ = 1.0


import bisect
import os
import pathlib
from functools import lru_cache

B = 1
K = 2 ** 10
M = 2 ** 20
G = 2 ** 30
SIZE = [B, K, M, G]
UNIT = ["B", "K", "M", "G"]
UNIT_MAP = dict(zip(UNIT, SIZE))


def files(pth):
    """ Iterate over the files in pth.
    Does not yield any result for the
    special paths '.' and '..'.
    Directories will be omitted.
    """
    pth = pathlib.Path(pth)
    return filter(lambda p: p.is_file(), pth.iterdir())


def filesize(filename):
    """ Return the size of a file in bytes.
    """
    return os.stat(filename).st_size


def dirsize(pth):
    """ Get the total size of a directory.
    """
    return sum(map(os.path.getsize, files(pth)))


@lru_cache()
def human(byts, unit="auto"):
    """ Convert bytes to KB, MB, GB

    Args:
        byts (int): total bytes
        unit (str, optional): explicitly specify what unit to convert to.

    Returns:
        str: file size in human readable format.
    """
    if unit == "auto":
        index = bisect.bisect(SIZE, byts) - 1
        return f"{byts/SIZE[index]:.1f}{UNIT[index]}"
    unit_value = UNIT_MAP.get(unit.upper())
    return f"{byts/unit_value:.1f}{unit}"


def size(fpath=os.curdir, unit="auto"):
    """Summary

    Args:
        fpath (TYPE, optional): Path to file or Directory
                                Default os.curdir.
        unit (str, optional): 'b', k','m','g'

    Returns:
        str: File size.
    """
    fpath = pathlib.Path(fpath)
    if fpath.is_file():
        return human(filesize(fpath))
    return human(dirsize(fpath), unit)
