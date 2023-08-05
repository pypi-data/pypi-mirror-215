from genetics.helpers.git import generatePatches, getRepo
from pathlib import Path


def genPatches():
    path = Path(str(Path.cwd()) + "/patches")
    path.mkdir(parents=True, exist_ok=True)
    return generatePatches(getRepo(), str(path))
