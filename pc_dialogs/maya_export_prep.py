# 
# Procedure for preparing models for export from maya
# 
#pyside2 imports
from PySide2 import QtWidgets
from PySide2 import QtCore

#shiboken imports 
from shiboken2 import wrapInstance

#maya imports
import pymel.core as pm
import maya.OpenMayaUI as omui

def mayaMainWindow():
    """
    Helper function that returns a python object for maya's main window, so that you can use this python object as the parent for qt widgets 
    in maya.
    """
    mainwindowpointer = omui.MQtUtil.mainWindow()
    mainwindowobject = wrapInstance(long(mainwindowpointer),QtWidgets.QWidget)

    return mainwindowobject

class NameGGRP(QtWidgets.QDialog):

    nameGGRP_dialog = None

    @classmethod
    def openNameGGRP_dialog(cls):
        
        if not cls.nameGGRP_dialog:

            cls.nameGGRP_dialog = NameGGRP()
            cls.nameGGRP_dialog.show()
        
        if cls.nameGGRP_dialog.isHidden():
            cls.nameGGRP_dialog.show()

        else:
            cls.nameGGRP_dialog.raise_()
            cls.nameGGRP_dialog.activateWindow()
            

    def __init__(self,parent=mayaMainWindow()):
        super(NameGGRP,self).__init__(parent)

        self.setWindowTitle("Prep for export")
        self.setMinimumSize(300,120)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.createWidgets()
        self.createLayout()
        self.createConnections()

    
    
    def createWidgets(self):
        
        #lineedit
        self.export_prep_name = QtWidgets.QLineEdit("Unnamed")

        # buttons
        self.go = QtWidgets.QPushButton("GO")
        self.cancel = QtWidgets.QPushButton("Close")

    def createLayout(self):

        #lineedit
        export_prep_lineedit_layout = QtWidgets.QHBoxLayout()
        export_prep_lineedit_layout.addWidget(self.export_prep_name)

        #buttons
        export_prep_button_layout = QtWidgets.QHBoxLayout()
        export_prep_button_layout.addStretch()
        export_prep_button_layout.addWidget(self.go)
        export_prep_button_layout.addWidget(self.cancel)

        #mainlayout
        export_prep_main_layout = QtWidgets.QVBoxLayout(self)
        export_prep_main_layout.addLayout(export_prep_lineedit_layout)
        export_prep_main_layout.addLayout(export_prep_button_layout)

    def createConnections(self):
        
        self.go.clicked.connect(self.createStructure)
        self.cancel.clicked.connect(self.close)


    def createStructure(self):
        
        namesuffix = "_GGRP"
        transname = "SRT"
        geosuffix = "_geo"

        selectedgeo = pm.ls(selection=True)
        groupname = self.export_prep_name.text() + namesuffix

        transgroup = pm.group(empty=True,world=True,n=transname)

        for i in selectedgeo:
            if not "_geo" in i.name():

                i.rename(i.name() + geosuffix)
                print(i.name())
         
            pm.parent(i,transgroup)

        asset = pm.group(empty=True,world=True,n=groupname)
        pm.parent(transgroup,asset)
        
        


        

    

