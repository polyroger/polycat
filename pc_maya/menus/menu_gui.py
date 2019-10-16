import pymel.core as pm
from pc_maya.exporters import pc_ABC_camera_exporter
from pc_maya.exporters import pc_playblast

class CamExportGui(object):
    def __init__(self,name):
        self.name = name
        
        if pm.window(self.name,q=True,exists=True):
            pm.deleteUI(self.name)
                
        self.window = pm.window(self.name,width=300)
        pm.columnLayout(columnOffset=("both",20),height=100,rowSpacing=10)
        pm.separator()
        self.scale = pm.floatSliderGrp(label="Camera Scale",field=True,value=0.1,columnAlign=(1,"left"))
        self.single = pm.checkBoxGrp(label="Export Single Frame",value1=False,columnAlign=(1,"left"))
        self.houexp = pm.checkBoxGrp(label="Export Houdini Camera",value1=True,columnAlign=(1,"left"))
        self.mayaexp = pm.checkBoxGrp(label="Export Maya Camera",value1=True,columnAlign=(1,"left"))
        self.range = pm.intFieldGrp(numberOfFields=2,label="Frame Range",value1=int(pm.playbackOptions(query=True, min=True)),value2=int(200),columnAlign=(1,"left"))
        pm.separator()
        pm.rowLayout(numberOfColumns=2,width=300,adjustableColumn=1)
        pm.button(label="Export",width=300,command=self.exportCamera)
        pm.showWindow(self.name)
    
    def exportCamera(self,_):
        print("The settings arent supported yet")

        #check for single frame export       
        if self.single.getValue1():
            self.range.setValue1(val=True,value1=int(pm.playbackOptions(query=True, min=True)),value2=int(pm.playbackOptions(query=True, min=True)+int(1)))
        print(self.range.getValue()[0])
        print(self.range.getValue()[1])
        pc_ABC_camera_exporter.runCameraExport(self.scale.getValue(),self.range.getValue(),self.houexp.getValue1(),self.mayaexp.getValue1(),self)
        pm.deleteUI(self.name,window=True)  

class PlayblastCameraGui(object):
    def __init__(self,name):
        self.name = name
        print("Playblast camera init succsess")

        if pm.window(self.name,q=True,exists=True):
            pm.deleteUI(self.name)
                
        self.window = pm.window(self.name,width=300)
        pm.columnLayout(columnOffset=("both",20),height=100,rowSpacing=10)
        pm.separator()
        self.range = pm.intFieldGrp(numberOfFields=2,label="Frame Range",value1=int(pm.playbackOptions(query=True, min=True)),value2=int(200),columnAlign=(1,"left"))
        pm.separator()
        pm.rowLayout(numberOfColumns=2,width=300,adjustableColumn=1)
        pm.button(label="Export",width=300,command=self.runPlayblast)
        pm.showWindow(self.name)

    def runPlayblast(self,_):
        print("this will run the playblast")
        pc_playblast.getEditor() 
        pc_playblast.setBlastSettings()
        pm.playblast(format="image",filename="C:/Users/roger/Documents/maya/projects/default/images/test",compression="jpg",widthHeight=[1920,1080],percent=100)
    
    
    


def initCameraExportGui():
    camgui = CamExportGui("cameraexportgui")

def initPlayblastCameraGui():
    blastgui = PlayblastCameraGui("blastcameragui")

def delGui(guiobject):
    del guiobject
    print("gui object deleted")

    
        

   






