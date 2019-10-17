import pymel.core as pm
from pipeline_utilities import filenaming

#setting the render settings


def getEditor():
    """
    The modelEditor is the node in maya that contains all the information about a modelPanel. A panel is an object in maya that acts as the root of a ui element. The model editor
    for instance holds information about what cameras have been added to a panel.
    """
    if pm.modelEditor("mypanel",exists=True):
        print("the panel exists...deleting and creating a new one")
        pm.deleteUI("mypanel") 
    
    cam = pm.ls(selection=True)[0]
    #SETTING CAMERA VIEWPORT SETTINGS
    pm.camera(cam,edit=True,displayResolution=False,displayFilmGate=False)

    window = pm.window(width=1280,height=720,backgroundColor=(1.0,0.0,0.0))
    lay = pm.paneLayout()
    pan = pm.modelPanel()
    pm.modelEditor("mypanel",camera=cam,activeView=True,displayAppearance="smoothShaded")
    pm.showWindow(window,window=True)

def setBlastSettings():
    #these can only be set on global level
    pm.setAttr("hardwareRenderingGlobals.multiSampleEnable",1)
    pm.setAttr("hardwareRenderingGlobals.ssaoEnable",False)


def saveLocation():
    
    startpath = filenaming.getexportdir("playblast")
    exportfilepath = pm.fileDialog2(dialogStyle=2, startingDirectory=startpath,fileMode=3,caption="Select a save location")

    return exportfilepath[0]

def pcBlast(savepath,startf,endf):

    #this runs the actual playblast 
    pm.playblast(format="image",filename=savepath,startTime=startf,endTime=endf,compression="jpg",widthHeight=[1920,1080],percent=100,framePadding=3,showOrnaments=False,viewer=False)
      
 
   
   


  

