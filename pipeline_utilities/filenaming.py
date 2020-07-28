import os
import re
import pymel.core as pm



# all this belew is what I am calling legacy from the first camera exporter. It works but needs to be updated to better practices

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
    # !!THIS IS A LITTLE DODGY AS IT IS NOT LOOKING FOR FILES NAMED A CERTAIN WAY SO IF THERE ARE OTHER FOLDERS IN THE CAMERA FOLDER THEN THE WALK WILL FIND THOSE
    #AND TRY USING THEM. YOU WILL MOSTLIKELY GET AN ERROR REGARDING THE GROUP() REGEX METHOD.

    app_versions = {"maya":int(1),"houdini":int(1),"nuke":int(1)}
    for root,dirs,files in os.walk(camerapath):
        for folder in dirs:
           
            mypath = os.path.join(camerapath,folder).replace("\\","/")
            print(mypath)
            
            for root,dirs,files in os.walk(mypath):
                
                files.sort()
                # temp = files
                if files:
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

    print exportfilepath[0]    
    return exportfilepath[0]

def buildFileName(app,exportfilepath):

    app = str(app).replace("1","")    
    dirname = os.path.dirname(exportfilepath)
    ext = ".abc"
    camera = "_camera_"
    latest_version = getVersion(exportfilepath)
    cut = os.path.basename(dirname)
    print (app)
    pathname = exportfilepath +"/"+ app + "/" + cut + camera + "v" + str(latest_version[app]).zfill(3) + ext
    return (pathname,dirname)




