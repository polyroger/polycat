"""
Polycat camera exporter
"""

import os
import pymel.core as pm

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

def bakeCamera(originalcam,camtobake,start,end,scene_scale):

    if originalcam == None:
        return None
    
    print("RUNNING BAKER")

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
