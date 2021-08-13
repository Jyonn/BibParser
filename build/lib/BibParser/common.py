from enum import Enum


class Status(Enum):
    free = 1
    entry = 2
    shortname = 3
    free_attr = 4
    attr_key = 5
    attr_value = 6
    end = 7


class Conflict:
    replace = 'replace'
    ignore = 'ignore'
    alert = 'alert'
    compare = 'compare'


class Quote:
    quotes = ['""', '{}']
    starts = [quote[0] for quote in quotes]
    ends = [quote[1] for quote in quotes]

    def __init__(self, start):
        self.start = start
        self.end = None
        for index, s in enumerate(self.starts):
            if s == self.start:
                self.end = self.ends[index]
        assert self.end

    def __str__(self):
        return self.start + self.end


def boolize(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    return v