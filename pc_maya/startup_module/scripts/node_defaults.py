"""
This is here as a place to add custom maya node defaults on startup. These are not perminant and will overide any other defaults set when maya launches
"""

import maya.cmds as cmds


def set_camera_aspect_default():
    """
    Sets the cameras film back so that the camera aspect default is 1.778 (HD)    
    """
    cmds.optionVar(remove='cameraVertAper')
    cmds.optionVar(remove='cameraHorizAper')
    cmds.optionVar( fv=('cameraVertAper', 0.526))
    cmds.optionVar( fv=('cameraHorizAper', 0.935))

