"""
Polycats material descriton export
"""
#python imports
import os, sys
from pipeline_utilities.pc_logging.pc_logger import Pc_Logger

#pyside2 imports
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

#shiboken imports 
from shiboken2 import wrapInstance

#maya imports
import maya.OpenMayaUI as omui
import maya.cmds as cmds

#polycat imports
from pc_maya.material_exporter import material_exporter as me

def mayaMainWindow():
    """
    Helper function that returns a python object for maya's main window, so that you can use this python object as the parent for qt widgets 
    in maya.
    """
    mainwindowpointer = omui.MQtUtil.mainWindow()
    mainwindowobject = wrapInstance(long(mainwindowpointer),QtWidgets.QWidget)

    return mainwindowobject

class Material_Exporter_Dialog(QtWidgets.QDialog):
    """
    THe materail exprter dialog class
    """

    dialog = None
    
    FILE_FILTERS = "pcmat (*.pcmat)"

    @classmethod
    def open_dialog(cls):
        """
        Using a class method to init your ui class ensures that multiple class objects cant be accidentally init
        """

        if not cls.dialog:
            cls.dialog = Material_Exporter_Dialog()
            cls.dialog.show()
        
        if cls.dialog.isHidden():
            cls.dialog.show()
        
        else:
            cls.dialog.raise_()
            cls.dialog.activateWindow()
        

    def __init__(self, parent = mayaMainWindow()):
        super(Material_Exporter_Dialog,self).__init__(parent)
        
        self.setWindowTitle("Polycat Material exporter")
        self.setMinimumSize(500,120)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        print("creating widgets")
        # line edit
        self.export_path_le = QtWidgets.QLineEdit()
        self.export_path_le.setText("\\\\YARN\\projects\\")
        self.export_path_le.setMinimumWidth(300)
        
        self.open_explorer_btn = QtWidgets.QPushButton("")
        self.open_explorer_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.open_explorer_btn.setToolTip("Open explorer window")
        
        # buttons
        self.export_btn = QtWidgets.QPushButton("Export") 
        self.close_btn = QtWidgets.QPushButton("Close")

        
    def create_layout(self):
        print("print creating layout")
        # main layout
        main_layout = QtWidgets.QVBoxLayout(self)

        # export path layout
        export_path_layout = QtWidgets.QHBoxLayout()
        export_path_layout.addWidget(self.export_path_le)
        export_path_layout.addWidget(self.open_explorer_btn)

        # button layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.export_btn)
        button_layout.addWidget(self.close_btn)

        # form body
        form_body = QtWidgets.QFormLayout()
        form_body.addRow("Export Path :", export_path_layout)

        # adding layouts to the main layout
        main_layout.addLayout(form_body)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        
    
    def create_connections(self):
        self.close_btn.clicked.connect(self.close)
        self.open_explorer_btn.clicked.connect(self.open_explorer)
        self.export_btn.clicked.connect(self.export)
        

    # UI methods

    def open_explorer(self):
        explorer = QtWidgets.QFileDialog.getSaveFileName(self, "Save file", dir=self.export_path_le.text(), filter=self.FILE_FILTERS)
        if explorer:
            self.export_path_le.setText(explorer[0])
    
    def get_export_path(self):
        export_path = self.export_path_le.text()
        name, ext = os.path.splitext(export_path)
        if not ext or ext != ".pcmat":
            return None
        else:
            return export_path
   
    def export(self):
        
        selection = me.get_selection()
        shaders = me.get_assigned_shaders(selection)
        exportpath = self.get_export_path()

        if not selection:
            mb = QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select somthing")
            return
        if not shaders:
            mb = QtWidgets.QMessageBox.warning(self, "Shader Error", "Please make sure that shaders are assigned to your selection")
        if not exportpath:
            mb = QtWidgets.QMessageBox.warning(self, "Export path error", "Please make sure that you have entered a valid export path")

        else:
            mat_dict = me.create_material_dict(shaders, selection)
            pcmat = me.write_material_json(mat_dict, self.get_export_path())
            mb = QtWidgets.QMessageBox.information(self, "Success", "Material description file exported successfully")
            self.close()

       

    
        
