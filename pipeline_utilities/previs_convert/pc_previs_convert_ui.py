"""
Polycat split video files into frame sequence and audio.
Generally to be used when converting for anim from previs
"""
import os,sys,subprocess
from PySide2 import QtCore,QtGui,QtWidgets

import pc_previs_convert as pcv

class SplitMedia(QtWidgets.QDialog):

    FPS_LIST = [24,25,30]

    def __init__(self):
        super().__init__()

        self.windowAttributes()
        self.creatWidgets()
        self.createLayout()
        self.createConnections()

        self.show()
    
    def windowAttributes(self):
        
        self.setWindowTitle("Split media")
        self.setGeometry(int(200),int(200),int(600),int(200))
        self.setWindowFlags(QtCore.Qt.WindowType.Window)

    def creatWidgets(self):

        # root path selection
        self.selection_root = QtWidgets.QLineEdit()
        self.selection_root.setText(r"\\YARN\projects")
        self.selection_root_button = QtWidgets.QPushButton("...")

        #fps selection
        self.fps = QtWidgets.QComboBox()
        for rate in self.FPS_LIST:
            self.fps.addItem(str(rate),str(rate))

        #start frame
        self.start_frame = QtWidgets.QLineEdit()
        self.start_frame.setMaximumWidth(100)
        self.start_frame.setText(str(1001))

        # dialog buttons
        self.close_button = QtWidgets.QPushButton()
        self.close_button.setText("Close")
        self.split_button = QtWidgets.QPushButton()
        self.split_button.setText("Split")

    def createLayout(self):
        
        main_layout = QtWidgets.QVBoxLayout(self)

        #selection root layout
        selection_root_layout = QtWidgets.QHBoxLayout()
        selection_root_layout.addWidget(self.selection_root)
        selection_root_layout.addWidget(self.selection_root_button)

        # fps layout
        fps_layout = QtWidgets.QHBoxLayout()
        fps_layout.addWidget(self.fps)
        
        # start frame layout
        start_frame_layout = QtWidgets.QHBoxLayout()
        start_frame_layout.addWidget(self.start_frame)

        body_layout = QtWidgets.QFormLayout()
        body_layout.addRow("Select Root Folder",selection_root_layout)
        body_layout.addRow("fps",fps_layout)
        body_layout.addRow("Start Frame",start_frame_layout)

        

        dialog_buttons = QtWidgets.QHBoxLayout()
        dialog_buttons.addStretch()
        dialog_buttons.addWidget(self.split_button)
        dialog_buttons.addWidget(self.close_button)


        main_layout.addLayout(body_layout)
        main_layout.addLayout(dialog_buttons)


    def createConnections(self):
        
        self.selection_root_button.clicked.connect(self.setRootPath)
        self.close_button.clicked.connect(sys.exit)
        self.split_button.clicked.connect(self.splitVideo)

    # Start of ui methods

    def testConnection(self,value):
        print("the connections has been made and the returned value is {}".format(value))
    
    def setRootPath(self):

        root_path = QtWidgets.QFileDialog.getExistingDirectory(self,"Select the scene root to convert",self.selection_root.text())

        if root_path:
            self.selection_root.setText(root_path)
    
    def splitVideo(self):
        
        all_files = pcv.allFilesInFolders(self.selection_root.text())
        ffmpeg_args = pcv.ffmpegArgList(all_files,self.fps.currentData(),self.start_frame.text())

        subprocess.run(ffmpeg_args)










# Requirements for the gui to launch
app = QtWidgets.QApplication([])
window = SplitMedia()
sys.exit(app.exec_())