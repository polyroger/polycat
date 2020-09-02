"""
Polycat scene helpers
"""
import pymel.core as pm
import os


def getScenePath():

    sname = pm.sceneName()

    if not sname:
        print("The scene has not been saved, re routing to projects")
        return "\\\\YARN\\projects\\"
    else:
        path,myfile = os.path.split(sname)
        return path


        

