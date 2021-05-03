"""
Polcat camera exporter ui
"""
#system
import os

#pyside2 imports    
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

#maya imports
import pymel.core as pm

#Camera exporter
from pc_maya.camera_exporter import pc_camera_exporter as camex
# import pc_camera_exporter as camex

#pipeline helpers
from pc_helpers import pc_path_helpers as phelp
from pc_helpers import pc_file_helpers as fhelp

#maya helpers
from pc_maya.maya_helpers import export_helpers as exhelp
from pc_maya.maya_helpers import scene_helpers as shelp
from pc_maya.maya_helpers import pyside2_helpers as py2help

class CameraExporter(QtWidgets.QDialog):

    cameraExportDialog = None

    @classmethod
    def openCameraExportDialog(cls):

        if not cls.cameraExportDialog:
    
            cls.cameraExportDialog = CameraExporter()
            cls.cameraExportDialog.show()
        
        if cls.cameraExportDialog.isHidden():
            cls.cameraExportDialog.show()

        else:
            cls.cameraExportDialog.raise_()
            cls.cameraExportDialog.activateWindow()


    def __init__(self,parent=py2help.mayaMainWindow()):
        super(CameraExporter,self).__init__(parent)

        self.setWindowTitle("Export Camera")
        self.setMinimumSize(600,150)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.createWidgets()
        self.createLayout()
        self.createConnections()


    def createWidgets(self):

        #export path widgets
        self.export_path = QtWidgets.QLineEdit()
        self.export_path.setText(self.getExportPath())
        self.export_path_btn = QtWidgets.QPushButton()
        self.export_path_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.export_path_btn.setToolTip("select file")        
        
        #checkboxes
        self.singleframe = QtWidgets.QCheckBox()
        self.openFolder = QtWidgets.QCheckBox()
        
        #frame range widgetts
        self.frame_range_start = QtWidgets.QLineEdit(str(int(pm.playbackOptions(q=True,minTime=True))))
        self.frame_range_start.setMaximumWidth(75)
        self.frame_range_end = QtWidgets.QLineEdit(str(int(pm.playbackOptions(q=True,maxTime=True))))
        self.frame_range_end.setMaximumWidth(75)
        self.frame_step = QtWidgets.QLineEdit("1.0")
        self.frame_step.setToolTip("less is more samples : (1/step) 1 / 0.1 = 10 subframes")  
        self.frame_step.setMaximumWidth(35)        

        intvalidator = QtGui.QIntValidator(-99999,99999,self)
        self.frame_range_start.setValidator(intvalidator)
        self.frame_range_end.setValidator(intvalidator)

        #button widgets
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.export_btn = QtWidgets.QPushButton("Export")


    def createLayout(self):

        main_layout = QtWidgets.QVBoxLayout(self)
        
        filepath_layout = QtWidgets.QHBoxLayout(self)
        filepath_layout.addWidget(self.export_path)
        filepath_layout.addWidget(self.export_path_btn)
        
        checkbox_sf_layout = QtWidgets.QVBoxLayout(self)
        checkbox_sf_layout.addWidget(self.singleframe)
        
        checkbox_of_layout = QtWidgets.QVBoxLayout(self)
        checkbox_of_layout.addWidget(self.openFolder)

        frame_range_layout = QtWidgets.QHBoxLayout(self)
        frame_range_layout.addWidget(self.frame_range_start)
        frame_range_layout.addWidget(self.frame_range_end)
        frame_range_layout.addWidget(self.frame_step)
    
        body_layout = QtWidgets.QFormLayout(self)
        body_layout.setVerticalSpacing(10)
        body_layout.setLabelAlignment(QtCore.Qt.AlignLeft)
        body_layout.addRow("Export Path : ",filepath_layout)
        body_layout.addRow("Single Frame : ",checkbox_sf_layout)
        body_layout.addRow("Open file dialog : ",checkbox_of_layout)
        body_layout.addRow("Frame Range : ",frame_range_layout)

        button_layout = QtWidgets.QHBoxLayout(self)
        button_layout.addStretch()
        button_layout.addWidget(self.export_btn)
        button_layout.addWidget(self.cancel_btn)


        main_layout.addLayout(body_layout)
        main_layout.addLayout(button_layout)
     

    def createConnections(self):
        
        self.export_path_btn.clicked.connect(self.selectCameraDir)
        self.export_btn.clicked.connect(self.runAbcExport)
        self.cancel_btn.clicked.connect(self.close)
        self.singleframe.stateChanged.connect(self.toggleFrameRange)
    
    ##############################

    def toggleFrameRange(self,state):

        if state:
            self.frame_range_start.setText("1001")       
            self.frame_range_start.setEnabled(False)
            self.frame_range_end.setText("1001")
            self.frame_range_end.setEnabled(False)
            self.frame_step.setText("1.0")
            self.frame_step.setEnabled(False)        
        else:
            self.frame_range_start.setEnabled(True)
            self.frame_range_start.setText(str(int(pm.playbackOptions(q=True,minTime=True))))
            self.frame_range_end.setEnabled(True)
            self.frame_range_end.setText(str(int(pm.playbackOptions(q=True,maxTime=True))))
            self.frame_step.setEnabled(True)
    
    
    def getExportPath(self):
        
        cameradir = "0_camera"
        export_label_path = phelp.goFindFolder(shelp.getScenePath(),cameradir)

        return export_label_path

    def selectCameraDir(self):
        
        cameradir = QtWidgets.QFileDialog.getExistingDirectory(self,"Select a '0_camera` folder",dir=self.export_path.text())
        
        if cameradir:
            self.export_path.setText(cameradir)

    def runAbcExport(self):

        if not shelp.getSelectedCamera():
            return
        else:
            selectedcam = shelp.getSelectedCamera()
        
        #get the globals, change them if need be
        mglobals = shelp.getRGlobals()
        
        if not shelp.checkCameraAspect(selectedcam,mglobals):
            return
        
        #update the global dict 
        mglobals = shelp.getRGlobals()

        applist = [("maya","maya_camera",1),("houdini","houdini_camera",.1)]
        attrlist = ["resx","resy"]

        ui_path = self.export_path.text()
        if not str(ui_path).endswith("0_camera"):
            pm.confirmDialog(title="WARNING",message="Please select a valid camera folder [ 0_camera ]")
            return None
        
        pm.refresh(suspend=True)

        for app in applist:

            try:
                path = os.path.join(self.export_path.text(),app[0])
                
                if not os.path.exists(path):
                    os.mkdir(path)

                #find the cut name
                cutchild = os.path.abspath(os.path.join(phelp.goFindFolder(path,"0_camera"),"../"))
                cut = cutchild.split("\\")[-1]
                
                allfiles = fhelp.listAllFilesInFolder(path)
                latestversion = fhelp.getLatestFromList(allfiles)
                version = fhelp.versionPlusOne(latestversion)

                ext = ".abc"
                filename = cut + "_camera" + version + ext
                filepath = os.path.join(path,filename)
                camtobake = camex.createCamera(app[1],mglobals)
                camex.bakeCamera(selectedcam,camtobake,int(self.frame_range_start.text()),int(self.frame_range_end.text()),app[2])
                command = exhelp.pcABCCameraArgs(camtobake.name(),filepath,int(self.frame_range_start.text()),int(self.frame_range_end.text()),attrlist,step=str(self.frame_step.text()))
                pm.AbcExport(j=command)

                # delete camera
                pm.delete(camtobake)
            except:
                pm.confirmDialog(title="WARNING",message="There was an error when trying to export the {} camera".format(app[1]))
                return

        pm.refresh(suspend=False)
        
        pm.confirmDialog(title="SUCCESS",message="All cameras exported",button=['Sweet!'], defaultButton='Sweet!')

        if self.openFolder.isChecked():
            
            correctedpath = str(self.export_path.text().replace("\\","/") + "/maya")
            os.startfile(os.path.realpath(correctedpath))
        

        self.close()





















