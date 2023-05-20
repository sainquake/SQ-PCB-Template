# pip install GitPython

import git
from git import Repo

local_repo = Repo()

for refs in local_repo.heads:
    print(refs.name)

local_repo.git.checkout('boards', 'existed-boards.md')

f = open('existed-boards.md', "r")
print(f.read())
f.close()

import os

os.remove('existed-boards.md')