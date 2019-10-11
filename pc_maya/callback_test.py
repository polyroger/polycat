import pymel.core as pm
from pc_maya.exporters import pc_ABC_camera_exporter
from functools import partial

class MyGui(object):
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
        pc_ABC_camera_exporter.runCameraExport(self.scale.getValue())  

    def getSettings(self,*args):
        pass

def initGui():
    gui = MyGui("cameraexportgui")

    
        

   






