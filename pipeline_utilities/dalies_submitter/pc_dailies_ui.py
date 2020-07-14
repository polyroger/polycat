import sys,json,subprocess
import json
import yaml

from PySide2 import QtWidgets,QtCore,QtGui


class PcDailiesGui(QtWidgets.QDialog):

    FFMPEG = r"\\YARN\projects\pipeline\utilities\ffmpeg\bin\ffmpeg.exe"
    OIIO = r"\\YARN\projects\pipeline\utilities\OpenImageIO-1.5.0-OCIO\bin\oiiotool.exe"

    FILEFILTERS = "jpeg (*.jpg *.jpeg);;png (*.png);;exr (*.exr);; all files (*.*)"
    defaultfilter = "all files (*.*)"

    ASSETLIST = ["Assets","Shots"]

    KASSETDATAPATH = r"\\YARN\projects\mov\eos\0_aaa\0_internal\0_project_data\kassetdata.json"
    KSHOTDATAPATH = r"\\YARN\projects\mov\eos\0_aaa\0_internal\0_project_data\kshotdata.json"
    
    def __init__(self):
        super().__init__()

        self.KASSETDATA = self.loadJdata(self.KASSETDATAPATH)
        self.KSHOTDATA = self.loadJdata(self.KSHOTDATAPATH)

        self.windowAttributes()
        self.createWidgets()
        self.createLayouts()
        self.createConnections()

        self.show()

    def windowAttributes(self):
        
        # self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("Polycat Dailies Submitter")
        self.setGeometry(int(800),int(200),int(500),int(100))
        self.setWindowFlags(QtCore.Qt.WindowType.Window)

    def createWidgets(self):
        
        #file selection
        self.select_file_label = QtWidgets.QLabel("Import :")
        self.select_file = QtWidgets.QLineEdit("Select file")
        self.select_file_btn = QtWidgets.QPushButton("...")
        self.select_file_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.select_file_btn.setToolTip("Choose the file to be dailied")
        
        #comboboxes
        self.sequence_box = QtWidgets.QComboBox()
        self.createCBoxItems(self.sequence_box,self.ASSETLIST)

        self.asset_type_box = QtWidgets.QComboBox()
        self.asset_type_box.addItems(["Asset Type"])
        self.asset_box = QtWidgets.QComboBox()
        self.asset_box.addItems(["Asset"])
        self.task_box = QtWidgets.QComboBox()
        self.task_box.addItems(["Task"])

        #output line edit
        self.output_file_label = QtWidgets.QLabel("Export :")
        self.output_file = QtWidgets.QLineEdit("Export file")
        self.output_file_btn = QtWidgets.QPushButton("...")
        self.output_file_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.select_file_btn.setToolTip("Choose the export path")


        #comment box
        self.comment_box_label = QtWidgets.QLabel("Comments")
        self.comment_box_label.setAlignment(QtCore.Qt.AlignBottom)
        self.comment_box_1 = QtWidgets.QLineEdit()
        self.comment_box_2 = QtWidgets.QLineEdit()
        self.comment_box_3 = QtWidgets.QLineEdit()


        #button widgets
        self.submit_btn = QtWidgets.QPushButton("Submit")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def createLayouts(self):
        
        #main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        
        #select_file
        select_file_layout = QtWidgets.QHBoxLayout()
        select_file_layout.addWidget(self.select_file_label)
        select_file_layout.addWidget(self.select_file)
        select_file_layout.addWidget(self.select_file_btn)

        #cobobox layout
        combobox_layout = QtWidgets.QHBoxLayout()
        combobox_layout.addWidget(self.sequence_box)
        combobox_layout.addWidget(self.asset_type_box)
        combobox_layout.addWidget(self.asset_box)
        combobox_layout.addWidget(self.task_box)

        #export_file
        output_file_layout = QtWidgets.QHBoxLayout()
        output_file_layout.addWidget(self.output_file_label)
        output_file_layout.addWidget(self.output_file)
        output_file_layout.addWidget(self.output_file_btn)


        #comment layout
        comment_layout = QtWidgets.QVBoxLayout()
        comment_layout.addWidget(self.comment_box_label)
        comment_layout.addWidget(self.comment_box_1)
        comment_layout.addWidget(self.comment_box_2)
        comment_layout.addWidget(self.comment_box_3)
    
        #button layout
        d_btn_layout = QtWidgets.QHBoxLayout()
        d_btn_layout.addStretch()
        d_btn_layout.addWidget(self.submit_btn)
        d_btn_layout.addWidget(self.cancel_btn)
        
        main_layout.addLayout(combobox_layout)
        main_layout.addLayout(select_file_layout)
        main_layout.addLayout(output_file_layout)
        main_layout.addLayout(comment_layout)
        main_layout.addLayout(d_btn_layout)
    
    def createConnections(self):
        #when creating connections remember that whenever a widget is called it will invoke the connection even if in a different method
        
        self.select_file_btn.clicked.connect(self.selectFileDialog)
        self.output_file_btn.clicked.connect(self.exportFileDialog)
        
        self.sequence_box.currentTextChanged.connect(self.refreshAssetTypeCBox)
        self.asset_type_box.currentTextChanged.connect(self.refreshAssetCBox)
        self.asset_box.currentTextChanged.connect(self.refreshTaskCBox)      
        
        self.submit_btn.clicked.connect(self.submitToDailies)
        self.cancel_btn.clicked.connect(self.close)

     
    #*************************************************
    #START OF DIAOLOG METHODS

    def loadJdata(self,jfile):
        
        with open(jfile,"r") as jdata:
            data = json.load(jdata)
            jdata.close()
        
        # print(data)
        return data
    
    
    def refreshAssetTypeCBox(self,level):

        itemlist = []

        if level == "Assets":
            
            for key,value in self.KASSETDATA.items():
                itemlist.append(key)
            self.asset_type_box.blockSignals(True)
            self.asset_type_box.clear()
            self.createCBoxItems(self.asset_type_box,itemlist)
            self.asset_type_box.blockSignals(False)
            
        
        elif level == "Shots":
            
            for key,value in self.KSHOTDATA.items():
                itemlist.append(key)

            self.asset_type_box.blockSignals(True)
            self.asset_type_box.clear()
            self.createCBoxItems(self.asset_type_box,itemlist)
            self.asset_type_box.blockSignals(False)

        
        else:
            print("The level was not set correctly")
            return None

    def refreshAssetCBox(self,assettype):


        assetlist = []
        sequence = self.sequence_box.currentData()
        
        if sequence == "Assets":
            data = self.KASSETDATA
        elif sequence == "Shots":
            data = self.KSHOTDATA
        
        for key,value in data[assettype].items():
            assetlist.append(key)
        
        self.asset_box.blockSignals(True)
        self.asset_box.clear()
        self.createCBoxItems(self.asset_box,assetlist)
        self.asset_box.blockSignals(False)
    
    def refreshTaskCBox(self,asset):


        tasklist = []
        sequence = self.sequence_box.currentData()
        atype = self.asset_type_box.currentData()
        
        if sequence == "Assets":
            data = self.KASSETDATA
        elif sequence == "Shots":
            data = self.KSHOTDATA
        
        self.task_box.clear()
        self.createCBoxItems(self.task_box,data[atype][asset]["tasks"])
        
            
    
    def createCBoxItems(self,combobox,itemlist):


        if itemlist:

            for item in itemlist:
                combobox.addItem(item,item)
            return combobox
        else:
            print("there are no items in the itemlist")
            return None


    def selectFileDialog(self):

        filename,filefilter = QtWidgets.QFileDialog.getOpenFileName(self,"select file",r"\\YARN\projects\mov\eos\3_development\pipeline_tools\dailies_submitter\test_files\sequences\render",self.FILEFILTERS,self.defaultfilter )
        if filename:
            self.select_file.setText(filename)
    
    def exportFileDialog(self):
    
        filters = "mp4 *.mp4"
        selected_filter = "mp4 *.mp4"

        output_path, selected_filter = QtWidgets.QFileDialog.getSaveFileName(self, "Save File As", "", filters, selected_filter)
        if output_path:
            self.output_file.setText(output_path)
       
    def convertImage(self):
        pass

    def submitToDailies(self):
        print("TODO: implement the backend")

    def printTest(self,test):
        print("the printTest function is returning a {0} type \n its value is {1}".format(type(test),test))
        print(self.sequence_box.currentData())


# Requirements for the gui to launch
app = QtWidgets.QApplication()
pcds = PcDailiesGui()
sys.exit(app.exec_())

# oiiotool basic command to export file and color convert
# oiiotool --frames 1001-1050 --colorconvert "ACES - ACEScg" "Output - rec709" .\scientific_wizard_lodge_pangolin_lodge_test_v01_#.exr -ch R,G,B -o test.#.jpeg

#ffmpeg
#ffmpeg -apply_trc bt709 -start_number 1001 -framerate 24 -i .\scientific_wizard_lodge_pangolin_lodge_test_v01_%04d.exr -c:v libx264 -vf scale=1280:-2 bt709_output.mp4
    #-apply_trc bt709 applies a color transform specific to exr sequences
    #scale=1280:-2 makes the width 1280 then scales the video heigt to be a proportional ratio divisible by 2

# this is on a png sequence that has been converted in ooio
#ffmpeg -start_number 1001 -framerate 24 -i .\test.%04d.exr -c:v libx264 -vf "scale=1280:-2" -pix_fmt yuv420p bt709_output.mp4
    # -vf "scale=1280:-2" scales the video so the width is 1280 and the -2 adjusts the height to maintain the aspect ratio.
    # -pix_fmt sets the pixel format for the codec. Google tells me that yuv420p is a good one.

