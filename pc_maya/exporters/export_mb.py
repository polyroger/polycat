"""
Polycats export selection as mb
"""

import sys, os
import maya.cmds as cmds

from pc_maya.maya_helpers import export_helpers
from pc_helpers import pc_path_helpers as pathhelp



def run_export(root_name, asset_path):

    
    stripns = export_helpers.stripNameSpace(root_name)
    export_name = stripns.replace("_GGRP", "")
    ref_version = export_helpers.getReferenceVersion(root_name)
    export_path = pathhelp.checkForPath(asset_path,export_name,ref_version) # technically this path should aready be created from the abc exporter, keeping it here incase

    mb_name = export_name + "_latest.mb"
    mb_path = os.path.join(export_path, mb_name).replace("\\","/")
    cmds.select(clear=True)
    selection = cmds.select(root_name) # so only the targeted root node gets exported
    mb = cmds.file(mb_path, es=True, type="mayaBinary", sh=True, force=True)
    
    return mb

    
    


