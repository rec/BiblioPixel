import abc, itertools


class Strip(abc.ABC):
    """Base class for contiguous strips.  You can also use a list as a Strip.
    NOt so now..."""

    @abc.abstractmethod
    def __getitem__(self, index):
        pass

    @abc.abstractmethod
    def __setitem__(self, index, value):
        pass

    @abc.abstractmethod
    def size(self):
        pass

    def for_each(self, function, *args, **kwds):
        indices = (range(i) for i in self.size())
        for index in itertools.product(*indices):
            function(index, *args, **kwds)


def fill(strip, item):
    strip.for_each(strip.__setitem__, item)
