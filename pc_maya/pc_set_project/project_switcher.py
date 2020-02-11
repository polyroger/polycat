# set up the workspace ( myworkspace = pm.core.system.workspace )
# there is a dictionary containing file rules that tell maya what folders to save different info
# make a new file rule dictionary, set the project to that path





import os
import pymel.core as pm 

def setworkspace():
    return pm.system.workspace()