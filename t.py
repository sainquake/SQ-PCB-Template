# pip install GitPython

import git
from git import Repo

local_repo = Repo()



'''
for refs in local_repo.heads:
    print(refs.name)

local_repo.git.checkout('boards', 'existed-boards.md')

f = open('existed-boards.md', "r")
print(f.read())
f.close()

import os

os.remove('existed-boards.md')

'''

local_repo.git.add('.')
commit_message = 'Some changes before switch to boards branch'
local_repo.index.commit(commit_message)

local_repo.git.checkout('boards')

f = open('existed-boards.md', "a")
f.write("Now the file has more content!")
f.close()

local_repo.git.add('.')
commit_message = 'Added new feature to other_branch'
local_repo.index.commit(commit_message)

local_repo.git.checkout('master')
