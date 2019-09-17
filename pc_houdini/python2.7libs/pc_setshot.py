import hou
import os

root =  hou.getenv("JOB") + "/"

def createMenu(menu_path):
    
    dirs = os.listdir(menu_path)
    result = []
    for i in dirs:
        result.append(i)
        result.append(i.upper())
        
    return (result)
    
    
def menuItems():
      
    client = hou.parm("client").eval()
    project = hou.parm("project").eval()
    cut = hou.parm("cut").eval()    
   
    client_path = root
    project_path = os.path.join(root,client)
    cut_path = os.path.join(project_path,project)
               
    return (client_path,project_path,cut_path)

def getMenuItems(category):
    items = os.listdir(category)
    return items


# Creating the menus    
def createClient():
    client_path,project_path,cut_path = menuItems()
    menu = createMenu(root)
    return menu

def createProject():
    client_path,project_path,cut_path = menuItems()
    menu = createMenu(project_path)
    return menu

def createCut():
    client_path,project_path,cut_path = menuItems()
    menu = createMenu(cut_path)
    return menu    

def resolvedJobPath():
    path = menuItems[2]
    
    return hou.parm("job").set("test")
    
########################

def getlatest(path):
    for root,folder,files in os.walk(path):
        files.sort()
        latest = files.pop()
        
        return latest

def cameraSetup(cut,abcnode):
   
    children = abcnode.allSubChildren()
    
    resx,resy = (1920,1080)
    
    
    for i in children:
        if i.type().name() == "cam":
            hcam = i
    hcam.setName(cut + "_" + "camera")
    hcam.parm("resx").set(resx)
    hcam.parm("resy").set(resy)
    #hcam.parm("near").deleteAllKeyframes()
    hcam.parm("near").set(0.001)
    hcam.parm("focus").deleteAllKeyframes()
    hcam.parm("ar_dof_enable").set(1)
    hcam.parm("ar_aperture_size").set(0.005)
    
    return hcam.path()
   
   
        
def getAbcCamera():
        
    setshot = hou.node(".")
    
    #root = "Y:/"
    job = setshot.parm("job").eval()
    cut = setshot.parm("cut").eval()
    cutpath = "/0_Camera/houdini/" 
       
    camerapath = root + job + "/" + cut + cutpath
    ver = getlatest(camerapath)
    
    filename = camerapath + ver
    
    print ver
   
    node = hou.node("/obj/")
    alembicCam = node.createNode('alembicarchive',cut + "_camera")
    parameter = alembicCam.parm('fileName')
    parameter.set(filename)
    alembicCam.parm('buildHierarchy').pressButton()
    
    setshot.parm("camera").set(cameraSetup(cut,alembicCam))
    
    
    
    


