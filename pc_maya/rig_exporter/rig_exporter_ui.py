"""
Polycat animations maya rig exporter ui

"""
# system imports
import os,re

# Maya imports
import maya.cmds as cmds 

# pyside2 imports    
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

# pipeline helpers
from pc_helpers import pc_path_helpers as phelp
from pc_helpers import pc_file_helpers as fhelp

#maya helpers
from pc_maya.maya_helpers import export_helpers as exhelp
from pc_maya.maya_helpers import scene_helpers as shelp
from pc_maya.maya_helpers import pyside2_helpers as py2help


class PcRigExporterUi(QtWidgets.QDialog):

    RIGEXPORTSET = "RIGEXPORTSET"
    FILE_FILTERS = "MayaBinary (*.mb)"
    DEFAULT_FILTER = "MayaBinary (*.mb)"

    rig_export_dialog = None

    @classmethod
    def open_rig_export_dialog(cls):

        # Checks for the existance of a rig set, creates it if not there
        rigset = cls.check_for_rig_set()
        if rigset == "Create":
            exhelp.create_rig_export_set()
            return
        elif rigset == "Cancel":
            return

        # Check if the rigset has items in it, that its a group and if the name ends with _rig
        if not cls.check_set_for_items():
            return
    
        # Checks if there is already an instance running, if so show it if no create it
        if not cls.rig_export_dialog:
            cls.rig_export_dialog = PcRigExporterUi()
            cls.rig_export_dialog.show()
        
        if cls.rig_export_dialog.isHidden():
            cls.rig_export_dialog.show()
        else:
            cls.rig_export_dialog.raise_()
            cls.rig_export_dialog.activateWindow()

    def __init__(self,parent=py2help.mayaMainWindow()):

        super(PcRigExporterUi, self).__init__(parent)

        self.setWindowTitle("Export Rig")
        self.setMinimumSize(600,150)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layout()
        self.create_connections()
    
    def create_widgets(self):
        
        #export path widgets
        self.export_path = QtWidgets.QLineEdit()
        self.export_path.setText(self.set_export_path())
        self.export_path_btn = QtWidgets.QPushButton()
        self.export_path_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.export_path_btn.setToolTip("select file")  

        # open folder checkbox
        self.openFolder = QtWidgets.QCheckBox()
        self.openFolder.setChecked(True)

        #button widgets
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.export_btn = QtWidgets.QPushButton("Export")


    def create_layout(self):
        
        main_layout = QtWidgets.QVBoxLayout(self)
        
        filepath_layout = QtWidgets.QHBoxLayout(self)
        filepath_layout.addWidget(self.export_path)
        filepath_layout.addWidget(self.export_path_btn)

        checkbox_layout = QtWidgets.QVBoxLayout(self)
        checkbox_layout.addWidget(self.openFolder) 

        body_layout = QtWidgets.QFormLayout(self)
        body_layout.setVerticalSpacing(10)
        body_layout.setLabelAlignment(QtCore.Qt.AlignLeft)
        body_layout.addRow("Export Path : ",filepath_layout)       
        body_layout.addRow("Open file dialog : ",checkbox_layout)

        button_layout = QtWidgets.QHBoxLayout(self)
        button_layout.addStretch()
        button_layout.addWidget(self.export_btn)
        button_layout.addWidget(self.cancel_btn)


        main_layout.addLayout(body_layout)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        
        self.export_path_btn.clicked.connect(self.select_export_dir)
        self.export_btn.clicked.connect(lambda :self.export_rig(self.export_path.text()))
        self.cancel_btn.clicked.connect(self.close)
        

    ### START OF UI METHOS ###

    # I extend the raise_ to force a refresh when the gui is not closed and there is an update to the contents of the rig directory
    # def raise_(self):
    #     self.set_export_path()
    #     print("extending the raise function to refresh the export path")
    #     super(PcRigExporterUi, self).raise_()


    @classmethod
    def check_for_rig_set(cls):

        if cmds.ls(cls.RIGEXPORTSET):
            return True
        else:
            answer = cmds.confirmDialog(title="Error", message="There is no 'RIGEXPORTSET', would you like to create one?", button=["Create", "Cancel"])
            return answer
    
    @classmethod
    def check_set_for_items(cls):
        """
        Used when the ui inits for characters and in the file validation for custom paths
        """

        items = cmds.sets(cls.RIGEXPORTSET,q=True)
        if items == None or not items:
            answer = cmds.confirmDialog(title="Error", message="There isnt anything in the RIGEXPORTSET", button=["OK..I will add a rig group"])
            return False
        else:
            for item in items:
                if item.endswith("_rig"):
            
                    return item
            # if none of the items end in _rig then return false
            answer = cmds.confirmDialog(title="Error", message="No item in the RIGEXPORTSET ends in `_rig`, please rename ", button=["OK..I will rename the item"])
            
            return False
    
    def select_items_in_set(self, set_name):
        cmds.select(clear=True)
        set_members = cmds.sets(set_name, q=True)
        if set_members:
            for item in set_members:
                cmds.select(item, add=True, ne=True)
            return set_members
        else:
            raise Exception("There are no items in the RIGEXPORTSET")

    
    def select_export_dir(self):
    
        export_dir, filter = QtWidgets.QFileDialog.getSaveFileName(self,"Select the file to save", dir=self.export_path.text(),filter=self.FILE_FILTERS,selectedFilter=self.DEFAULT_FILTER)
        
        if export_dir:
            self.export_path.setText(export_dir)
    
    def get_export_path(self):

        export_dir = "0_sourcegeo"
        export_label_path = phelp.goFindFolder(shelp.getScenePath(),export_dir)

        return export_label_path
    
    def set_export_path(self):
        """
        Sets the export path in the ui when loaded, This works for characters. Props tend to have a more complicated folder struncture so finding the directory will be
        a more manual process.
        """

        win_path = self.get_export_path().replace("/","\\")
        
        set_members = cmds.sets(self.RIGEXPORTSET, q=True)
        if set_members:
            for item in set_members:
                if cmds.nodeType(item) == "transform" and item.endswith("_rig"):
                    try:
                        server_name = item.replace("_rig", "")
                        if not server_name in os.listdir(win_path):  # if the name of the rig is not a child of the sourcegeo then its most likely a prop with potentially a random user defined path
                            return win_path
                        else:
                            server_path = os.path.realpath(os.path.join(win_path,server_name,"rig"))
                            latest_version = fhelp.versionPlusOne(fhelp.getLatestVersion(server_path)) # gets the latest version as an int then makes it a v000 string
                            export_path = os.path.join(server_path,server_name) + "_rig{0}{1}".format(latest_version,".mb")
                            
                            return export_path.replace("/","\\")
                    
                    except Exception as e:
                        print(e)
                        
                        return win_path

        return win_path

    def filename_validator(self, filename):

        version_re = r"_v(\d{3})"
        rig_version_re = r"(_rig_v\d+.mb$)"

        if filename:
            
            try:
                print("validating extension")
                # is there a filenam
                if not os.path.splitext(filename)[1]:
                    raise Exception("Please enter a valid file with a .mb extension")
                
                print("validating spaces")
                # check for spaces
                if " " in filename:
                    raise Exception("There is a space in your filename, please remove it or use '_' instead")
                
                print("validating case")
                # check for case
                if not filename.islower():
                    raise Exception("You may not have any uppercase characters in your filename, please rename to all be lowercase")
                
                print("validating version naming")
                # versioning check
                if not re.search(version_re, filename):
                    raise Exception("There is no _v000 style versioning in your filename, please add _v000 style versioning")
                if not re.search(rig_version_re, filename):
                    raise Exception("There is no '_rig_' before v000 style version in your filename")
                
                print("validating filename")
                # Is filename the same as rig group name
                if not filename.split("_v0")[0] == self.check_set_for_items():
                    raise Exception("The filename and the rig group name need to match. Please check the correct spelling")

                return True
            
            except Exception as e:
                return e
            
    def export_rig(self,export_path):
        
        try:
            basename, filename = os.path.split(export_path)
            validation = self.filename_validator(filename)
            print(validation)
            # the exception here is handled in the filename_validator function, and the msg passed through to this try block
            if type(validation) == Exception:
                raise Exception("{}".format(validation))

            self.select_items_in_set(self.RIGEXPORTSET)
                                          
            if not os.path.isdir(basename):
                os.makedirs(basename)
            
            cmds.file(export_path,es=True, type="mayaBinary", chn=True, con=True,sh=True)
            cmds.confirmDialog(title="Success", message="Rig exported succesfully", button=["Nice!"])

            cmds.select(clear=True)
            
            if self.openFolder.isChecked:
                os.startfile(os.path.realpath(basename))
            
            self.close()

        except Exception as e:
            cmds.confirmDialog(title="ERROR", message="{0}".format(e), button=["Ok"])
            self.close()


 

        

        

            




        
        
        

    
        

  