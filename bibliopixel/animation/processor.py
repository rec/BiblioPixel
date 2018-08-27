import numpy as np
from . import wrapper
from .. project.types import channel_order as co
from .. util import color_list, permutation


class Processor(wrapper.Wrapper):
    def __init__(self, *args, scale=1, offset=0, gamma=1,
                 channel_order=None, permutation=None, reverse=False, **kwds):
        super().__init__(*args, **kwds)
        color_list.check_numpy(self)

        self.detach()
        self.channel_order = channel_order
        self.permutation = permutation
        self.scale = scale
        self.offset = offset
        self.gamma = gamma
        self.reverse = reverse

    def reset(self):
        self.scale = 1
        self.offset = 0
        self.channel_order = None
        self.permutation = None
        self.reverse = False

    def step(self, amt=1):
        super().step(amt)
        cl = self.color_list[::-1] if self.reverse else self.color_list

        np.copyto(cl, self.layout.color_list)
        if self.scale != 1:
            cl *= self.scale
        if self.offset != 0:
            cl += self.offset
        if self.gamma != 1:
            cl /= 256
            np.power(cl, self.gamma, out=cl)
            cl *= 256
        if self.permutation:
            cl[:] = cl[self.permutation, :]
        if self.channel_order:
            cl[:] = cl[:, self.channel_order]

    @property
    def channel_order(self):
        return self._channel_order

    @channel_order.setter
    def channel_order(self, channel_order):
        self._channel_order = channel_order and co.make(channel_order)

    def _permutation(self):
        if self.permutation is None:
            self.permutation = np.array(range(len(self.color_list)))
        return self.permutation

    def shuffle(self):
        np.random.shuffle(self._permutation())

    def advance(self, increasing=True, forward=True):
        permutation.advance_permutation(
            self._permutation(), increasing, forward)
