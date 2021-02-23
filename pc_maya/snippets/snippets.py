import pymel.core as pm
import maya.cmds as cmds
import os
import re
from pc_helpers import pc_path_helpers as pathhelp
# from pipeline_utilities import path_manipulation


def importAlembicFile():
    """
    Tries to get to the first source geo folder by going up from your maya file. Opens an alembic import dialog
    """

    maya_file = pm.sceneName()
    
    starting_path = os.path.split(maya_file)[0]
    
    if maya_file == "":
        
        pm.confirmDialog(button="OK", message="Your scene has not been saved yet, please save or open a scene and try again", title="Save file location error")
        return None
   
    else:
        asset_path = pathhelp.goFindFolder(starting_path,"0_sourcegeo")
        abcfilter = "alembic (*.abc)"

        try:
            abcfile = pm.fileDialog2(fileFilter=abcfilter,dialogStyle=2,startingDirectory=asset_path,fileMode=1)[0]
            importAlembic(abcfile)
        except:
            print("The import alembic operation was cancelled by user")

def importAlembic(abcfile):
    pm.AbcImport(abcfile,mode="import")

def addGeoSuffix(geoselection,geosuffix):
    repattern = r"_geo$"            #checks if the string ends in _geo

    myre = re.search(repattern,geoselection.name())
    
    if not myre:
        print ("{0} does not end in {1}, adding".format(geoselection.name(),geosuffix))
        geoselection.rename(geoselection.name() + geosuffix)
    else:
        print("All the selected geo alredy ends with _geo")

def duplicateAndMatch():
    """
    Rigging snippet just to copy multiple instances of one thing onto another, assumes that the target is in a heiracy that 
    containts the transforms, if the target is frozen it wont do anything

    """
    
    selection = pm.ls(selection=True)
    objtocopy = selection[0]
    objectstomatch = selection[1:]
    
    for obj in objectstomatch:
        
        source = pm.duplicate(objtocopy)[0]
        
        target = obj
        transm = pm.xform(obj,q=True,ws=True,m=True)
        pm.xform(source,ws=True,m=transm)
           
    pm.delete(objtocopy) 

def duplicate_shader():
    """
    Duplicates a shader by its shading engine so that any nodes plugged into the shading engine get duplicated too
    """
    selection = cmds.ls(selection=True)
    se = cmds.listConnections(selection, type="shadingEngine")
    newshader = cmds.duplicate(se, un=True) 

    return newshader

  