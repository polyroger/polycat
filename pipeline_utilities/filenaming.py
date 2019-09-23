import os
import re
import pymel.core as pm

def getexportdir(asset):
    # this is a tempory way to idetify folders, find a better way. Maybe a global json file that gives you relative paths
    relpaths = {"cam":"../../","playblast":"../../0_Playblast"}
    scenedir = pm.sceneName()
    if scenedir.startswith("Y:"):
        dirname = os.path.dirname(scenedir)
        cameradir = os.path.abspath(os.path.join(dirname,relpaths[asset]))
    else:
        cameradir = "Y:/"

    return cameradir

def getVersion(camerapath):

    app_versions = {"maya":int(1),"houdini":int(1),"nuke":int(1)}
    for root,dirs,files in os.walk(camerapath):
        for folder in dirs:
           
            mypath = os.path.join(camerapath,folder).replace("\\","/")
            
            for root,dirs,files in os.walk(mypath):
                files.sort()
                temp = files
                if temp:
                    for file in files:
                        noext = os.path.splitext(file)[0]
                        # this regex looks for numbers matching 0-9 only at the end of a filenam. The extension is stripped to make it easier.
                        latest = re.search(r"\d[0-9]$",noext).group()
                        latest_plus = int(latest) + int(1)
                else:
                    print("there were no files in the {} folder...creating version 001".format(folder))
                    latest_plus = int(1)
                app_versions[folder] = latest_plus   
               
    return app_versions                        

def getExportFilePath():
    exportfilepath = pm.fileDialog2(fileFilter=".nothing", dialogStyle=2, startingDirectory=getexportdir("cam"),fileMode=3,caption="Select the camera folder")
    if os.path.basename(exportfilepath[0].lower()) != "0_camera":
        pm.confirmDialog(m="You have not selected a pipeline camera folder\nPlease select the 0_Camera folder in a cut",t="Camera export Error",)
        exit()
    else:
        print("File path correctly set")
        
    return exportfilepath[0]


def buildFileName(app,exportfilepath):
        
    dirname = os.path.dirname(exportfilepath)
    ext = ".abc"
    camera = "_camera_"
    latest_version = getVersion(exportfilepath)
    cut = os.path.basename(dirname)

    pathname = exportfilepath +"/"+ app + "/" + cut + camera + "v" + str(latest_version[app]).zfill(3) + ext
 
    return (pathname,dirname)


# need to find the file with the highest version
# add in a better regex to get any numbered version, currently its only getting two platces , 1 - 99 addin int two /d seemed to do it but i think that its incorrect            

