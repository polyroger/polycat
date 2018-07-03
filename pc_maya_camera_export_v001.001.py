#still to do :
#create variables for all the names and figure out how to store objects in a variable so that you dont explicitly call the name - kinda done
#fix the out of rannge error if there is nothing selected - done
#make it so that if anything other that a camera is selected the script doesnt execute - done
#make sure that the abc plugin is loaded - done
#allow for selection of multiple cameras

#create a gui to set some paramaters like the export scale.


import maya.cmds as cdms
import os
import sys 

#checks that somthing has been selected and if that thing is a camera object

myselection = cmds.ls(selection=True)

if len(myselection) == 0:
    cmds.confirmDialog(title="warning",message="please first select a camera",button = "continue")
    sys.exit()
    
selectionshape = cmds.listRelatives(myselection,shapes=True)
selectiontype =  cmds.objectType(selectionshape[0])

if selectiontype != "camera":
    cmds.confirmDialog(title="warning",message="you have not selected a camera, please select a camera object",button = "continue")
    sys.exit()
    

#starts off with the abc dialog
basicfilter = "*.abc"
exportfilepath = cmds.fileDialog2(fileFilter = basicfilter, dialogStyle = 2, fileMode = 0)
basename = os.path.basename(exportfilepath[0])
(savename,ext) = os.path.splitext(basename)


#variables 
mycamera = str("mycamera")
myscale = float(0.1)
start = int(cmds.playbackOptions(q=True,min=True))
end = int(cmds.playbackOptions(q=True,max=True))


#sets the current time to the beginning of the export range
cmds.currentTime(start)

#duplicate and unparent the selected camera
cmds.duplicate(myselection[0],n=mycamera)
hasparent = bool(cmds.listRelatives(mycamera, parent=True))

if hasparent != 0:
    cmds.parent(mycamera,w=True)


#create the final camera for export
cmds.duplicate(myselection[0],n=savename)
hasparent = bool(cmds.listRelatives(savename, parent=True))

if hasparent != 0:
    cmds.parent(savename,w=True)

cmds.setAttr(savename + ".scaleX",1)    
cmds.setAttr(savename + ".scaleY",1)
cmds.setAttr(savename + ".scaleZ",1)

#create constraint and bake
cmds.parentConstraint(myselection[0],mycamera)
cmds.bakeResults(mycamera,simulation = True,disableImplicitControl = True,time = (start,end))
mycameracons = cmds.listConnections(mycamera,type="constraint")
cmds.delete(mycameracons)

# Create group, parent and scale
cmds.group(name = "mycamera_srt",empty=True)
cmds.parent(mycamera,"mycamera_srt")
cmds.setAttr("mycamera_srt.scaleX",myscale)    
cmds.setAttr("mycamera_srt.scaleY",myscale)
cmds.setAttr("mycamera_srt.scaleZ",myscale)



cmds.parentConstraint(mycamera,savename)
cmds.bakeResults(savename,simulation = True,disableImplicitControl = True,time = (start,end))
exportcameracons = cmds.listConnections(mycamera,type="constraint")
cmds.delete(exportcameracons)


#Start of the export code
if cmds.pluginInfo('AbcExport.so', query=True, loaded=True) is False:
    cmds.loadPlugin("AbcExport.so")
if cmds.pluginInfo('AbcImport.so', query=True, loaded=True) is False:
    cmds.loadPlugin("AbcImport.so")


#setting the flag values for the export command
start = str(start)
end = str(end)

myfile = str("-file " + exportfilepath[0])
root = str("-root " + savename)
myframerange = "-frameRange " + start + " " + end

#sets the export command
exportcommand = myfile + " " + root + " " + myframerange + " " + "-eulerFilter -worlspace"

#writes the file
cmds.AbcExport( j = exportcommand ) 

#delet all the extra stuff

cmds.delete("mycamera_srt")



