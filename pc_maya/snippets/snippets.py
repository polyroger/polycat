import pymel.core as pm
import os
import re
from pipeline_utilities import path_manipulation

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
        
        asset_path = path_manipulation.goFindDirectory(starting_path,"0_sourcegeo")
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
        print "{0} does not end in {1}, adding".format(geoselection.name(),geosuffix)
        geoselection.rename(geoselection.name() + geosuffix)
    else:
        print("All the selected geo alredy ends with _geo")



