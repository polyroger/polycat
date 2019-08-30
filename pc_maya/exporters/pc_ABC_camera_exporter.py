"""
Polycat maya camera exporter 
2019
"""


import os
import pymel.core as pm


class BasicCameraBake():

    def __init__(self,camtobake,camtoget):
        self.camtobake = camtobake
        self.camtoget = camtoget


    def bakeme(self,start,end,scene_scale):
        for i in range(start, end + 1,):
            # updates the time and gets to camera attributes stored in the origcam object
            pm.currentTime(i, edit=True, update=True)

            # unpacks the object attributes into vaiables for readability
            mylens = self.camtoget.shape.focalLength.get()
            mysensorx = self.camtoget.shape.horizontalFilmAperture.get()
            mysensory = self.camtoget.shape.verticalFilmAperture.get()
            mytransx, mytransy, mytransz = pm.xform(self.camtoget.selection, query=True, ws=True, t=True)
            myrotx, myroty, myrotz = pm.xform(self.camtoget.selection, query=True, ws=True, ro=True)

            # key the lens
            pm.setKeyframe(self.camtobake.shape, v=mylens, at="focalLength")
            # key sensor
            pm.setKeyframe(self.camtobake.shape, v=mysensorx, at="horizontalFilmAperture")
            pm.setKeyframe(self.camtobake.shape, v=mysensory, at="verticalFilmAperture")
            # key translates and mulitplies it by the scenescale
            pm.setKeyframe(self.camtobake.selection, v=mytransx * scene_scale, at="translateX")
            pm.setKeyframe(self.camtobake.selection, v=mytransy * scene_scale, at="translateY")
            pm.setKeyframe(self.camtobake.selection, v=mytransz * scene_scale, at="translateZ")
            # key rotates - rotation order ZXY
            pm.setKeyframe(self.camtobake.selection, v=myrotz, at="rotateZ")
            pm.setKeyframe(self.camtobake.selection, v=myrotx, at="rotateX")
            pm.setKeyframe(self.camtobake.selection, v=myroty, at="rotateY")


class GetSceneSettings():
    def __init__(self,scene_scale=float(1.0)):
        self.start =  int(pm.playbackOptions(query=True, min=True))
        self.end = int(pm.playbackOptions(query=True, max=True))
        self.scene_scale = scene_scale

    @classmethod
    def test(cls):
        print("this is a class method")

class SelectedCamera():
    def __init__(self):
        self.camobj = pm.ls(selection=True)
        self.selection = self.camobj[0]
        self.shape = self.selection.getShape()

class RootCamera():

    def __init__(self,name):

        self.rootcam = pm.camera(name=name)
        self.selection = self.rootcam[0]
        self.shape = self.selection.getShape()


    def __str__(self):
        return ("{}".format(self.selection))


# RUNS THE EXPORT
def runCameraExport():

    # SETTING THE VARIABLES FOR THE ABC EXPORT
    exportfilepath = pm.fileDialog2(fileFilter="*.abc", dialogStyle=2, startingDirectory="Y:/")
    if exportfilepath:
        
        basename = os.path.basename(exportfilepath[0])
        dirname = os.path.dirname(exportfilepath[0])
        savename = os.path.splitext(basename)[0]
        ext = os.path.splitext(basename)[1]

        scene_settings = GetSceneSettings(0.1)
        selectedcam = SelectedCamera()
        rootcam = RootCamera("maya")
        houdinicam = RootCamera("houdini")

       
        # BAKES
        bakedrootcam = BasicCameraBake(rootcam, selectedcam)
        bakedhoudinicam = BasicCameraBake(houdinicam, rootcam)

        bakedrootcam.bakeme(scene_settings.start,scene_settings.end,1)
        bakedhoudinicam.bakeme(scene_settings.start,scene_settings.end,0.1)
           

        myfile = str("-file " + dirname + "/" + savename + "_houdini" + ext)
        root = str("-root " + str(houdinicam.selection))
        myframerange = "-frameRange " + str(scene_settings.start) + " " + str(scene_settings.end)
        exportcommand = myfile + " " + root + " " + myframerange + " " + "-eulerFilter -worldspace"
        pm.AbcExport(j=exportcommand)

        print (houdinicam.selection)
        print (rootcam.selection)
        print (exportcommand)
        
        
        
        # from alembic_helper import maya_alembic_helper
        # reload(maya_alembic_helper)
        # for s in ["maya", "houdini"]:
        #     newDir = os.path.join(dirname, s)
        #     if os.path.exists(newDir) is False:
        #         os.mkdir(newDir)
        #     a = maya_alembic_helper.Helper()
        #     a.set_alembic_node(houdinicam.selection)
        #     a.set_alembic_output(os.path.join(newDir, "{}{}".format(savename, ext)))
        #     a.set_alembic_command(["-frameRange 1 120"])
        #     a.export_alembic()
