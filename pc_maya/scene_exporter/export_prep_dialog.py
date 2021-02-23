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

#polycat imports
from pc_maya.maya_helpers import pc_model_prep


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

        #checkboxes
        self.freezetrans = QtWidgets.QCheckBox("Freeze Transforms")
        # self.freezetrans.setEnabled(True)
        self.delhistory = QtWidgets.QCheckBox("Delete History")
        # self.delhistory.setEnabled(True)
        self.addsuffix = QtWidgets.QCheckBox("ONLY Add Suffix")
        # self.addsuffix.setEnabled(True)
       

        # buttons
        self.go = QtWidgets.QPushButton("GO")
        self.cancel = QtWidgets.QPushButton("Close")

    def createLayout(self):

        #lineedit
        export_prep_lineedit_layout = QtWidgets.QHBoxLayout()
        export_prep_lineedit_layout.addWidget(self.export_prep_name)

        #checkboxes
        checkbox_layout = QtWidgets.QVBoxLayout()
        checkbox_layout.addWidget(self.freezetrans)
        checkbox_layout.addWidget(self.delhistory)
        checkbox_layout.addWidget(self.addsuffix)
      

        #buttons
        export_prep_button_layout = QtWidgets.QHBoxLayout()
        export_prep_button_layout.addStretch()
        export_prep_button_layout.addWidget(self.go)
        export_prep_button_layout.addWidget(self.cancel)

        #mainlayout
        export_prep_main_layout = QtWidgets.QVBoxLayout(self)
        export_prep_main_layout.addLayout(export_prep_lineedit_layout)
        export_prep_main_layout.addLayout(checkbox_layout)
        export_prep_main_layout.addLayout(export_prep_button_layout)

    def createConnections(self):

        self.addsuffix.stateChanged.connect(self.toggleEnabled)     
        self.go.clicked.connect(lambda: pc_model_prep.createStructure(self.addsuffix.isChecked(),self.export_prep_name.text(),self.freezetrans.isChecked(),self.delhistory.isChecked()))
        self.cancel.clicked.connect(self.close)

    #custom methods

    def toggleEnabled(self,state):
        if state:
            self.export_prep_name.setEnabled(False)
            self.freezetrans.setEnabled(False)
            self.delhistory.setEnabled(False)

        else:
            self.export_prep_name.setEnabled(True)
            self.freezetrans.setEnabled(True)
            self.delhistory.setEnabled(True)


            
        


        

    
                
        
        
   
        

    

