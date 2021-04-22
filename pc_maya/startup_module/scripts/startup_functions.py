"""
This is here as a place to add custom maya node defaults on startup. These are not perminant and will overide any other defaults set when maya launches
"""

import maya.cmds as cmds

def set_camera_aspect_default():
    """
    Sets the cameras film back so that the camera aspect default is 1.778 (HD)    
    """
    if cmds.optionVar(q='cameraVertAper') != 0.526:
        cmds.optionVar(remove='cameraVertAper')
        cmds.optionVar(fv=('cameraVertAper', 0.526))
    
    if cmds.optionVar(q='cameraHorizAper') != 0.935:
        cmds.optionVar(remove='cameraHorizAper')
        cmds.optionVar(fv=('cameraHorizAper', 0.935))


def set_ffmpeg_path():
    """
    Sets the ffmpeg path for the playblast tool on startup
    """
    if not cmds.optionVar(q="PcPlayblastUiFFmpegPath"):
        print("setting PcPlayblastUiFFmpegPath to '\\\\YARN\\projects\\pipeline\\utilities\\ffmpeg\\bin\\ffmpeg.exe' ")
        cmds.optionVar(sv=('PcPlayblastUiFFmpegPath',r'\\YARN\projects\pipeline\utilities\ffmpeg\bin\ffmpeg.exe'))
    
def import_default_arnold_shader():
    """
    imorts the default arnold polycat shader
    """
    default_shader = r"\\YARN\projects\pipeline\utilities\maya\shaders\pc_default\pc_default.mb"
    shader_name = "pc_default"

    if cmds.ls(shader_name):
        return
    else:
        try:
            print(default_shader)
            cmds.file(default_shader, i=True, iv=True)
        except:
            print("could not import default shader")

