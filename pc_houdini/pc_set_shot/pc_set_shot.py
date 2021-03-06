import hou
import os
import json

import abc_functions as pcabc
from pc_helpers import pc_file_helpers as fhelp


root =  hou.getenv("JOB") + "/"


###### START OF SET SHOT MENU CREATION #####

def menuItems():
      
    client = hou.parm("client").eval()
    project = hou.parm("project").eval()
    level = hou.parm("level").eval()
    scene = hou.parm("scene").eval()      
    cut = hou.parm("cut").eval()    
   
    client_path = root
    project_path = os.path.join(root,client)
    level_path = os.path.join(project_path,project)
    scene_path = os.path.join(level_path,level)
    cut_path = os.path.join(scene_path,scene)
               
    return (client_path,project_path,level_path,scene_path,cut_path)

def createMenu(menu_path):
    
    dirs = os.listdir(menu_path)
    result = []
    for i in dirs:
        result.append(i)
        result.append(i.upper())
        
    return (result)

#setting the menu lists
def createClient():

    client_path,project_path,level_path,scene_path,cut_path = menuItems()
    menu = createMenu(root)
    return menu

def createProject():
    
    client_path,project_path,level_path,scene_path,cut_path = menuItems()
    menu = createMenu(project_path)
    
    return menu
    
def createLevel():
    
    client_path,project_path,level_path,scene_path,cut_path = menuItems()
    menu = createMenu(level_path)
    
    return menu

def createScene():
    
    client_path,project_path,level_path,scene_path,cut_path = menuItems()
    menu = createMenu(scene_path)
    
    return menu  

def createCut():
    
    client_path,project_path,level_path,scene_path,cut_path = menuItems()
    menu = createMenu(cut_path)
    
    return menu

def resetParms():
    
    job = hou.parm("job")
    cut = hou.parm("cut")
    
       
    jobexp = "strcat(strcat(strcat(strcat(chs(\"client\"),\"/\"),strcat(chs(\"project\"),\"/\")),strcat(chs(\"level\"),\"/\")),strcat(chs(\"scene\"),\"/\"))"
    cutexp = "chs(\"shot\")"
        
    job.setExpression(jobexp)
    cut.setExpression(cutexp)

    ##### START OF CAMERA CREATION ######

def cameraSetup(cut,abcnode):
        
    children = abcnode.allSubChildren()
     
    for i in children:
        
        if i.type().name() == "cam":
            
            hcam = i
    
    hcam.setName(cut + "_" + "camera")

    try:
        resx,resy = pcabc.getResolutionFromCamera(abcnode.parm("fileName").eval())
        hcam.parm("resx").set(resx)
        hcam.parm("resy").set(resy)
    except:
        print("there was no resolution attribute set on the alembic file")

    hcam.parm("near").deleteAllKeyframes()
    hcam.parm("near").set(0.001)
    hcam.parm("focus").deleteAllKeyframes()
    hcam.parm("ar_dof_enable").set(1)
    hcam.parm("ar_aperture_size").set(0.005)
    
    parent = hcam.parent()
    focus_null = parent.createNode("null","focus_null")
    focus_null.parm("tz").set(-1)
    expr = "abs(ch(\"../focus_null/tz\"))"
    hcam.parm("focus").setExpression(expr)
    

    return hcam.path()
    
        
def getAbcCamera(node):

    camerapath = node.parm("fullpath").eval() + "/0_camera/houdini/"
    print(camerapath)
    ver = fhelp.getLatestFile(fhelp.listAllFilesInFolder(os.path.realpath(camerapath)))
    print(ver)
    cut = hou.parm("cut").eval()
    
    # print(ver)

    if not ver:
    
        hou.ui.displayConfirmation("There are no pipeline cameras")
        
    else:
        
        filename = os.path.join(camerapath,ver)
        filename = filename.replace("\\\\YARN\projects","$JOB")
        node = hou.node("/obj/")
        alembicCam = node.createNode('alembicarchive',cut + "_camera")
        parameter = alembicCam.parm('fileName')
        parameter.set(filename)
        alembicCam.parm('buildHierarchy').pressButton()
        hou.node(".").parm("camera").set(cameraSetup(cut,alembicCam))
        # sets the color and position of the created camera
        nodecol = (0.28999999165534973, 0.5649999976158142, 0.8859999775886536) #rgb of houdini lighter blue
        bcol = hou.Color(nodecol)
        alembicCam.setColor(bcol)
        campos = [-2.59164, -4.56144]# xy vector for the camera position relative to the pc_scene_start
        posvec = hou.Vector2(campos)
        alembicCam.setPosition(posvec)
    
################ savecfile ################

def runSaveScene():
    
    savedir = hou.parm("fullpath").eval()
    hou.hipFile.setName(savedir)        
    newfilename = hou.ui.selectFile(start_directory=savedir)
    hou.hipFile.save(newfilename)
    
    print(newfilename)
       
############# Frame range from file ##################

RANGETEST = r"C:\Users\Administrator\Documents\0_LOCAL_DEV\pipeline\polycat\sample_files\json\frame_range_sample.json"

def readFrameRangeFromFile(framerangefile):

    cutname = hou.parm("shot").eval()

    try:

        with open(framerangefile) as f:
            jdata = json.load(f)
            start,end = jdata.get(cutname)
            hou.playbar.setFrameRange(int(start),int(end))
            hou.playbar.setPlaybackRange(int(start),int(end))
    except :
        hou.ui.displayConfirmation("There was an error reading the frame range file, Setting range to 1001-1100")
        hou.playbar.setFrameRange(1001,1100)
        hou.playbar.setPlaybackRange(1001,1100)

