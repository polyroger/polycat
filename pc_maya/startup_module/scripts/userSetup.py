# Polycat Animation
# Standard user setup file for maya

import pymel.core as pm
import os
import sys

#package dependencies, not sure if this is the best way to do this.
#sys.path.append("F:\\projects\\pipeline\\packages") - this is for offsite dev
sys.path.append("Y:\\pipeline\\packages")

#external packages, after path append
import scandir

# these are deffered because they are required for the menu creation, if you are adding to the tools menu they must be added as deffered
pm.evalDeferred("from pc_maya.menus import pc_maya_tools_menu;pc_maya_tools_menu.createMayaMenus()")


