from git import Repo


def genSources() -> Repo:
    return Repo.clone_from('https://github.com/Breadcord/Breadcord.git', 'source')
