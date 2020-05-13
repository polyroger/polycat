#Module for all the pre render Houdini scripts

import hou
import os

def saveSimHip():

    # from pc_houdini.render_scripts import pre_render;pre_render.saveSimHip() # call this from pre render in houdini

    node = hou.node("..")
    fullfilepath = node.parm("file").eval()
    (path,filename) = os.path.split(fullfilepath)
    noext = os.path.splitext(filename)[0]
    simname = noext + "_simsave.hip"
    savefolder = "simsave"

    fullsimsavepath = os.path.join(path,savefolder,simname)
    fullsimsavepath = fullsimsavepath.replace("\\","/")

    if not os.path.exists(path):
        os.makedirs(path)
    
    hou.hipFile.save(file_name=fullsimsavepath,save_to_recent_files=True)
    

