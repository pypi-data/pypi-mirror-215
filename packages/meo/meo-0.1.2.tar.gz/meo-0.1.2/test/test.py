import sys
import os

sys.path.insert(0, os.path.curdir)

from meo.crack import Crack

zg = Crack.zip("./test/flag.zip")
print(zg.by_seed_mp())