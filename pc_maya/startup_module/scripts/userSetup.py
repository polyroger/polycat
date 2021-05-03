# Polycat Animation
# Standard user setup file for maya


import os
import sys
import maya.cmds as cmds
import pymel.core as pm
import pc_maya

# package dependencies, not sure if this is the best way to do this.
# sys.path.append("F:\\projects\\pipeline\\packages") # for remote use
sys.path.append("\\\\YARN\\projects\\pipeline\\packages")
sys.path.append("\\\\YARN\\projects\\pipeline\\utilities\\studiolibrary-2.7.1\\src")

# #external packages, after path append
import scandir
import pullframerange
import startup_functions

#setting pipeline variables
startup_functions.set_camera_aspect_default()
startup_functions.set_ffmpeg_path()

#DIRTY.....OH SO DIRTY, SETTING OF PROJECT VARIABLES
# os.environ["PROJASSETS"] = cmds.optionVar(q="pcPROJASSETS")

# setting some preffered settings that dont require functions
cmds.renderThumbnailUpdate(False)

# # these are deffered because they are required for the menu creation, if you are adding to the tools menu they must be added as deffered
pm.evalDeferred("from pc_maya.menus import pc_maya_tools_menu;pc_maya_tools_menu.createMayaMenus()")

# # Checking sequence data
pm.evalDeferred("pullframerange.makeRange()")

# setting the viewport 2.0 trnsparency sorting
pm.evalDeferred("cmds.setAttr('hardwareRenderingGlobals.transparencyAlgorithm', 5)")

#checking for references
pm.evalDeferred("from pc_maya.update_references import update_references; update_references.run_reference_update('scriptJob')")
pm.evalDeferred("cmds.scriptJob(event=['SceneOpened', 'from pc_maya.update_references import update_references; update_references.run_reference_update(\"scriptJob\")'])", lp=True)

#addimg default shader
pm.evalDeferred("startup_functions.import_default_arnold_shader()", lp=True) # this makes sure that the shader is created on startup
pm.evalDeferred("cmds.scriptJob(event=['NewSceneOpened', 'startup_functions.import_default_arnold_shader()'])", lp=True)
pm.evalDeferred("cmds.scriptJob(event=['SceneOpened', 'startup_functions.import_default_arnold_shader()'])", lp=True)


