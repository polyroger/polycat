# POLYCAT
POLYCAT PIPELINE REPO

!! WORK IN A LOCAL DEV THAT IS A BRANCH OF DEVELOPMENT, DONT MESS UP THINGS FOR  PRODUCTION !!

>" The line between risk and failure is where you will find greatness " - Roger Wellard, October, 2019

This repo is separated by software.
All scripts specifically relating to each software should be in their respective folders, and then separated into a specific sub folder.
All utilities that are cross platform to be placed in the " pipeline_utilities " folder.
Standalone polycat software should be packaged in its own unique folder under its name. 
Code that can span across multiple applications / acts on the os, should be placed into a folder in the pipeline_utiliteis folder.

MAYA
The maya intergration centers around the module approach. Each user's maya.env needs to have a variable called "MAYA_MODULE_PATH" and that needs to point to the relavant mod folder on the server. There are production and development branches so if you want to be on the development branch (unstable) set to the mod folder in development. The mod file adds the production branch ( development or production ) to the 


