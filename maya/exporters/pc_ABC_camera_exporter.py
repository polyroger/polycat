# todo:
# export both the maya camera and the houdini camera into a version folder with a .houdini or .maya tag - done
# unify all the classes to use the same attribute names so reading the code is easier - done ( should be further fixed with inheritance )
# add this to a maya polycat menu rather than a shelf tool - done
# add the camera to a version folder / check to see if a version exists and version up from it.
# create a standard nameing convention for cameras ( {scene}_{shot}_camera_{version}
# let the user select a folder rather than choosing a name
# fix the naming of the imported maya camera
# print out a "camera export was a sucsess " if the conditions are me
# create an interface that lets you overide the defualy scale value
# look at maintaining this and future code in a git repository
# use inheratice to have to maya camera and the houdini camera to share the same "export functino" from a place holder export class
# ad exceptions for the camera exports so that it does not fail and gives you a confirmation dialogue
# set the frame range from the database


# Polycat Maya Camera to Houdini Exporter
# 2019

import pymel.core as pm
import os

class MayaCamera():

    def __init__(self):
        self.selection = pm.ls(selection=True)

        if self.selection:
            self.selection = self.selection[0]
            self.shape = self.selection.getShape()
        else:
            print("you have not selected a camera")

    def export_me(self,mayadirname,mayasavename,mayaext):

        # sets the string arguments needed for the ABC export a
        myfile = str("-file " + mayadirname + "/" + mayasavename + "_maya" + mayaext)
        root = str("-root " + str(self.selection))
        myframerange = "-frameRange " + str(start) + " " + str(end)
        exportcommand = myfile + " " + root + " " + myframerange + " " + "-eulerFilter -worldspace"
        pm.AbcExport(j=exportcommand)

    def __str__(self):
        return ("{}".format(self.selection))


class HoudiniCamera():

    def __init__(self):

        self.houdinicam = pm.camera(name=savename)
        self.selection = self.houdinicam[0]
        self.shape = self.selection.getShape()

    def export_me(self, houdirname, housavename, houext):

        # sets the string arguments needed for the ABC export a
        myfile = str("-file " + houdirname + "/" + housavename + "_houdini" + houext)
        root = str("-root " + str(self.selection))
        myframerange = "-frameRange " + str(start) + " " + str(end)
        exportcommand = myfile + " " + root + " " + myframerange + " " + "-eulerFilter -worldspace"
        pm.AbcExport(j=exportcommand)

    def __str__(self):
        return ("{}".format(self.selection))


#SETTING UP THE GLOBAL VARIABLES

start = int(pm.playbackOptions(query=True,min=True))
end = int(pm.playbackOptions(query=True,max=True))
scene_scale = 0.1

#SETTING THE ABC EXPORT STARTING DIRECTORY
def getexportdir():
    scenedir = pm.sceneName()
    dirname = os.path.dirname(scenedir)
    cameradir = os.path.abspath(os.path.join(dirname,"../../0_Camera"))

    if not os.path.exists(cameradir):
        cameradir = "Y:/"

    return cameradir

startdir = getexportdir()

# SETTING THE VARIABLES FOR THE ABC EXPORT
exportfilepath = pm.fileDialog2(fileFilter="*.abc", dialogStyle=2, startingDirectory=startdir)
basename = os.path.basename(exportfilepath[0])
dirname = os.path.dirname(exportfilepath[0])
savename = os.path.splitext(basename)[0]
ext = os.path.splitext(basename)[1]


# SETTING THE OBJECTS
mayacam = MayaCamera()
hdcam = HoudiniCamera()


# EXPORTING THE MAYA CAMERA
if True:
    try:
        mayacam.export_me(dirname,savename,ext)
    except ValueError:
        print ("There was an error exporting the maya camera")

#BAKING ALL THE ATTRIBUTES FOR HOUDINI
for i in range(start,end):

    # updates the time and gets to camera attributes stored in the origcam object
    pm.currentTime(i, edit=True, update=True)

    # unpacks the object attributes into vaiables for readability
    mylens = mayacam.shape.focalLength.get()
    mysensorx = mayacam.shape.horizontalFilmAperture.get()
    mysensory = mayacam.shape.verticalFilmAperture.get()
    mytransx, mytransy, mytransz = pm.xform(mayacam.selection,query=True,ws=True,t=True)
    myrotx, myroty, myrotz = pm.xform(mayacam.selection,query=True,ws=True,ro=True)

    # key the lens
    pm.setKeyframe(hdcam.shape, v=mylens, at="focalLength")
    # key sensor
    pm.setKeyframe(hdcam.shape, v=mysensorx, at="horizontalFilmAperture")
    pm.setKeyframe(hdcam.shape, v=mysensory, at="verticalFilmAperture")
    # key translates and mulitplies it by the scenescale
    pm.setKeyframe(hdcam.selection, v=mytransx * scene_scale, at="translateX")
    pm.setKeyframe(hdcam.selection, v=mytransy * scene_scale, at="translateY")
    pm.setKeyframe(hdcam.selection, v=mytransz * scene_scale, at="translateZ")
    # key rotates - rotation order ZXY
    pm.setKeyframe(hdcam.selection, v=myrotz, at="rotateZ")
    pm.setKeyframe(hdcam.selection, v=myrotx, at="rotateX")
    pm.setKeyframe(hdcam.selection, v=myroty, at="rotateY")


# EXPORT THE ABC FOR HOUDINI AND DELETE THE PLOTTED CAMERA

print(hdcam.selection)

hdcam.export_me(dirname,savename,ext)
pm.delete(hdcam.selection, s=True)

print("CAMERA SCRIPT HAS ENDED")


