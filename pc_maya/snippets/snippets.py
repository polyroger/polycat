import pymel.core as pm
import os
from pipeline_utilities import path_manipulation

def importAlembicFile():

    maya_file = pm.sceneName()
    
    starting_path = os.path.split(maya_file)[0]
    
    if maya_file == "":
        
        pm.confirmDialog(button="OK", message="Your scene has not been saved yet, please save or open a scene and try again", title="Save file location error")
        return None
   
    else:
        
        asset_path = path_manipulation.goFindDirectory(starting_path,"0_sourcegeo")
        abcfilter = "alembic (*.abc)"

        try:
            abc_file = pm.fileDialog2(fileFilter=abcfilter,dialogStyle=2,startingDirectory=asset_path,fileMode=1)[0]
            pm.AbcImport(abc_file,mode="import")
        except:
            print("The import alembic operation was cancelled by user")