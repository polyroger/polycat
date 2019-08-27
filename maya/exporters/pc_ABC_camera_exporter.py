# Polycat Maya Camera to Houdini Exporter
# 2019

"""
This script is designed to be run from a main window drop down menu in maya.
It creates a new camera at the scene root and on each frame sets and keys a specified value from the maya camera.
It also scales the translates by 0.1 so as to match the houdini scene scale.
A houdini camera at scale 0.1 is exported as well as a maya camera at scale 1.

"""

import pymel.core as pm
import os


class ExportMe():

    def __init__(self,mydirname,mysavename,myext):
        self.mydirname = mydirname
        self.mysavename = mysavename
        self.myext = myext

    def export(self, appname):

        # sets the string arguments needed for the ABC export a
        myfile = str("-file " + self.mydirname + "/" + self.mysavename + "_" + appname + self.myext)
        root = str("-root " + str(self.selection))
        myframerange = "-frameRange " + str(start) + " " + str(end)
        exportcommand = myfile + " " + root + " " + myframerange + " " + "-eulerFilter -worldspace"
        pm.AbcExport(j=exportcommand)

class RootCamera():

    def __init__(self):

        self.rootcam = pm.camera(name="rootCam")
        self.selection = self.rootcam[0]
        self.shape = self.selection.getShape()

    def __str__(self):
        return ("{}".format(self.selection))



class DuplicateCamera():

    def __init__(self,rootcam_selection):

        try:
            self.mayacam = pm.duplicate(rootcam_selection,name="maya_cam",inputConnections=True)
            self.selection = self.mayacam[0]
            self.shape = self.selection.getShape()
            print("The maya camera has been set")
        except:
            pm.confirmDialog(title="Camera Export Error", button="OK",message="There was an error setting the maya camera\nThe camera has not been exported, please try again")
            exit()

    def __str__(self):
        return ("{}".format(self.selection))





#SETTING THE ABC EXPORT STARTING DIRECTORY

def getexportdir():
    scenedir = pm.sceneName()
    dirname = os.path.dirname(scenedir)
    cameradir = os.path.abspath(os.path.join(dirname,"../../0_Camera"))

    if not os.path.exists(cameradir):
        cameradir = "Y:/"

    return cameradir

startdir = getexportdir()

# HAVE TO INCLUDE THIS
def getSceneSettings():
    """
    Gets the values for the scenes export
    :return: tuple (int "start" , int "end", int "scene_scale") 
    """
    start = int(pm.playbackOptions(query=True, min=True))
    end = int(pm.playbackOptions(query=True, max=True))

    return (start, end,)


# SETTING THE VARIABLES FOR THE ABC EXPORT
exportfilepath = pm.fileDialog2(fileFilter="*.abc", dialogStyle=2, startingDirectory=startdir)
basename = os.path.basename(exportfilepath[0])
mydirname = os.path.dirname(exportfilepath[0])
mysavename = os.path.splitext(basename)[0]
myext = os.path.splitext(basename)[1]


def bakeMe(thecamera,scene_scale=float(1.0)):

    start,end = getSceneSettings()

    for i in range(start, end):
        # updates the time and gets to camera attributes stored in the origcam object
        pm.currentTime(i, edit=True, update=True)

        # unpacks the object attributes into vaiables for readability
        mylens = mayacam.shape.focalLength.get()
        mysensorx = mayacam.shape.horizontalFilmAperture.get()
        mysensory = mayacam.shape.verticalFilmAperture.get()
        mytransx, mytransy, mytransz = pm.xform(mayacam.selection, query=True, ws=True, t=True)
        myrotx, myroty, myrotz = pm.xform(mayacam.selection, query=True, ws=True, ro=True)

        # key the lens
        pm.setKeyframe(thecamera.shape, v=mylens, at="focalLength")
        # key sensor
        pm.setKeyframe(thecamera.shape, v=mysensorx, at="horizontalFilmAperture")
        pm.setKeyframe(thecamera.shape, v=mysensory, at="verticalFilmAperture")
        # key translates and mulitplies it by the scenescale
        pm.setKeyframe(thecamera.selection, v=mytransx * scene_scale, at="translateX")
        pm.setKeyframe(thecamera.selection, v=mytransy * scene_scale, at="translateY")
        pm.setKeyframe(thecamera.selection, v=mytransz * scene_scale, at="translateZ")
        # key rotates - rotation order ZXY
        pm.setKeyframe(thecamera.selection, v=myrotz, at="rotateZ")
        pm.setKeyframe(thecamera.selection, v=myrotx, at="rotateX")
        pm.setKeyframe(thecamera.selection, v=myroty, at="rotateY")


def exportCameras():

    root_camera = RootCamera()




    maya_camera = MayaCamera(root_camera.selection)
    houdini_camera = HoudiniCamera(root_camera.selection)


