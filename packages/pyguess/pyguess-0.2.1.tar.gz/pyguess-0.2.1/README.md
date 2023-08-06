<div align="center">

# pyguess
The Python library to Guess Swiss Streets

</div>

---

### Table of Contents

1.  [Disclaimer](#org00a6381)
2.  [Installation](#org549dfd1)
3.  [Usage](#orgc7de4f4)



<a id="org00a6381"></a>

# Disclaimer

**The library is in the alpha stage**, which means there's a lot of work to do still! So, don't expect too much from it!


<a id="org549dfd1"></a>

# Installation

To install from PyPi, run:

    pip install pyguess


<a id="orgc7de4f4"></a>

# Usage

    import pyguess
    from pyguess import Config, Candidate

    config = Config(
        path_to_streets="../misc/data/streets_data",
    )
    candidate = pyguess.guess_address("Rigistrasse 10", "Pfaffikon", config)

    assert candidate == Candidate("rigistrasse 10", "pfäffikon zh")
