import pymel.core as pm

#tests a class UI
import maya.cmds as cmds
from functools import partial

class NewUI(object):
      def __init__(self, name):
          self.name = name   

          #delete existing ui
          if (cmds.window(self.name, q=1, exists=1)):
             cmds.deleteUI(self.name)

          #ui
          self.testWin = cmds.window(self.name, title = self.name, wh = (200, 100))
          self.testCol = cmds.columnLayout()
          self.testFrame = cmds.frameLayout(label = "frame", w=200)
          self.testBtn = cmds.button(label = "< selected")
          self.testTF = cmds.textField(text = "someText")

          #ui commands
          cmds.button(self.testBtn, e=1, command = partial(self.getText))

          #show ui
          cmds.showWindow(self.testWin);

      #change textfield text
      def getText(self, *args):
          cmds.textField(self.testTF, e=1, text= str(cmds.ls(sl=1)[0].split(':')[0]))


# #testScript.py
# import maya.cmds as cmds
# import TestUIClass as ui

# def showUI():
#     #create instance of NewUI
#     myWin = ui.NewUI("myTestWin")

#     myText = cmds.textField(myWin.testTF, q=1, text=1)
#     print(myText)



# def createCameraOptions():

#     winname = "mywin"
#     pm.window(winname,title="Camera Exporter Settings")
#     pm.columnLayout(columnOffset=("both",20),height=100,rowSpacing=10)
#     pm.separator()
#     pm.floatSliderGrp("camscale",label="Camera Scale",parent=winname,field=True,value=0.1,columnAlign=(1,"left"))
#     pm.checkBoxGrp("houdiniexp",label="Export Houdini Camera",value1=True,parent=winname,columnAlign=(1,"left"))
#     pm.checkBoxGrp("mayaexp",label="Export Maya Camera",value1=True,parent=winname,columnAlign=(1,"left"))
#     pm.separator()
#     pm.rowLayout(numberOfColumns=2,width=300,adjustableColumn=1)
#     pm.button("exportme",label="Export",command="pc_ABC_camera_exporter.runCameraExport()")
#     pm.showWindow(winname)  

# class exportCameraUi():
#     def __init__(self):
#         self.winname = "camexportwin"

#         self.buildUi()

#     def buildUi(self):
        
#         pm.window(self.winname,title="Camera Exporter Settings")
#         pm.columnLayout(columnOffset=("both",20),height=100,rowSpacing=10)
#         pm.separator()
#         pm.floatSliderGrp("camscale",label="Camera Scale",field=True,value=0.1,columnAlign=(1,"left"))
#         pm.checkBoxGrp("houdiniexp",label="Export Houdini Camera",value1=True,columnAlign=(1,"left"))
#         pm.checkBoxGrp("mayaexp",label="Export Maya Camera",value1=True,columnAlign=(1,"left"))
#         pm.separator()
#         pm.rowLayout(numberOfColumns=2,width=300,adjustableColumn=1)
#         pm.button("exportme",label="Export",command="pc_ABC_camera_exporter.runCameraExport()")
#         pm.showWindow(self.winname)

#     def getValues(self):



        



       



