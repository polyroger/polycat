"""
Polycats Houdini previs geometry exporter

"""
import os
import hou
import toolutils

def getSetShot():
    
    obj = hou.node("/obj")

    for node in obj.children():
        if node.type().nameComponents()[2] == "pc_set_shot":
            
            ss = node
            
            return ss

        else:
            hou.ui.displayConfirmation("Could not find the set shot", title="error")
            return None

def getCutName(subnetpath):

    subnet = hou.node(subnetpath)
    
    return subnet.name()


def checkSubnet(root,setshot,subnetname):
    
    if setshot:

        seqpath = setshot.parm("job").eval()
    
        cutlevel = root + seqpath
    
        if subnetname not in os.listdir(cutlevel):

            hou.ui.displayConfirmation("The subnet cut name is not a shot in the sequence",title="ERROR")

            return False

        else:
            return True

    print("there was an errot in the checkSubnet()")
    
    return None

def getRopnet():

    for node in hou.node(".").children():
        if node.name() == "ropnet1":
            abcrop = node.children()[0]
            return abcrop
        else:
            return None


######## START OF FLIPBOOK #######

def getSceneAndViewer():

    scene = toolutils.sceneViewer()
    viewport = scene.curViewport()

    return (scene,viewport)


def cutCameraInSubnet():

    subnet = hou.node("../")

    for node in subnet.children():
    
        if node.type().name() == "cam":
            return node


def setCameraToSceneView(viewport,camera):

    try:
        viewport.setCamera(camera)
        return True
    except:
        print("error setting camera to viewport")
        return False

def setFlipbookSettings(scene,camera):

    fbsettings = scene.flipbookSettings().stash()

    fstart = hou.parm("frame_rangemin").eval()
    fend = hou.parm("frame_rangemax").eval()

    resolution = (camera.parm("resx").eval(),camera.parm("resy").eval())

    res = {"camera":"camera",
            "75":(int(round(resolution[0] * 0.75)),int(round(resolution[1] * 0.75))),
            "50":(int(round(resolution[0] * 0.5)),int(round(resolution[1] * 0.5))),
            "25":(int(round(resolution[0] * 0.25)),int(round(resolution[1] * 0.25)))}
        
    
    if not hou.parm("resolution").eval() == "camera":
    
        resolution = res[hou.parm("resolution").eval()]


    fbsettings.resolution(resolution)
    fbsettings.output(hou.parm("export_path").eval())
    fbsettings.frameRange((hou.parm("frame_rangemin").eval(),hou.parm("frame_rangemax").eval()))
    fbsettings.beautyPassOnly(True)
    fbsettings.antialias(hou.flipbookAntialias.HighQuality)

    
    return fbsettings

def setFlipbookOutput(setshot):
    
    cutlevel = setshot.parm("job").eval()
    cutname = getCutName(hou.node("..").path())
    version = hou.parm("version").eval()
    output = "//YARN/projects/" + cutlevel + cutname + "/0_playblast/" + version + "/" + cutname + "_" + "previs" + "_" + version + ".$F4.jpg"

    return output




