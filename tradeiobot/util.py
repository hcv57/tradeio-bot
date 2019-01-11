# https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
from decimal import Decimal


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def balance_changes(current, previous):
    differences = dict()
    for k in {**current, **previous}.keys():
        delta = Decimal(str(current.get(k, 0))) - Decimal(str(previous.get(k, 0)))
        if delta != 0:
            differences[k] = float(delta)
    return differences
