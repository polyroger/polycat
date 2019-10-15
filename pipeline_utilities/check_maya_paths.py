import sys
import pymel.core as pm

def getMayaPaths(envvar):

    #PYTHONPATH
    pythonpaths = pm.mel.getenv("PYTHONPATH")
    listpythonpaths = pythonpaths.split(";")

    #MAYA_SCRIPT_PATH
    mayascriptpaths = pm.mel.getenv("MAYA_SCRIPT_PATH")
    listmayascriptpaths = mayascriptpaths.split(";")


    

    pathdict = {"pythonpath":listpythonpaths,"mayascriptpaths":listmayascriptpaths}

    print("\n\n The %s paths are : \n\n" % envvar)
    for i in pathdict[envvar]:
        print("\t - " + i)
     