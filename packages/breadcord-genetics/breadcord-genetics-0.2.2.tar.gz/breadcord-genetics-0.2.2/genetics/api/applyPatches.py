from genetics.helpers.git import appPatches, getRepo
from pathlib import Path


def applyPatches():
    for i in Path(str(Path.cwd()) + "/patches").glob("*.patch"):
        appPatches(getRepo(), str(i))
