# Maya Playblast exporter

# sysyem imports
import os

#pyside2 imports
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

#shiboken imports 
from shiboken2 import wrapInstance

#maya imports
import pymel.core as pm
import maya.OpenMayaUI as omui

#polycat imports
import pc_playblast
from pc_helpers import pc_file_helpers as fhelp
from pc_helpers import pc_path_helpers as phelp

#polycat maya import
from pc_maya.maya_helpers import scene_helpers as shelp


def mayaMainWindow():
    """
    Helper function that returns a python object for maya's main window, so that you can use this python object as the parent for qt widgets 
    in maya.
    """
    mainwindowpointer = omui.MQtUtil.mainWindow()
    mainwindowobject = wrapInstance(long(mainwindowpointer),QtWidgets.QWidget)

    return mainwindowobject

class PcPlayblast(QtWidgets.QDialog):

    FILE_FILTERS = "jpg (*.jpg)"

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
        self.setMinimumSize(600,120)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        # self.cameraSelectionDialog()

        self.rglobals = shelp.getRGlobals()

        self.createWidgets()
        self.createLayouts()
        self.createConnetions()

    def createWidgets(self):

        #export folder name
        self.foldername = QtWidgets.QLineEdit("unnamed")

        #export path
        self.exportpath = QtWidgets.QLineEdit()
        self.exportpath.setText(phelp.goFindFolder(shelp.getScenePath(),"0_playblast"))
        self.exportpath_btn = QtWidgets.QPushButton()
        self.exportpath_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.exportpath_btn.setToolTip("select file")

        #frame range widgetts
        self.frame_range_start = QtWidgets.QLineEdit(str(int(self.rglobals["fstart"])))
        self.frame_range_start.setMaximumWidth(75)
        self.frame_range_end = QtWidgets.QLineEdit(str(int(self.rglobals["fend"])))
        self.frame_range_end.setMaximumWidth(75)


        self.blast_button = QtWidgets.QPushButton("BLAST")
        self.cancel_button = QtWidgets.QPushButton("Cancel")

    def createLayouts(self):

        main_layout = QtWidgets.QVBoxLayout(self)

        #export path layout
        exportpath_layout = QtWidgets.QHBoxLayout()
        exportpath_layout.addWidget(self.exportpath)
        exportpath_layout.addWidget(self.exportpath_btn)


        #frame range
        frame_range_layout = QtWidgets.QHBoxLayout()
        frame_range_layout.addWidget(self.frame_range_start)
        frame_range_layout.addWidget(self.frame_range_end)

        #add in items here
        body_layout = QtWidgets.QFormLayout()
        body_layout.setLabelAlignment(QtCore.Qt.AlignLeft)
        body_layout.setVerticalSpacing(10)
        body_layout.addRow("Export Path :",exportpath_layout)
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
        self.exportpath_btn.clicked.connect(self.setExportFilePath)
        self.blast_button.clicked.connect(self.blastMe)

        self.cancel_button.clicked.connect(self.close)
    
    #Methods

    def setExportFilePath(self):
    
        filepath = QtWidgets.QFileDialog.getSaveFileName(self,"Name your playblast",dir=self.exportpath.text(),filter=self.FILE_FILTERS)

        if filepath[0]:
            self.exportpath.setText(filepath[0])
        
    def blastMe(self):

        g = shelp.getRGlobals()
        blastdir,filename = os.path.split(self.exportpath.text())

        if self.exportpath.text() == phelp.goFindFolder(shelp.getScenePath(),"0_playblast"):
            
            pm.confirmDialog(title="WARNING",message="Please export your playblast into a folder")
            return
        
        try:
            path,name_ext = os.path.split(self.exportpath.text())
            name,ext = os.path.splitext(name_ext)
            print(path,name_ext)
            if not os.path.exists(path):
                print("Creating export directory")
                os.mkdir(path)

            if not name_ext:
                pm.confirmDialog(title="WARNING",message="Please give your playblast a name")
                return
            
            finalname = os.path.splitext(self.exportpath.text())[0]

            print(finalname)
            start = int(self.frame_range_start.text())
            end = int(self.frame_range_end.text())
            
            cam = shelp.getSelectedCamera()
            camshape = cam.getShape()
            
            if not shelp.checkCameraAspect(cam,g):
                return
            
            #re setting globals if changed by the aspect check
            g = shelp.getRGlobals()
            pc_playblast.setTempGlobals()
            
            blast_window = pc_playblast.createPBWindow("blastwindow",camshape)
            pc_playblast.runPlayblast(finalname,start,end,g)
            
            pc_playblast.cleanUp(g,blast_window)

            pm.confirmDialog(title="SUCCESS",message="Done Blasting!")
            self.close()
        except :
            pm.confirmDialog(title="ERROR",message="An Error occured, make sure that a valid export path and filename has been set")

      
       
        
        
