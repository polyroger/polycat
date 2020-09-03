"""
The polycat playblast camera backend
"""

#maya imports
import pymel.core as pm


def setTempGlobals():

    pm.setAttr("hardwareRenderingGlobals.multiSampleEnable",1)
    pm.setAttr("hardwareRenderingGlobals.aasc",16)
    pm.displayRGBColor("background",0.2,0.2,0.2)

    return "Temporarily set global settings"


def createPBWindow(windowname,camera):
    
    if pm.window(windowname,exists=True):
        pm.deleteUI(windowname)

    pbwindow = pm.window(windowname)
    pm.paneLayout()
    blastpanel = pm.modelPanel(label="blast_panel")
    
    pm.modelEditor( modelPanel=blastpanel,
                    camera=camera.name(),
                    cameras=False,
                    grid=False,
                    hud=False,
                    ipz=True,
                    displayTextures=True,
                    lights=False,
                    joints=False,
                    locators=False,
                    nurbsCurves=False,
                    displayAppearance="smoothShaded")
    
    # pbwindow.show()
    pm.setFocus(blastpanel)

    return windowname

def runPlayblast(savepath,start,end,rglobals):

    try:
        pm.playblast(   format="image",
                        filename=savepath,
                        startTime=start,
                        endTime=end,
                        compression="jpg",
                        percent=100,
                        framePadding=3,
                        showOrnaments=False,
                        viewer=False,
                        width=rglobals["resx"],
                        height=rglobals["resy"])
        
        print("Playblast completed")
        return True
    
    except :
        
        print("There was an error rendering the playblast")
        return False


def cleanUp(rglobals,windowname):
    
    pm.deleteUI(windowname)
    pm.displayRGBColor("background",float(rglobals["bgrgb"][0]),float(rglobals["bgrgb"][1]),float(rglobals["bgrgb"][2]))
    pm.setAttr("hardwareRenderingGlobals.multiSampleEnable",0)
    pm.setAttr("hardwareRenderingGlobals.aasc",8)

    return "Done with clean up"    

