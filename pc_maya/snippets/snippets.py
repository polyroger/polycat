import pymel.core as pm
import os
from pipeline_utilities import path_manipulation

def importAlembicFile():

    maya_file = pm.sceneName()
    starting_path = os.path.split(maya_file)[0]
    print(starting_path)

    #just a check to see if the scene file has bees saved or not
    if not path_manipulation.goFindDirectory(starting_path,"0_sourcegeo"):
        return None
    else:
        asset_path = path_manipulation.goFindDirectory(starting_path,"0_sourcegeo")

    abcfilter = "alembic (*.abc)"

    abc_file = pm.fileDialog2(fileFilter=abcfilter,dialogStyle=2,startingDirectory=asset_path,fileMode=1)[0]

    pm.AbcImport(abc_file,mode="import")