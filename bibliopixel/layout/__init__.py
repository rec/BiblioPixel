from . rotation import Rotation, rotate_and_flip

from . circle import (
    calc_ring_pixel_count, calc_ring_steps, gen_circle, layout_from_rings)
from . cube import gen_cube, layout_from_cube
from . matrix import gen_matrix, layout_from_matrix


def gen_strip(num):
    return [[x, 0, 0] for x in range(num)]
