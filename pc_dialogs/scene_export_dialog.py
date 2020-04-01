# 
# The standard 3d package asset exporter dialog for polycat
# 
#pyside2 imports
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

#shiboken imports 
from shiboken2 import wrapInstance

#maya imports
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as omui

#polycat imports
from pc_maya.exporters.export_helpers import ExportHelpers


def mayaMainWindow():
    """
    Helper function that returns a python object for maya's main window, so that you can use this python object as the parent for qt widgets 
    in maya.
    """
    mainwindowpointer = omui.MQtUtil.mainWindow()
    mainwindowobject = wrapInstance(long(mainwindowpointer),QtWidgets.QWidget)

    return mainwindowobject


class PcSceneExporter(QtWidgets.QDialog):

    exporter_dialog = None
    helpers = ExportHelpers()

    @classmethod
    def openExportDialog(cls):
        
        if not cls.exporter_dialog:
           
            cls.exporter_dialog = PcSceneExporter()
            cls.exporter_dialog.show()
        
        if cls.exporter_dialog.isHidden():
            cls.exporter_dialog.show()
        
        else:
            cls.exporter_dialog.raise_()
            cls.exporter_dialog.activateWindow()
            
    
    def __init__(self,parent=mayaMainWindow()):
        
        super(PcSceneExporter,self).__init__(parent)
       

        self.setWindowTitle("Polycat Exporter")
        self.setMinimumSize(1000,120)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.createWidgets()
        self.createLayout()
        self.createConnections()

        print("this is the init")
    
    def createWidgets(self):

        #geo export table
        self.geo_table = QtWidgets.QTableWidget()
        self.geo_table.setColumnCount(3)
        self.geo_table.setColumnWidth(0,30)
        self.geo_table.setColumnWidth(2,30)
        self.geo_table.setHorizontalHeaderLabels(["E","Name","SF"])
        self.geo_table_header = self.geo_table.horizontalHeader()
        self.geo_table_header.setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
        
        self.geo_export_path = QtWidgets.QLineEdit()
        self.geo_export_path_label = QtWidgets.QLabel("Asset Directory :")
        self.geo_export_path_btn = QtWidgets.QPushButton()
        self.geo_export_path_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.geo_export_path_btn.setToolTip("select file")
        
        
        #camera export table
        self.cam_table = QtWidgets.QTableWidget()
        self.cam_table.setColumnCount(3)
        self.cam_table.setColumnWidth(0,30)
        self.cam_table.setColumnWidth(2,30)
        self.cam_table.setHorizontalHeaderLabels(["E","Name","SF"])
        self.cam_table_header = self.cam_table.horizontalHeader()
        self.cam_table_header.setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
        
        self.cam_export_path = QtWidgets.QLineEdit()
        self.cam_export_path_label = QtWidgets.QLabel("Camera Directory")
        self.cam_export_path_btn = QtWidgets.QPushButton()
        self.cam_export_path_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.cam_export_path_btn.setToolTip("select file")
        
        self.export_btn = QtWidgets.QPushButton("Export")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        
    
    def createLayout(self):

        #main layout
        main_layout = QtWidgets.QVBoxLayout(self)

        geo_export_layout = QtWidgets.QHBoxLayout()
        geo_export_layout.addWidget(self.geo_table)
        geo_export_layout.addWidget(self.geo_export_path_label)
        geo_export_layout.addWidget(self.geo_export_path)
        geo_export_layout.addWidget(self.geo_export_path_btn)

        cam_export_layout = QtWidgets.QHBoxLayout()
        cam_export_layout.addWidget(self.cam_table)
        cam_export_layout.addWidget(self.cam_export_path_label)
        cam_export_layout.addWidget(self.cam_export_path)
        cam_export_layout.addWidget(self.cam_export_path_btn)

        body_layout = QtWidgets.QFormLayout()
        body_layout.addRow("Geo Exports",geo_export_layout)
        body_layout.addRow("Camera Exports", cam_export_layout)
        

        #main dialog button layout
        d_btn_layout = QtWidgets.QHBoxLayout()
        d_btn_layout.addStretch()
        d_btn_layout.addWidget(self.export_btn)
        d_btn_layout.addWidget(self.cancel_btn)

        # main dialog layout
        
        main_layout.addLayout(body_layout)
        main_layout.addLayout(d_btn_layout)


    def createConnections(self):
        
        self.cancel_btn.clicked.connect(self.close)
        self.export_btn.clicked.connect(self.helpers.printTest)

    #START OF CUSTOM METHODS
    
    def exportSelections(self):
        print("TODO: write the export methods")







