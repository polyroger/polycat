"""
Python3
Standalone app that connects to a running instance of resolve and sets render settings that allow individual clips to be rendered out with audio
"""

import sys
from PySide2 import QtWidgets,QtCore,QtGui
import pc_previs_from_resolve as pfr

class PrevisFromResolve(QtWidgets.QDialog,pfr.Pc_Logger):

    
    def __init__(self):
        super().__init__()
        
        self.resolve_dict = pfr.connetToResolve()
        
        #attempting the connection
        print("attempting to connect to resolve")
        
        if self.resolve_dict:
            
            super().info("Connection Successful")
            print(self.resolve_dict["resolve"])            
            self.windowAttributes()
            self.createWidgets()
            self.createLayouts()
            self.createConnections()
            self.show()

        else:
            
            super().info("Connection Failed")
            sys.exit()
        

    def windowAttributes(self):
        
        self.setWindowTitle("Resolve Previs Export")
        self.setGeometry(int(200),int(200),int(600),int(200))
        self.setWindowFlags(QtCore.Qt.WindowType.Window)
    
    def createWidgets(self):

        #export path widgets
        self.export_path = QtWidgets.QLineEdit()
        self.export_path.setText(r"\\YARN\projects")
        self.export_path_btn = QtWidgets.QPushButton("...")
        self.export_path_btn.setToolTip("select export location")

        #timeline widget
        self.timeline = QtWidgets.QComboBox()
        pfr.createCBoxItemsFromObj(self.timeline,pfr.getTimelineObjects(self.resolve_dict["proj"]))

        #render preset widget
        self.render_preset = QtWidgets.QComboBox()
        pfr.createCBoxItemsList(self.render_preset,self.resolve_dict["proj"].GetRenderPresetList())

        #track number widget
        self.track_number = QtWidgets.QComboBox()
        pfr.createCBoxItemsList(self.track_number,pfr.getTrackList(self.resolve_dict["proj"],self.timeline.currentData()))

        #button widgets
        self.render_button = QtWidgets.QPushButton("Create Render Que")
        self.close_button = QtWidgets.QPushButton("Close")


    def createLayouts(self):

        main_layout = QtWidgets.QVBoxLayout(self)

        #export path layout
        export_path_layout = QtWidgets.QHBoxLayout()
        export_path_layout.addWidget(self.export_path)
        export_path_layout.addWidget(self.export_path_btn)

        #timeline layoue
        timeline_layout = QtWidgets.QHBoxLayout()
        timeline_layout.addWidget(self.timeline)

        #render preset layout
        render_preset_layout = QtWidgets.QVBoxLayout()
        render_preset_layout.addWidget(self.render_preset)

        #track number layout
        track_number_layout = QtWidgets.QHBoxLayout()
        track_number_layout.addWidget(self.track_number)

        #button layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.render_button)
        button_layout.addWidget(self.close_button)

        #body layout
        body_layout = QtWidgets.QFormLayout()
        body_layout.addRow("Export Path",export_path_layout)
        body_layout.addRow("Timeline to export",timeline_layout)
        body_layout.addRow("Render Preset",render_preset_layout)
        body_layout.addRow("Video Track",track_number_layout)

        #main layout
        main_layout.addLayout(body_layout)
        main_layout.addLayout(button_layout)
    
    def createConnections(self):

        self.export_path_btn.clicked.connect(self.setExportDir)
        
        self.timeline.currentIndexChanged.connect(self.switchTimeline)
        self.timeline.currentIndexChanged.connect(self.refreshTracks)

        self.render_button.clicked.connect(self.renderTimeline)
        self.close_button.clicked.connect(sys.exit)
    
    #start of ui methods

    def renderTimeline(self):

        project = self.resolve_dict["proj"]
        exportpath = str(self.export_path.text())
        timeline = self.timeline.currentData()
        tracknum = int(self.track_number.currentData())
        renderpreset = str(self.render_preset.currentData())

        pfr.Pc_Logger.info("{0}\n{1}\n{2}\n{3}\n{4}".format(project,exportpath,timeline,tracknum,renderpreset))

        pfr.renderPrevisCuts(project,exportpath,timeline,tracknum,renderpreset)
    
    def switchTimeline(self,index):
        selection = self.timeline.itemData(index)
        
        if self.resolve_dict["proj"].SetCurrentTimeline(selection):

            super().info("Changed timeline successfully")
        
        else:

            super().info("Could not switch timeline")
    
    def refreshTracks(self,index):
        self.track_number.clear()
        pfr.createCBoxItemsList(self.track_number,pfr.getTrackList(self.resolve_dict["proj"],self.timeline.currentData()))

    def setExportDir(self):
        
        exportdir = QtWidgets.QFileDialog.getExistingDirectory(self,"Select Export Directory",self.export_path.text())

        if exportdir:
            self.export_path.setText(exportdir)
        
    

# Requirements for the gui to launch
app = QtWidgets.QApplication([])
window = PrevisFromResolve()
sys.exit(app.exec_())