import setuptools
from setuptools.command.install import install
import subprocess
import json
import os, sys
from shutil import copyfile

branch = "development"

#by default clones branch (which can be passed as a parameter python install.py branch test_branch)
#if branch doesnt exist clones the default_branch
def clone(repository, folder, default_branch, cwdp='', recursive = False):
    global branch
    print("Cloning "+repository)
    if recursive:
        subprocess.call(['git', 'clone', '--recursive', repository], cwd='./'+cwdp)
    else:
        subprocess.call(['git', 'clone', repository], cwd='./'+cwdp)

def main(argv):
    global branch
    if(len(argv) > 0):
        if(argv[0] == 'branch'):
           branch = argv[1]

if __name__ == "__main__":
    main(sys.argv[1:])

# set cwd
os.chdir(os.getcwd()+"/../")

# install requirements
subprocess.call(['pip', 'install', '-r', 'requirements.txt'], cwd='./')

# Clone Repos
clone('https://github.com/openworm/org.geppetto.frontend','org.geppetto.frontend','developmente', 'static')
clone('https://github.com/MetaCell/geppetto-scidash.git','geppetto-scidash','developmente', 'static/org.geppetto.frontend/src/main/webapp/extensions/')

# change extension
print("Enabling Geppetto SciDash Extension ...")
geppetto_configuration = os.path.join(os.path.dirname(__file__), './utilities/GeppettoConfiguration.json')
copyfile(geppetto_configuration, './static/org.geppetto.frontend/src/main/webapp/GeppettoConfiguration.json')

# Install and building
print("NPM Install and build for Geppetto Frontend  ...")
subprocess.call(['npm', 'install'], cwd='./static/org.geppetto.frontend/src/main/webapp/')
subprocess.call(['npm', 'run', 'build-dev-noTest'], cwd='./static/org.geppetto.frontend/src/main/webapp/')

