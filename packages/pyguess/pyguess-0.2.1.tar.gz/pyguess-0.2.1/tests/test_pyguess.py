import unittest

import pyguess
from pyguess import Candidate, Config

CONFIG = Config(
    path_to_streets="../misc/data/streets_data",
)
EXAMPLES = [
    (
        "rigistr. 10",
        "Pfaffikon",
        Candidate("rigistrasse 10", "pfäffikon zh"),
    ),
    (
        "rigistr. 10",
        4054,
        Candidate("rigistrasse 10", 4054),
    ),
    (
        "Rigistrasse 10",
        "Pfäffikon",
        Candidate("rigistrasse 10", "pfäffikon zh"),
    ),
    ("Schlossstrasse 9", "Berg", Candidate("schlossstrasse 9", "berg tg")),
    ("Oberfeld 7", "Root", Candidate("oberfeld 7", "root")),
]


class TestPyguess(unittest.TestCase):
    def test_examples(self):
        for street, location, expected in EXAMPLES:
            actual = pyguess.guess_address(street, location, CONFIG)
            self.assertEqual(
                actual,
                expected,
                f"Comparing {actual} and {expected}",
            )
