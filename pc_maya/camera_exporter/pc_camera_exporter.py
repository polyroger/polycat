"""
Polycat camera exporter
"""

import os
import pymel.core as pm

def getGlobals():

    mglobal = {}
    
    #resolution
    mglobal["resx"] = pm.getAttr("defaultResolution.width")
    mglobal["resy"] = pm.getAttr("defaultResolution.height")
    mglobal["aspect"] = round(float(mglobal["resx"]) / float(mglobal["resy"]),3)

    #frame range
    mglobal["fstart"] =  int(pm.playbackOptions(q=True,minTime=True))
    mglobal["fend"] =  int(pm.playbackOptions(q=True,maxTime=True))

    return mglobal


def createCamera(cameraname,mglobals):

    newcamera = pm.camera()[0]
    newcamera_shape = newcamera.getShape()
    newcamera.rename(cameraname)

    newcamera.addAttr("resx",attributeType="short")
    newcamera.resx.set(mglobals["resx"])
    newcamera.addAttr("resy",attributeType="short")
    newcamera.resy.set(mglobals["resy"])

    newcamera_shape.setAspectRatio(mglobals["aspect"])

    return newcamera

def getSelectedCamera():

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


def bakeCamera(originalcam,camtobake,mglobals,scene_scale):

    if originalcam == None:
        return None
    
    print("RUNNING BAKER")

    start,end = (mglobals["fstart"],mglobals["fend"])
    
    originalcamshape = originalcam.getShape()
    camtobakeshape = camtobake.getShape()

    for i in range(start, end + 1):
        # updates the time to get that frames camera data
        pm.currentTime(i, edit=True, update=True)

        # unpacks the object attributes into vaiables for readability
        lens = originalcamshape.focalLength.get()
        sensorx = originalcamshape.horizontalFilmAperture.get()
        sensory = originalcamshape.verticalFilmAperture.get()
        transx, transy, transz = pm.xform(originalcamshape.getParent(), query=True, ws=True, t=True)
        rotx, roty, rotz = pm.xform(originalcamshape.getParent(), query=True, ws=True, ro=True)

        # key the lens
        pm.setKeyframe(camtobakeshape, v=lens, at="focalLength")
        # key sensor
        pm.setKeyframe(camtobakeshape, v=sensorx, at="horizontalFilmAperture")
        pm.setKeyframe(camtobakeshape, v=sensory, at="verticalFilmAperture")
        # key translates and mulitplies it by the scenescale
        pm.setKeyframe(camtobake, v=transx * scene_scale, at="translateX")
        pm.setKeyframe(camtobake, v=transy * scene_scale, at="translateY")
        pm.setKeyframe(camtobake, v=transz * scene_scale, at="translateZ")
        # key rotates - rotation order ZXY
        pm.setKeyframe(camtobake, v=rotz, at="rotateZ")
        pm.setKeyframe(camtobake, v=rotx, at="rotateX")
        pm.setKeyframe(camtobake, v=roty, at="rotateY")
