import pymel.core as pm

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

def getSelectedCamera():

    cam = pm.ls(selection=True)[0]
    camshape = cam.getShape()
    
    if pm.nodeType(camshape) != "camera":
        return None

    return camshape

def checkRenderSettings(camerashape,rglobals):
    camaspect = round(camerashape.getAspectRatio(),2)
    globalaspect = rglobals["aspect"]

    if camaspect != globalaspect:
        print("The camera aspect ({0}) and the render aspect ({1}) do not match".format(camaspect,globalaspect))
        return False

    print("all good")
    return True


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
    
    pm.showWindow(pbwindow)
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

#test run
# savepath = "C:\\Users\\Administrator\\Documents\\0_LOCAL_DEV\\pipeline\\polycat\\sample_files\\playblast\\blast2.png"
# camera = getSelectedCamera()
# renderglobals = getRGlobals()
# rendercheck = checkRenderSettings(camera,renderglobals)
# setTempGlobals()
# pbwindow = createPBWindow("pbwindow",camera)
# runPlayblast(savepath,1001,1100,renderglobals)
# cleanUp(renderglobals,pbwindow)



"""
WHITEBOARD

the gui needs to set options for the defaultRenderGlobals and the defaultRenderingGlobals
    -   resolution
    -   sampling
as well as the model editor
    -   shading mode
    -   show textures

Needs to save the current hardware settings before they get changes so they can be set back to defaults after the playblast has ended

The tool needs to be easiily sent off when packaging up shots.

Should default to the shots playblast folder. Version up in the tag is the same or create a new folder if the tag is unique. 

the camera aspect and the render aspect should match

have a global size multiplyer


"""