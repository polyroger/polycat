import os
import hou
 

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
    
def resetParms():
    
    job = hou.parm("job")
    cut = hou.parm("cut")
    
    jobexp = "strcat(strcat(chs(\"client\"),\"/\"),chs(\"project\"))"
    cutexp = "chs(\"shot\")"
        
    job.setExpression(jobexp)
    cut.setExpression(cutexp)   
    
    
###############################     CAMERA            ########################

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
    
    parent = hcam.parent()
    focus_null = parent.createNode("null","focus_null")
    expr = "abs(ch(\"../focus_null/tz\"))"
    hcam.parm("focus").setExpression(expr)
    
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
    
###############################     SAVE SCENE           ########################
# check if the path is valid, if not in a houdini folder cancel
# check if there is a hip file in the path,
# if there is a hip file get the list of files
# saveandincrementfilname

# if not filelist:
#     prompt for save name with open text dialouge
#     check for name conflict
#     save file


def checkValidHipDir(hippath):

    if os.path.exists(hippath):

        filegroup = []
        for f in os.listdir(hippath):
            if os.path.isfile(hippath + "/" + f):
                filegroup.append(f)

        return filegroup

        
    else:
        print "no"
        return False
   

def showHipFiles(filelist):

    return hou.ui.selectFromList(filelist,exclusive=True,message="If you want to version up a current hip file select one from the list")[0]



    # """
    # Takes a file path as an argumnet and checks if that path is a valid polycat hip file save location

    # """
    # print "running"

    # if os.path.split(hippath[:-1])[1] == "houdini" or os.path.exists(hippath):

    #     hou.ui.displayConfirmation("there is a valid `houdini` folder in this save path")
    #     return True
    # else:

    #     hou.ui.displayConfirmation("There is not a `houdini` folder in this save path")
        
    #     return False 
        
    # print "done"





    
    


