# Polycat Animation
# Standard user setup file for maya

import pymel.core as pm
import os
from pc_maya.exporters import pc_ABC_camera_exporter

# these are deffered because they are required for the menu creation, if you are adding to the tools menu they must be added as deffered
pm.evalDeferred("from pc_maya.menus import pc_maya_tools_menu;pc_maya_tools_menu.createMayaMenus()")
pm.evalDeferred("from pc_maya.menus import menu_gui")
pm.evalDeferred("from pc_dialogs.scene_export_dialog import PcSceneExporter ")
pm.evalDeferred("from pc_dialogs.maya_export_prep import NameGGRP")
