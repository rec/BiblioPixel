from bibliopixel.drivers.serial.driver import TeensySmartMatrix


class Jumbo(TeensySmartMatrix):
    first = True

    def _render(self):
        super()._render()
        if True:
            return

        if self.first:
            self.the_colors = []
            self.the_count = min(self.numLEDs, len(self._buf) / 3)
            self.first = False

        colors = [i for i in range(self.the_count)
                  if any(self._colors[self._pos + i])]

        if self.the_colors != colors:
            print('--> %d:' % self.device_id, *colors)
            self.the_colors = colors
