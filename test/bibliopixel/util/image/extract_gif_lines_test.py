import unittest
from unittest.mock import patch
from bibliopixel.util.image import extract_gif_lines


class ExtractGifLinesTest(unittest.TestCase):
    def test_extract(self):
        actual = list(extract_gif_lines._extract(GIF_LINES))
        self.assertEqual(actual, EXPECTED1)

    def test_extract_gif_lines(self):
        actual = list(extract_gif_lines.extract_gif_lines(GIF_LINES))
        self.assertEqual(actual, EXPECTED2)


GIF_LINES = """

# Here's some stuff.
# now code

```
    math.frog(23)
    print('glog')
```

# But there's no GIF file.
# More code:

```
    animation: BiblioPixelAnimations.matrix.MatrixRain
    shape: [2, 2]
```
```
    animation: BiblioPixelAnimations.matrix.MatrixRain
    shape: [32, 32]
```

![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/\
BiblioPixel/doc/bibliopixel/animations/something.gif)

```
    animation: .split
    shape: 128
```
![Result](https://raw.githubusercontent.com/ManiacalLabs/DocsFiles/master/\
BiblioPixel/doc/bibliopixel/animations/minimal.gif)
""".splitlines()

YAML_LINES_1 = """\
    animation: BiblioPixelAnimations.matrix.MatrixRain
    shape: [32, 32]
""".splitlines()

YAML_LINES_2 = """\
    animation: .split
    shape: 128
""".splitlines()

EXPECTED1 = [
    ('doc/bibliopixel/animations/something.gif', YAML_LINES_1),
    ('doc/bibliopixel/animations/minimal.gif', YAML_LINES_2)]

DATA1 = {
    'animation': 'BiblioPixelAnimations.matrix.MatrixRain',
    'shape': [32, 32]}

DATA2 = {
    'animation': '.split',
    'shape': 128}

EXPECTED2 = [
    ('doc/bibliopixel/animations/something.gif', DATA1),
    ('doc/bibliopixel/animations/minimal.gif', DATA2)]