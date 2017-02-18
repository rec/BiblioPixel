import functools
from . import index_ops

"""This module uses the operations in index_ops to make transforms."""


def transformer(function, *args):
    """
    Create a transform by binding a base function and arguments.
    """

    @functools.wraps(function)
    def transform(point, size):
        return function(point, size, *args)

    return transform


def maker(function):
    """"
    Bind a transformer to a base function.
    """

    @functools.wraps(function)
    def maker(*args):
        return transformer(function, *args)

    return maker


def identity(point, size):
    """
    A transform that returns a point unchanged.
    """
    return point


combine = maker(index_ops.combine)
reflect = maker(index_ops.reflect)
serpentine = maker(index_ops.serpentine)
transpose = maker(index_ops.transpose)

"""

reflect_x = reflect() = relect(0)
reflect_y = reflect(1)
reflect_xyz = reflect(0, 1, 2)

serpentine_x = serpentine() = serpentine(0)
serpentine_y = serpentine(1)
serpentine_xz = serpentine(0, 2)
serpentine_yz = serpentine(1, 2)
serpentine_zx = serpentine(2, 0)

transpose_xy = transpose() = transpose(0, 1)
transpose_xz = transpose(0, 2)
transpose_yz = transpose(1, 2)
"""
