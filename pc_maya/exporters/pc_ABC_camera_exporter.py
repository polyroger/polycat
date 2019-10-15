"""
Polycat maya camera exporter 
2019
"""


import os
import pymel.core as pm
from pipeline_utilities import filenaming



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

    
class SelectedCamera():
    def __init__(self):
        try:
            self.camobj = pm.ls(selection=True)
            self.selection = self.camobj[0]
            self.shape = self.selection.getShape()
        except IndexError:
            pm.confirmDialog(m="You have not selected a camera",t="Camera export Error",)
            # raise SystemExit
            exit()
      

# creates a new camera
class RootCamera():

    def __init__(self,name):

        self.rootcam = pm.camera(name=name)
        self.selection = self.rootcam[0]
        self.shape = self.selection.getShape()


    def __str__(self):
        return ("{}".format(self.selection))



# RUNS THE EXPORT
def runCameraExport(scale,frange,houdiniexp,mayaexp,guiobject):
  
    # SETTING THE VARIABLES FOR THE ABC EXPORT
    selectedcam = SelectedCamera()
    path = filenaming.getExportFilePath()
    exportcams = []
    
    
    if path:

        # checking if cam needs to be exported and baking
        if mayaexp:
            rootcam = RootCamera("maya")
            exportcams.append(str(rootcam.selection))#replacing the 1 in the name...find a better way
            print(rootcam.selection + " was added to the exportcams list")
            bakedrootcam = BasicCameraBake(rootcam, selectedcam)
            bakedrootcam.bakeme(frange[0],frange[1],1)
        
        # checking if cam needs to be exported and baking
        if houdiniexp:
            houdinicam = RootCamera("houdini")
            exportcams.append(str(houdinicam.selection))#replacing the 1 in the name....find a better way
            print(houdinicam.selection + " was added to the exportcams list")
            bakedhoudinicam = BasicCameraBake(houdinicam, selectedcam)
            bakedhoudinicam.bakeme(frange[0],frange[1],scale)
        

        # for the object.selection toggle
        camindex = 0

        for app in exportcams:
           
            pathname,dirname = filenaming.buildFileName(app,path)
            
            newDir = os.path.split(pathname)[0]
            
            if not os.path.exists(newDir):
                 os.mkdir(newDir)

            myfile = str("-file " + pathname)
            print(myfile)
            root = str("-root " + str(app))
            myframerange = "-frameRange " + str(frange[0]) + " " + str(frange[1])
            exportcommand = myfile + " " + root + " " + myframerange + " " + "-eulerFilter -worldspace"
            pm.AbcExport(j=exportcommand)


        try: 
            pm.delete(houdinicam.selection)
        except:
            print("There is no need to delete the houdini camera")
        try:
             pm.delete(rootcam.selection)
        except:
            ("There is no need to delete the maya camera")
        
       
        del guiobject
        
                
 

   






