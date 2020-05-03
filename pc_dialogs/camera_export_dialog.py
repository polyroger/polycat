# 
# Camera alembic exporter
# 
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
from pipeline_utilities import pyside2_helpers


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





    def __init__(self,parent=pyside2_helpers.mayaMainWindow()):
        super(CameraExporter,self).__init__(parent)

        self.setWindowTitle("Export Camera")
        self.setMinimumSize(300,120)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.createWidgets()
        self.createLayout()
        self.createConnections()




    def createWidgets(self):
        
        #export scale widget
        self.export_scale = QtWidgets.QLineEdit("0.1")
        self.export_scale.setMaximumWidth(75)
        
        floatvalidator = QtGui.QDoubleValidator(0.0,100.0,3,self)
        self.export_scale.setValidator(floatvalidator)

        #frame range widgetts
        self.frame_range_start = QtWidgets.QLineEdit("1001")
        self.frame_range_start.setMaximumWidth(75)
        self.frame_range_end = QtWidgets.QLineEdit("1100")
        self.frame_range_end.setMaximumWidth(75)

        intvalidator = QtGui.QIntValidator(-99999,99999,self)
        self.frame_range_start.setValidator(intvalidator)
        self.frame_range_end.setValidator(intvalidator)

        #button widgets
        self.button_cancel = QtWidgets.QPushButton("Cancel")
        self.button_export = QtWidgets.QPushButton("Export")


    def createLayout(self):

        main_layout = QtWidgets.QVBoxLayout(self)
        
        export_scale_layout = QtWidgets.QHBoxLayout()
        export_scale_layout.addWidget(self.export_scale)

        frame_range_layout = QtWidgets.QHBoxLayout()
        frame_range_layout.addWidget(self.frame_range_start)
        frame_range_layout.addWidget(self.frame_range_end)
    
        body_layout = QtWidgets.QFormLayout()
        body_layout.setVerticalSpacing(10)
        body_layout.addRow("Export Scale : ",export_scale_layout)
        body_layout.addRow("Frame Range : ",frame_range_layout)

        button_layout = QtWidgets.QHBoxLayout(self)
        button_layout.addStretch()
        button_layout.addWidget(self.button_export)
        button_layout.addWidget(self.button_cancel)


        main_layout.addLayout(body_layout)
        main_layout.addLayout(button_layout)
     

      



       
        

    def createConnections(self):
        pass
    


