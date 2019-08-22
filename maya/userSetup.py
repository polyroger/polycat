import sys
import os

# opens the command port for pycharm
# import maya.cmds as cmds
#
# if not cmds.commandPort(':4434', query=True):
#     cmds.commandPort(name=':4434')

#START OF PIPELINE REQUIREMENTS
# adds our script location for the maya session.
script_path = os.getenv("MAYA_PIPELINE_LIBRARY")
sys.path.append(script_path)


