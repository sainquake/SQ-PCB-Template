# pip install GitPython

from git import Repo

local_repo = Repo()

for refs in local_repo.heads:
    print(refs.name)