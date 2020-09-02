# 
# Maya Playblast exporter
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
import pc_playblast


def mayaMainWindow():
    """
    Helper function that returns a python object for maya's main window, so that you can use this python object as the parent for qt widgets 
    in maya.
    """
    mainwindowpointer = omui.MQtUtil.mainWindow()
    mainwindowobject = wrapInstance(long(mainwindowpointer),QtWidgets.QWidget)

    return mainwindowobject

class PcPlayblast(QtWidgets.QDialog):

    pcplayblast_dialog = None

    @classmethod
    def openPcPlayblast_dialog(cls):
        
        if not cls.pcplayblast_dialog:

            cls.pcplayblast_dialog = PcPlayblast()
            cls.pcplayblast_dialog.show()
        
        if cls.pcplayblast_dialog.isHidden():
            cls.pcplayblast_dialog.show()

        else:
            cls.pcplayblast_dialog.raise_()
            cls.pcplayblast_dialog.activateWindow()
            

    def __init__(self,parent=mayaMainWindow()):
        super(PcPlayblast,self).__init__(parent)
        
        self.setWindowTitle("Polycat Playblast")
        self.setMinimumSize(300,120)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.camera_selection_dialog()

        self.rglobals = pc_playblast.getRGlobals()

        self.createWidgets()
        self.createLayouts()
        self.createConnetions()

    def createWidgets(self):
        #export path
        self.exportpath = QtWidgets.QLineEdit("autofill the path")

        #frame range widgetts
        self.frame_range_start = QtWidgets.QLineEdit(str(int(self.rglobals["fstart"])))
        self.frame_range_start.setMaximumWidth(75)
        self.frame_range_end = QtWidgets.QLineEdit(str(int(self.rglobals["fend"])))
        self.frame_range_end.setMaximumWidth(75)


        self.blast_button = QtWidgets.QPushButton("BLAST")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

    def createLayouts(self):

        main_layout = QtWidgets.QVBoxLayout(self)

        #frame range
        frame_range_layout = QtWidgets.QHBoxLayout()
        frame_range_layout.addWidget(self.frame_range_start)
        frame_range_layout.addWidget(self.frame_range_end)

        #add in items here
        body_layout = QtWidgets.QFormLayout()
        body_layout.setLabelAlignment(QtCore.Qt.AlignLeft)
        body_layout.setVerticalSpacing(10)
        body_layout.addRow("Export Path :",self.exportpath)
        body_layout.addRow("Frame Range :",frame_range_layout)
  
        #Ok Cancel buttons
        button_layout = QtWidgets.QHBoxLayout(self)
        button_layout.addStretch()
        button_layout.addWidget(self.blast_button)
        button_layout.addWidget(self.cancel_button)

        #adding it all to the main layout
        main_layout.addLayout(body_layout)
        main_layout.addLayout(button_layout)
    
    
    def createConnetions(self):
        pass
    
    #Custom UI

    def cameraSelectionDialog(self):

        self.camera_selection_dialog = QtWidgets.QMessageBox(self,"Select Camera")
        self.camera_selection_dialog.addButton("Ok",QtWidgets.QMessageBox.AcceptRole)
        self.camera_selection_dialog.addButton("Cancel",QtWidgets.QMessageBox.RejectRole)


        