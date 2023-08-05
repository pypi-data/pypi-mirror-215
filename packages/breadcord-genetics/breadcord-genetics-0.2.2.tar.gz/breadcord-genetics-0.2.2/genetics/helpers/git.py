import git
import pathlib


def getRepo() -> git.Repo:
    return git.Repo(str(pathlib.Path.cwd()) + "/source")


def execute(cmd: str, repo: git.Repo):
    return repo.git.execute(cmd.split(), with_stdout=True)


def generatePatches(repo: git.Repo, out: str):
    return execute(f"git format-patch --output-directory {out} origin/HEAD..HEAD", repo)


def appPatches(repo: git.Repo, patch: str):
    return execute(f"git am {patch}", repo)