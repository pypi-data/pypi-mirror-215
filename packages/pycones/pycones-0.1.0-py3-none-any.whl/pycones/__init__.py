"""
The pycones package provides useful functions
"""


def flatten(lst):
    """
    flatten a list
    """
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def list_join(*args, sep=""):
    """
    join lists into a string
    """
    res = sep.join(flatten(args))
    return res
