import copy
from bibliopixel.animation.matrix import Matrix
from bibliopixel.colors import COLORS


class Flash(Matrix):
    def pre_run(self):
        self.cl = [COLORS.blue for i in self.color_list], [
            COLORS.black for i in self.color_list]

    def step(self, amt=1):
        self.color_list[:] = self.cl[self.cur_step % 2]
        super().step()
