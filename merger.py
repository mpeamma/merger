#!/usr/local/bin/python3
import sys
from git import Repo
import os
from colorama import Fore, Style

if len(sys.argv) < 2:
    print("Syntax: merger.py <filename>")
    exit()

commits = [x.strip() for x in open(sys.argv[1], "r").readlines()]
successful_commits = []

repo = Repo(os.getcwd())
repo.config_reader()
git = repo.git
for commit_hash in commits:
    try:
        commit = repo.commit(commit_hash)
        if len(commit.parents) > 1:
            print(git.cherry_pick(commit_hash, m=1))
        else:
            print(git.cherry_pick(commit_hash))
    except:
        if len(successful_commits) > 0:
            print(Fore.GREEN + "Successful commits:")
            [print(x) for x in successful_commits]
        print(Fore.RED + "Failed on " + commit_hash)
        print("Commits left to cherry-pick:")
        [print(x) for x in commits if x not in successful_commits]
        print(Style.RESET_ALL)
        exit(1)

    successful_commits += [commit_hash]

print("Successfully cherry-picked all commits")
