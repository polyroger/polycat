import sys,os,pathlib
from PySide2 import QtWidgets,QtCore,QtGui

import maya_audio_transcode as mat

class MayaAudioTranscode(QtWidgets.QDialog):

    FFMPEG_PATH = r"\\YARN\projects\pipeline\utilities\ffmpeg\bin\ffmpeg.exe"

    def __init__(self):
        super().__init__()

        self.selection = None
        self.export_folder = r"\\YARN\projects"

        self.windowAttributes()
        self.createWidgets()
        self.createLayouts()
        self.createConnections()

        self.show()

    def windowAttributes(self):
        self.setWindowTitle("Maya Audio Transcode")
        self.setGeometry(int(200),int(200),int(600),int(200))
        self.setWindowFlags(QtCore.Qt.WindowType.Window)
        # print(QtWidgets.QStyleFactory.keys())
    
    def createWidgets(self):
        #filepath
        self.inputfile_path = QtWidgets.QLineEdit()
        self.inputfile_path.setText("Select a file(s) that you want to convert")
        self.inputfile_path.setMinimumWidth(250)

        self.select_file_btn = QtWidgets.QPushButton()
        self.select_file_btn.setText("...")

        self.open_folder = QtWidgets.QCheckBox()
        self.open_folder.setChecked(True)

        self.outputlogging = QtWidgets.QLineEdit()
        self.outputlogging.setMinimumSize(75,200)
        self.outputlogging.setText("Implement logging to this window,\nPlaceholder for future use")

        #dialog buttons
        self.convert_btn = QtWidgets.QPushButton("Convert")
        self.cancel_btn = QtWidgets.QPushButton("Close")

        
    def createLayouts(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        filepath_layout = QtWidgets.QHBoxLayout()
        filepath_layout.addWidget(self.inputfile_path)
        filepath_layout.addWidget(self.select_file_btn)

        checkbox_layout = QtWidgets.QHBoxLayout()
        checkbox_layout.addWidget(self.open_folder)

        logging_output_layout = QtWidgets.QHBoxLayout()
        logging_output_layout.addWidget(self.outputlogging)
        
        body_layout = QtWidgets.QFormLayout()
        body_layout.addRow("Select File",filepath_layout)
        body_layout.addRow("Open folder after export",checkbox_layout)
        body_layout.addRow("Output",logging_output_layout)

        dialog_btn_layout = QtWidgets.QHBoxLayout()
        dialog_btn_layout.addStretch()
        dialog_btn_layout.addWidget(self.convert_btn)
        dialog_btn_layout.addWidget(self.cancel_btn)

        main_layout.addLayout(body_layout)
        main_layout.addLayout(dialog_btn_layout)

    def createConnections(self):
        self.select_file_btn.clicked.connect(self.selectFileDialog)
        
        self.convert_btn.clicked.connect(self.createMayaWavs)
        self.cancel_btn.clicked.connect(self.close)

    ######### START OF UI METHODS ############

    def createMayaWavs(self):
        
        selected = mat.convert_to_wav(self.FFMPEG_PATH,self.selection)
        openfolder = os.path.realpath(str(pathlib.Path(selected).parent))
        print("this is {}".format(openfolder))
        
        if self.open_folder.isChecked():
            os.startfile(openfolder)

        self.selection = None
    
    def selectFileDialog(self):
        """
        Returns a list of selected files.
        """
        if os.path.exists(self.inputfile_path.text()):
            startpath = self.inputfile_path.text()
        else:
            startpath = r"\\YARN\projects"

        selection,filters = QtWidgets.QFileDialog.getOpenFileNames(self,"select a file or folder",startpath)

        self.selection = selection
        print("selected files : {0}".format(self.selection))
  

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyle("Fusion")
    mat_ui = MayaAudioTranscode()
    sys.exit(app.exec_())