from . import transforms


def guess_size(columns=None, rows=None, length=None):
    """
    Given at least two of columns, rows and length, returns (columns, rows), or
    throws an exception if the paramters are inconsistent.
    """
    if length is None:
        assert not (columns is None or rows is None)

    elif columns is None:
        assert rows is not None
        columns = length // rows

    elif rows is None:
        rows = length // columns

    else:
        assert rows * columns <= length

    return columns, rows


def array_index(point, size, bigendian):
    if isinstance(point, int):
        return point

    if bigendian:
        start, stop, step = len(point) - 1, -1, -1
    else:
        start, stop, step = 0, len(point), 1

    index = point[start]
    last_size = size[start]

    for i in range(start + step, stop, step):
        index *= last_size
        index += point[i]
        last_size = size[i]

    return index


class ArrayMap(object):
    """Map points onto a strip of lights."""

    def __init__(self, strip, size,
                 transform=transforms.identity, bigendian=False):
        self.strip = strip
        self.size = size
        self.transform = transform
        self.bigendian = bigendian

    def index(self, point):
        point = self.transform(point, self.size)
        return array_index(point, self.size, self.bigendian)

    def __getitem__(self, point):
        return self.strip[self.point_to_index(point)]

    def __setitem__(self, point, value):
        self.strip[self.point_to_index(point)] = value
