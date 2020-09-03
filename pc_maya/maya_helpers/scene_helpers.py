"""
Polycat scene helpers
"""
import pymel.core as pm
import os

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
    rglobals["bgrgb"] = bg.split(" ")[1:]

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

            pm.confirmDialog(title="No Camera Selected",message="Please select a camera to export")
            return None
    except :
        pm.confirmDialog(title="Nothing was selected",message="Please select a camera to export")
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

def createCineScopeCamera():
    
    camera = pm.camera()
    cam = camera[0]
    camshape = camera[1]

    #camera settings
    


def createHDCamera():
    pass