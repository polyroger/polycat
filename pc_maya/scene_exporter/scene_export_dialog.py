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
import pymel.core as pm

#polycat imports
import os
from pc_maya.maya_helpers import export_helpers
from pc_maya.exporters import pc_abc_exporter, export_mb
from pc_helpers import pc_path_helpers as pathhelp
# from pipeline_utilities import path_manipulation


def mayaMainWindow():
    """
    Helper function that returns a python object for maya's main window, so that you can use this python object as the parent for qt widgets 
    in maya.
    """
    mainwindowpointer = omui.MQtUtil.mainWindow()
    mainwindowobject = wrapInstance(long(mainwindowpointer),QtWidgets.QWidget)

    return mainwindowobject


class PcSceneExporter(QtWidgets.QDialog):

    ATTR_ROLE = QtCore.Qt.UserRole
    VALUE_ROLE = QtCore.Qt.UserRole + 1

    exporter_dialog = None

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

        print("this is the init")

        self.setWindowTitle("Polycat Exporter")
        self.setMinimumSize(500,120)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.createWidgets()
        self.createLayout()
        self.createConnections()

    
    def createWidgets(self):

        #geo export table
        self.geo_table = QtWidgets.QTableWidget()
        self.geo_table.setColumnCount(3)
        self.geo_table.setColumnWidth(0,30)
        self.geo_table.setColumnWidth(2,30)
        self.geo_table.setHorizontalHeaderLabels(["E","Name","SF"])
        self.geo_table_header = self.geo_table.horizontalHeader()
        self.geo_table_header.setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
   
        #export path widgets
        self.geo_export_path = QtWidgets.QLineEdit()
        self.geo_export_path.setText(pathhelp.goFindFolder(self.getStartingPath(),"0_sourcegeo"))
        self.geo_export_path_label = QtWidgets.QLabel("Export Directory :")
        self.geo_export_path_btn = QtWidgets.QPushButton()
        self.geo_export_path_btn.setIcon(QtGui.QIcon(":fileOpen.png"))
        self.geo_export_path_btn.setToolTip("select file")

        #frame range widgetts
        self.frame_range_label = QtWidgets.QLabel("Frame Range : ")
        self.frame_range_start = QtWidgets.QLineEdit(str(export_helpers.getFrameRanges()[0]))
        self.frame_range_start.setMaximumWidth(75)
        self.frame_range_end = QtWidgets.QLineEdit(str(export_helpers.getFrameRanges()[1]))
        self.frame_range_end.setMaximumWidth(75)

        intvalidator = QtGui.QIntValidator(-99999,99999,self)
        self.frame_range_start.setValidator(intvalidator)
        self.frame_range_end.setValidator(intvalidator)

        #button widgets
        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.export_btn = QtWidgets.QPushButton("Export All")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        
    
    def createLayout(self):

        #main layout
        main_layout = QtWidgets.QVBoxLayout(self)

        geo_table_layout = QtWidgets.QHBoxLayout()
        geo_table_layout.addWidget(self.geo_table)
        
        geo_export_layout = QtWidgets.QHBoxLayout()
        geo_export_layout.addWidget(self.geo_export_path_label)
        geo_export_layout.addWidget(self.geo_export_path)
        geo_export_layout.addWidget(self.geo_export_path_btn)

        frame_range_layout = QtWidgets.QHBoxLayout()
        frame_range_layout.addWidget(self.frame_range_label)
        frame_range_layout.addWidget(self.frame_range_start)
        frame_range_layout.addWidget(self.frame_range_end)

        body_layout = QtWidgets.QFormLayout()
        body_layout.addRow("",geo_table_layout)
        body_layout.addRow("",geo_export_layout)
        body_layout.addRow("",frame_range_layout)
        
        #main dialog button layout
        d_btn_layout = QtWidgets.QHBoxLayout()
        d_btn_layout.addStretch()
        d_btn_layout.addWidget(self.refresh_btn)
        d_btn_layout.addWidget(self.export_btn)
        d_btn_layout.addWidget(self.cancel_btn)

        # main dialog layout
        
        main_layout.addLayout(body_layout)
        main_layout.addLayout(d_btn_layout)


    def createConnections(self):
        
        self.geo_export_path_btn.clicked.connect(lambda : self.showFileDialog(self.geo_export_path))
        self.export_btn.clicked.connect(lambda : self.runExportGeo(self.geo_table))
        self.refresh_btn.clicked.connect(lambda : self.refreshPysideTableWidget(self.geo_table,export_helpers.getExportSet()))
        self.cancel_btn.clicked.connect(self.close)
       

    #START OF CUSTOM METHODS

    def showFileDialog(self,lineedit):
        myd = QtWidgets.QFileDialog.getExistingDirectory(self,"Select export directory",dir=self.geo_export_path.text())
        if myd:
            lineedit.setText(myd)
        
    def getStartingPath(self):
        
        maya_file = pm.sceneName()

        try:
            print(os.path.isfile(maya_file[0]))
            startpath = os.path.split(maya_file)[0]
        except IndexError:
            print("The current scene has not been saved")
            startpath = "\\\\YARN\projects"

        return startpath

    def buttontest(self):

        myitem = self.geo_table.item(0,1)
        myitemflags = myitem.flags()
        myitemflags
        myindex = QtWidgets.QTableWidget.indexFromItem(self.geo_table,myitem)
        print(myindex.isValid)
        print(myindex)
        print(myitem.text())
        print(myitem.data(self.ATTR_ROLE))
        print(myitem.data(self.VALUE_ROLE))
        print(myitem.checkState())
    

    def runExportGeo(self,table):

        print("running export geo")
        
        explist = export_helpers.getExportList(table)
        print(explist)

        for i in explist:
            
            exportname = i.data(self.VALUE_ROLE)
            exportpath = self.geo_export_path.text()
            start = self.frame_range_start.text()
            end = self.frame_range_end.text()
            singlframe = export_helpers.checkBoxStateBool(table.item(i.row(),2))
            
            print("\n {0} will be exported".format(exportname))

            #.abc export
            pc_abc_exporter.pcAbcExporter(exportname,exportpath,start,end,singlframe)
            #. mb export
            export_mb.run_export(exportname, exportpath)

    #this is overwriting the QtWidjet showEvent() method. So that when the window show() event is triggered it automtically refreshes
    def showEvent(self,e):
        super(PcSceneExporter,self).showEvent(e)
        self.refreshPysideTableWidget(self.geo_table,export_helpers.getExportSet())
        self.geo_export_path.setText(pathhelp.goFindFolder(self.getStartingPath(),"0_sourcegeo"))

    def refreshPysideTableWidget(self,table,table_data):
        """
        Takes in a table and a list of items, sets the rows to 0 then re builds the rows from the list.\n
        First argument : a table object \n
        Second argument : a list of row entries
        """
        print("Running table refresh")

        if table_data:
            
            table.setRowCount(0)
            
            for i in range(len(table_data)):
                table.insertRow(i)
                geogroup = table_data[i]
                self.insertTableItem(i,0,"","Exportme",True,True)
                self.insertTableItem(i,1,geogroup.name(),"groupname",geogroup.name(),False)
                self.insertTableItem(i,2,"","Single Frame",False,True)
        else:
            print("An export set could not be found")
       
    def insertTableItem(self,row,column,text,attr,value,checkable):
        
        item = QtWidgets.QTableWidgetItem(text)
        item.setFlags(QtCore.Qt.ItemIsEnabled)                  #not sure wht this modifier doesnt let the user edit. But it works
        self.setItemAttr(item,attr)
        self.setItemValue(item,value)
        
        if checkable:
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.setItemChecked(item,value)

        self.geo_table.setItem(row,column,item)

    def setItemText(self,item,text):
        """
        Sets the text of a QtWidjet table item \n
        Takes a QT Table item as an argument and a text string\n
        eg : setItemText(self, mytableitem,"this is an items text")
        """
        item.setText(text)

    def getItemText(self,item):
        """
        Gets the text of a QtWidget table item
        Takes a QT Table item as an argument
        """

        return item.text()

    def setItemChecked(self,item,checked):
        """
        Sets the state of a checkbox to a QT state to whether it is checked or not \n
        Works with the isItemChecked helper
        """

        if checked:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.Unchecked)

    def isItemChecked(self,item):

        return item.checkState() == QtCore.Qt.Checked

    def setItemAttr(self,item,attr):
        item.setData(self.ATTR_ROLE,attr)

    def getItemAttr(self,item):
        return item.data(self.ATTR_ROLE)
    
    def setItemValue(self,item,value):
        item.setData(self.VALUE_ROLE, value)
    
    def getItemValue(self,item):
        return item.data(self.VALUE_ROLE)







