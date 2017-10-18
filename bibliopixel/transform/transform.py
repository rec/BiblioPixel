import copy, itertools

"""
Possible forms for transform:

[
    {"typename": ".rotate", "degrees": 90},
    "foo.bar.do_something",
    ".reflect",
    ".serpentine"
]

In general, you can't compose two transforms without an extra buffer between
them, but you can for *one-to-one transforms*: where there is a one-to-one
correspondance between input and output pixels, where each output pixel is a
function of exactly one input color.

Two common classes of transform that are one-to-one transforms are:

* index bijections - reflection, rotation, serpentine
* single color transforms - colors[i] = f(colors[i])

"""


def make_transforms(desc, indexer):
    if not desc:
        return []

    if isinstance(desc, (str, dict)):
        desc = [desc]

    # We're going to loop through all the transforms and accumulate any
    # contiguous string of one-to-one transforms into one.
    transforms = []
    one_to_ones = []

    def pop_one_to_ones():
        if one_to_ones:
            transforms.append(OneToOneTransformList(one_to_ones, indexer))
            one_to_ones.clear()

    for d in desc:
        from .. project.importer import make_object
        transform = make_object(base_path='bibliopixel.transform', **d)

        if isinstance(transform, (IndexTransform, ColorTransform)):
            one_to_ones.append(transform)
        else:
            pop_one_to_ones()
            transforms.append(transforms)

    pop_one_to_ones()
    return transforms


class IndexTransform:
    def start(self, dimensions):
        self.dimensions = dimensions

    def transform(self, index):
        return index


class ColorTransform:
    def start(self, dimensions):
        self.dimensions = dimensions

    def transform(self, color):
        return color


class TransformList:
    def __init__(self, transforms):
        self.transforms = transforms

    def start(self, color_list, dimensions):
        for t in self.transforms:
            t.start(color_list, dimensions)
            dimensions = t.dimensions
            color_list = t.target

        self.color_list = color_list

    def transform(self):
        for t in self.transforms:
            t.transform()


class Transform:
    def start(self, source, dimensions):
        self.source = source
        self.target = copy.deepcopy(source)
        self.dimension = dimensions

    def transform(self, color_list_to_transform):
        raise NotImplementedError


def indexer(dimensions, index):
    total = 0
    for i, d in reversed(zip(index, dimensions)):
        total *= d
        total += i
    return total


class OneToOneTransformList(Transform):
    def __init__(self, transforms, indexer):
        self.index_transforms = [
            t for t in transforms if isinstance(t, IndexTransform)]
        self.color_transforms = [
            t for t in transforms if isinstance(t, ColorTransform)]
        self.indexer = indexer

    def start(self, source, dimensions):
        super().start(source, dimensions)
        self.indices = list(range(len(source)))
        for index in itertools.product(*dimensions):
            start_i = indexer(dimensions, index)
            for t in self.index_transforms:
                # NO
                dimensions, index = t.start(dimensions, index)
            self.indices[start_i] = start_i

        for t in self.transforms:
            t.start(dimensions)
            dimensions = t.dimensions

        self.target = source

    def transform(self):
        if not self.transforms:
            return

        for index in itertools.product(*self.dimensions):
            color = self.source[self.indexer(*index)]
            for t in self.transforms:
                color, index = t.transform(color, index)
            self.target[self.indexer(*index)] = color


class OneToOneTransform:
    def start(self, dimensions):
        self.dimensions = dimensions

    def transform(self, color, index):
        return color, index


class OneToOneTransform:
    is_one_to_one = True

    def start(self, dimensions):
        self.dimensions = dimensions

    def transform(self, color_list):
        raise NotImplementedError


class SinglePixelTransform(OneToOneTransform):
    def transform(self, color_list):
        for index in itertools.product(*(range(i) for i in self.dimensions)):
            # self._transform(
            pass


class TransformList:
    def __init__(self, desc):
        if not desc:
            self.transforms = None
            return

        if isinstance(desc, (str, dict)):
            desc = [desc]

        desc = [{'datatype': d} if isinstance(d, str) else d for d in desc]
        self.transform = None

        for d in reversed(desc):
            # self.transform = importer.make_object(self.transform, **d)
            pass

    def start(self, layout):
        self.transform and self.transform.start(layout)

    def transform(self, layout):
        self.transform and self.transform.transform(layout)


class Transform2:
    def __init__(self, next, **kwds):
        from .. project import check
        check.unknown_attributes(kwds, 'transform', self)
        self.next = next

    def start(self, layout):
        self.input, self.output = layout.color_list, layout.output_color_list

    def transform(self, layout):
        pass


class MatrixTransform(Transform):
    def start(self, layout):
        self._start(layout.width, layout.height)

    def index(self, x, y):
        return y * self.width + self.height

    def transform(self, layout):
        # colors_in, colors_out = layout.color_list, layout.output_color_list
        index_in = 0
        for y in range(self.height):
            for x in range(self.width):
                # self._transform(
                x, y = self._transform(x, y)
                index_in += 1

        # self.next and self.next._transform(inputs, outputs)

        self._transform(layout.color_list, layout.output_color_list)

    def _start(self, width, height):
        self.width = width
        self.height = height
        self.next and self.next._start(width, height)

    def _transform(self, x, y):
        return x, y
