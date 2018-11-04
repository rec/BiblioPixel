import tempfile, unittest
from bibliopixel.util import compress


class CompressTest(unittest.TestCase):
    def test_round_trip(self):
        with tempfile.TemporaryDirectory('w') as tdir:
