# splitgit
Python script for splitting out large git repos into smaller ones whilst retaining git history.

It is pretty much entierly based on [this blog post](https://imwill.com/split-a-large-git-repository/) by Hendrik Will 

The script clones from a local repo into a new directory, brings your chosen subdirectory to the top of the repo.

It will then perform some cleanup tasks before adding a new remote for your new repo.

The script will not push to the remote, that is currently left as task for the user, giving you a chance to review the new repo before proceeding.  The script will leave your original repository untouched, you will need to tidy that up yourself at present.

# Installation
You will need Python 2.7.x  Though I have only tested against 2.7.11
You will need to install gitpython

   pip --install gitpython

or you can setup a virtualenv and install gitpython there if you want.

#Usage

Lets say you have a big_repo that has directories foo and bar.  To split out foo into its own git repo.
   
   $ python splitgit.py -s ~/big_repo -d ~/new_repo -f foo -r origin -u git@github.com:Moncky/foo

see
   $ python splitgit.py --help 
for more info.

#Contributing

Please do.  Fork the project, then commit and push till your happy.