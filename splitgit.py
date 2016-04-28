from git import *
import argparse
import os
import shutil
import sys
import subprocess

join = os.path.join 

parser = argparse.ArgumentParser(description='Splitgit, for splitting large git repos into smaller ones')

parser.add_argument('-s', '--source', action='store', dest='source_repo_dir',
                    help='Path to Source Git repos directory')
parser.add_argument('-d', '--destination', action='store', dest='dest_repo_dir',
                    help='Path to Destination Git repo directory')
parser.add_argument('-f', '--subdirecotry', action='store', dest='subdir',
                    help='Subdirectory of the source git repo that you are splitting from the source repo')
parser.add_argument('-r', '--remote', action='store', dest='remote',
                    help='Name of your remote e.g origin')
parser.add_argument('-u', '--git_url', action='store', dest='git_url',
                    help='URL of your remote repo eg user@github.com:/user/my_repo.git')
parser.add_argument('-n', '--name', action='store', dest='new_repo_name',
                    help='New name of the repo if not the same as SUBDIR')

results = parser.parse_args()

source_repo_dir = results.source_repo_dir
subdir = results.subdir
dest_repo_dir = results.dest_repo_dir
dest_repo_url = results.git_url
if results.new_repo_name != None:
    new_repo_name = results.new_repo_name
else:
    new_repo_name = results.subdir
if results.remote != None:
    dest_remote = results.remote
else:
    dest_remote = 'origin'

#Setup the source repo
source_repo = Repo(source_repo_dir)
assert not source_repo.bare
source_git = Git(source_repo_dir)

#Clone the repo with no destination links
def clone_repo():
    print("Cloning Repo")
    global dest_git
    dest_git = Git(source_repo_dir)
    source_git.execute(["git", "clone", "-v", "--no-hardlinks", source_repo_dir, dest_repo_dir])

#clean out the destination if it exists
def clean_dest():
    if os.path.isdir(dest_repo_dir) == True:
        print(dest_repo_dir + "is a dir.  Cleaning it up before continuing\n")
        shutil.rmtree(dest_repo_dir)
    else:
        print("Destinatoin dir" + dest_repo_dir + "doesn't exist.  It will be created by the clone\n")

#We need to select the subdirectory we want to make the new repo from
def extract_dir(git_subdir):
    print("Extracting " + git_subdir)
    dest_git.execute(["git", "filter-branch", "--subdirectory-filter", git_subdir, "HEAD"])
    #This removes the refs we dont want
    #http://stackoverflow.com/questions/7389662/link-several-popen-commands-with-pipes
    print("Removing refs/original/ as we no longer need them")
    p1 = subprocess.Popen(["git", "for-each-ref", "--format=\"%(refname)\"", "refs/original/"], cwd=dest_repo_dir, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["xargs", "-n", "1", "git", "update-ref", "-d"], stdin=p1.stdout, stdout=subprocess.PIPE, cwd=dest_repo_dir)
    p2.communicate()
    print("Expiring ref log entries")
    dest_git.execute(["git", "reflog", "expire", "--expire=now", "--all"])
    print("Reseting HEAD")
    dest_git.reset("--hard")
    print("Remove remote origin")
    dest_repo.delete_remote("origin")
    print("Performing Git Garbage Collection")
    dest_git.execute(["git", "gc"])

#Add the new remote
def add_remote(name, url):
    dest_repo.create_remote(name, url)

clean_dest()

clone_repo()

dest_repo = Repo(dest_repo_dir)
assert not dest_repo.bare 
dest_git = Git(dest_repo_dir)

extract_dir(subdir)

add_remote(remote, dest_repo_url + "/" + new_repo_name)
