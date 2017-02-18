"""
These are operations that transform a point and a size - with perhaps
additional arguments.

Either point and size are integers - which represent 1-dimensional arrays;
or they are lists, which represent n-dimensional arrays.
"""


def combine(point, size, *transforms):
    """
    Perform zero or more transforms on a given point and size.
    """
    for transform in transforms:
        point = transform(point, size)

    return point


def transpose(point, size, i=0, j=1):
    """
    Transpose two distinct coordinates in a point.
    """
    assert i != j
    assert max(i, j) < size

    point = list(point)
    point[i], point[j] = point[j], point[i]

    # TODO: does this work?  Don't I have to transpose size too somehow?
    return point


def reflect(point, size, *indices):
    """
    Reflect a point in one coordinate.
    """
    if isinstance(point, int):
        return size - point - 1

    for i in indices or [0]:
        point[i] = size[i] - point[i] - 1

    return point


def serpentine(point, size, i=0, *switches):
    """
    Return either the original point, or the reflected point, depending on the
    parity of a list of switch indices.

    Only makes sense for points that are 2-d or greater.

    If no switches are given, it simply uses "all the other coordinates" as
    switches.
    """
    switches = switches or (s for s in switches if s != i)

    if sum(point[s] % 2 for s in switches) % 2:
        return reflect(point, size, i)

    return point
