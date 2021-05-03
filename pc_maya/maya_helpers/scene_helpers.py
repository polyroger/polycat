"""
Polycat scene helpers
"""
import os, re
import pymel.core as pm
import maya.cmds as cmds
from pc_helpers import pc_file_helpers

def getRGlobals():
    
    rglobals = {}
    inchtomm = 25.4

    #resolution
    rglobals["resx"] = float(pm.getAttr("defaultResolution.width")) 
    rglobals["resy"] = float(pm.getAttr("defaultResolution.height"))
    rglobals["aspect"] = round(rglobals["resx"] / rglobals["resy"],2)

    #frame range
    rglobals["fstart"] =  pm.playbackOptions(q=True,minTime=True)
    rglobals["fend"] =  pm.playbackOptions(q=True,maxTime=True)

    #background color
    allcols = pm.displayRGBColor(list=True)
    bg = allcols[0]
    bgtop = allcols[1]
    bgbottom = allcols[2]
    rglobals["bgrgb"] = bg.split(" ")[1:]
    rglobals["bgtoprgb"] = bgtop.split(" ")[1:]
    rglobals["bgbottomrgb"] = bgbottom.split(" ")[1:]
    
    return rglobals

def getScenePath():

    sname = pm.sceneName()

    if not sname:
        print("The scene has not been saved, re routing to projects")
        return "\\\\YARN\\projects\\"
    else:
        path,myfile = os.path.split(sname)
        return path

def getSelectedCamera():
    """
    Returns the root node ( transform ) of the selected camera or None
    """

    try:
        cam = pm.ls(selection=True)[0]
        camshape = cam.getShape()
        
        if pm.nodeType(camshape) != "camera":

            pm.confirmDialog(title="No Camera Selected",message="Please select a camera to export",button=['Let me select a camera'], defaultButton='Let me select a camera')
            return None
    except :
        pm.confirmDialog(title="Nothing was selected",message="Please select a camera to export",button=['Let me select a camera'], defaultButton='Let me select a camera')
        return None
    
    return cam

def checkCameraAspect(camera,mglobals):

    camshape = camera.getShape()
    cancel = "Cancel"
    changecam = "Change Camera"
    changeglobal = "Change Global"

    if round(camshape.getAspectRatio(),2) != round(mglobals["aspect"],2):

        answer = pm.confirmDialog(  title="WARNING", 
                                    message="The camera aspect does not match the global aspect", 
                                    button=[changecam,changeglobal,cancel], 
                                    defaultButton=changeglobal, 
                                    cancelButton=cancel, 
                                    dismissString=cancel )
        
        if answer == cancel:
        
            return None
        
        elif answer == changecam:
        
            camshape.setAspectRatio(mglobals["aspect"])
            return True
        
        elif answer == changeglobal:

            resy = int(pm.getAttr("defaultResolution.height"))
            resx = int(resy * camshape.getAspectRatio())
            pm.setAttr("defaultResolution.width",resx)
            pm.setAttr("defaultResolution.deviceAspectRatio",camshape.getAspectRatio())
            return True
    
    else:
        return True

    pm.confirmDialog(title="WARNING",message="The camera check failed")
    return None   

def get_all_references():
    """
    Gets all the references in a maya scene
    
    Returns (list): A list of reference nodes
    """

    all_ref_nodes = cmds.ls(type="reference")
    ignore = ["_UNKNOWN_REF_NODE_", "sharedReferenceNode"] # There seems to be some behind the scenes nodes that cause the update to fail

    def filter_ignore(ref):
        return ref not in ignore
    
    def filter_loaded(ref):
        return cmds.referenceQuery(ref,il=True)

    ignored = list(filter(filter_ignore, all_ref_nodes))
    all_ref_nodes = list(filter(filter_loaded, ignored))

    return all_ref_nodes

def get_latest_reference_path(node):
    
    node_path = cmds.referenceQuery(node, f=True, un=False, wcn=True)
    node_dir, filename = os.path.split(node_path)
   
    # Checking the case for duplicated references that have the {1} duplication tag in the resolved name
    pattern = r"{\d+}"
    node_ext = re.sub(pattern,"",os.path.splitext(filename)[1])
   
    dir_contents = os.listdir(node_dir)
    # filter out the file type from the contents of the dirlist
    file_list = []
    for f in dir_contents:
        if os.path.splitext(f)[1] == node_ext:
            file_list.append(f)
    
    # get the resolved and un resolved path the un resolved could have variables in it, we are only interested in the file name so
    # strip the end off of the unresolved path and replace it with the getLatestFIle
    # so that the path returned is has the variable and the latest file. 

    updated_path = os.path.join(node_dir,pc_file_helpers.getLatestFile(file_list)).replace("\\","/")

    return updated_path
