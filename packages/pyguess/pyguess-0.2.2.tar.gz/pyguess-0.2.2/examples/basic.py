import pyguess
from pyguess import Candidate, Config

config = Config(
    path_to_streets="../../misc/data/streets_data",
)

try:
    candidate1 = pyguess.guess_address("Rigistrasse 10", "Pfaffikon", config)
    candidate2 = pyguess.guess_address("Rigistrasse 10", 4054, config)
except BaseException as err:  # in case if you really need to catch panic!
    if "PanicException" in str(type(err)):
        print("PanicException caught:", err)
    raise err

assert candidate1 == Candidate("rigistrasse 10", "pfäffikon zh")
assert candidate2 == Candidate("rigistrasse 10", 4054)
