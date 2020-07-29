# POLYCAT
POLYCAT ANIMATION PIPELINE REPO

!! WORK IN A LOCAL DEV THAT IS A BRANCH OF DEVELOPMENT, DONT MESS UP THINGS FOR  PRODUCTION !!

>" Hidden between the lines of risk and failure, you will find greatness, " - Roger Wellard, October, 2019

Each folder should contain all that is needed for the respected folder name.
All scripts specifically relating to each software should be in their respective folders, and then separated into a specific sub folder.
All utilities that are cross platform to be placed in the " pipeline_utilities " folder.
Standalone polycat software should be packaged in its own unique folder under its name. 
Code that can span across multiple applications / acts on the os, should be placed into a folder in the pipeline_utiliteis folder.

SOURCE CONTROL
We use GIT for source and version contol and GIT HUB for off site managment. Development is a branch of production. Production is tested code that works and that wont
break production.
Development is used for user testing so that selected people can test the code and bug report outside of the production branch.
Local Dev is where the main development happens, this is a branch of development and is only on the devs local drive.

Local dev pushes to development, development pushes to production. This all happens on GIT HUB, so the production and development local branch are always pulling from the GIT HUB repo so that all the branches remain insync with regards to their relative repo branches.


MAYA
The maya intergration centers around the module approach. Each user's maya.env needs to have a variable called "MAYA_MODULE_PATH" and that needs to point to the relavant mod folder on the server. There are production and development branches so if you want to be on the development branch (unstable) set to the mod folder in development. The mod file adds the code base ( development or production ) to the pythonpath and adds a new location to find the startup scripts. 


