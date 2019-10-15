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
    window = pm.window(width=1280,height=720)
    lay = pm.paneLayout()
    pan = pm.modelPanel()
    pm.modelEditor("mypanel",camera=cam,parent=pan,activeView=True)
    pm.showWindow(window)

def setBlastSettings():
    
    pm.setAttr("hardwareRenderingGlobals.multiSampleEnable",1)

def saveLocation():
    
    startpath = filenaming.getexportdir("playblast")
    print (startpath)
    # savepath = pm.fileDialog2(am=1,ds=2,fm=2,)
 
   
   


  

