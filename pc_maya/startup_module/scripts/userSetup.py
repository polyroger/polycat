# Polycat Animation
# Standard user setup file for maya

import pymel.core as pm
from pc_maya.exporters import pc_ABC_camera_exporter

# these are deffered because they are required for the menu creation
pm.evalDeferred("from pc_maya.menus import pc_maya_tools_menu;pc_maya_tools_menu.createMayaMenus()")
pm.evalDeferred("from pc_maya.menus import menu_gui")
