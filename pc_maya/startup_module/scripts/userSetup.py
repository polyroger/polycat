# Polycat Animation
# Standard user setup file for maya

import pymel.core as pm
import os
import sys
import pc_maya


# package dependencies, not sure if this is the best way to do this.
# sys.path.append("F:\\projects\\pipeline\\packages") # for remote use
sys.path.append("\\\\YARN\\projects\\pipeline\\packages")
sys.path.append("\\\\YARN\\projects\\pipeline\\utilities\\studiolibrary-2.7.1\\src")

# #external packages, after path append
import scandir
import pullframerange
import node_defaults

#setting pipeline variables
node_defaults.set_camera_aspect_default()
node_defaults.set_ffmpeg_path()

# # these are deffered because they are required for the menu creation, if you are adding to the tools menu they must be added as deffered
pm.evalDeferred("from pc_maya.menus import pc_maya_tools_menu;pc_maya_tools_menu.createMayaMenus()")

# # Checking sequence data
pm.evalDeferred("pullframerange.makeRange()")



