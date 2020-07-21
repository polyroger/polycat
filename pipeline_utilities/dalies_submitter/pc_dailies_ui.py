import os,pathlib,sys,json,re,subprocess

from PySide2 import QtWidgets,QtCore,QtGui


class PcDailiesGui(QtWidgets.QDialog):

    FFMPEG = r"\\YARN\projects\pipeline\utilities\ffmpeg\bin\ffmpeg.exe"
    OIIO = r"\\YARN\projects\pipeline\utilities\OpenImageIO-1.5.0-OCIO\bin\oiiotool.exe"
    LOGO  = r"\\YARN\projects\pipeline\utilities\images\logos\polycat_white_1024x1024.png"
    ICON =  r"\\YARN\projects\pipeline\utilities\images\logos\polycat_black_50x50.png"

    ACES_FROM_SPACE = ["ACES - ACEScg"]
    ACES_TO_SPACE = ["Output - Rec.709"]
    

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
        self.setWindowTitle("Polycat Transcoder")
        self.setGeometry(int(800),int(200),int(500),int(100))
        self.setWindowFlags(QtCore.Qt.WindowType.Window)
        
        self.pcicon = QtGui.QIcon(self.ICON)
        self.setWindowIcon(self.pcicon)

    def createWidgets(self):
         
        #comboboxes
        self.sequence_box = QtWidgets.QComboBox()
        self.createCBoxItems(self.sequence_box,self.ASSETLIST)
        self.asset_type_box = QtWidgets.QComboBox()
        self.asset_type_box.addItems(["Asset Type"])
        self.asset_box = QtWidgets.QComboBox()
        self.asset_box.addItems(["Asset"])
        self.task_box = QtWidgets.QComboBox()
        self.task_box.addItems(["Task"])
        
        #file selection
        self.select_file_label = QtWidgets.QLabel("Import :")
        self.select_file = QtWidgets.QLineEdit("Select file")
        self.select_file_btn = QtWidgets.QPushButton("...")
        self.select_file_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.select_file_btn.setToolTip("Choose the file to be dailied")
       
        #output line edit
        self.output_file_label = QtWidgets.QLabel("Export :")
        self.output_file = QtWidgets.QLineEdit("Export file")
        self.output_file_btn = QtWidgets.QPushButton("...")
        self.output_file_btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.select_file_btn.setToolTip("Choose the export path")

        #color management
        self.enable_col_man = QtWidgets.QCheckBox("Enable Color management")
        self.from_space = QtWidgets.QComboBox()
        self.createCBoxItems(self.from_space,self.ACES_FROM_SPACE)
        self.from_space.setEnabled(False)
        self.to_space = QtWidgets.QComboBox()
        self.createCBoxItems(self.to_space,self.ACES_TO_SPACE)
        self.to_space.setEnabled(False)

        #comment box
        self.comment_box_label = QtWidgets.QLabel("Comments")
        self.comment_box_label.setAlignment(QtCore.Qt.AlignBottom)
        self.comment_box_1 = QtWidgets.QLineEdit()
        self.comment_box_2 = QtWidgets.QLineEdit()
        self.comment_box_3 = QtWidgets.QLineEdit()

        #button widgets
        self.submit_btn = QtWidgets.QPushButton("Convert")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def createLayouts(self):
        
        #main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        
        #cobobox layout
        combobox_layout = QtWidgets.QHBoxLayout()
        combobox_layout.addWidget(self.sequence_box)
        combobox_layout.addWidget(self.asset_type_box)
        combobox_layout.addWidget(self.asset_box)
        combobox_layout.addWidget(self.task_box)

        #select_file
        select_file_layout = QtWidgets.QHBoxLayout()
        select_file_layout.addWidget(self.select_file_label)
        select_file_layout.addWidget(self.select_file)
        select_file_layout.addWidget(self.select_file_btn)
      
        #export_file
        output_file_layout = QtWidgets.QHBoxLayout()
        output_file_layout.addWidget(self.output_file_label)
        output_file_layout.addWidget(self.output_file)
        output_file_layout.addWidget(self.output_file_btn)

        color_man_layout = QtWidgets.QHBoxLayout()
        color_man_layout.addWidget(self.enable_col_man)
        color_man_layout.addWidget(self.from_space)
        color_man_layout.addWidget(self.to_space)

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
        
        # main_layout.addLayout(combobox_layout)
        main_layout.addLayout(select_file_layout)
        main_layout.addLayout(output_file_layout)
        main_layout.addLayout(color_man_layout)
        # main_layout.addLayout(comment_layout)
        main_layout.addLayout(d_btn_layout)
    
    def createConnections(self):
        #when creating connections remember that whenever a widget is called it will invoke the connection even if in a different method
        
        self.select_file_btn.clicked.connect(self.selectFileDialog)
        self.output_file_btn.clicked.connect(self.exportFileDialog)

        self.enable_col_man.stateChanged.connect(self.toggleColorMan)
        
        # self.sequence_box.currentTextChanged.connect(self.refreshAssetTypeCBox)
        # self.asset_type_box.currentTextChanged.connect(self.refreshAssetCBox)
        # self.asset_box.currentTextChanged.connect(self.refreshTaskCBox)      
        
        self.submit_btn.clicked.connect(self.submitToDailies)
        self.cancel_btn.clicked.connect(self.close)

     
    #*************************************************
    #START OF DIAOLOG METHODS

    def toggleColorMan(self,state):

        if state:
            self.from_space.setEnabled(True)
            self.to_space.setEnabled(True)
        else:
            self.from_space.setEnabled(False)
            self.to_space.setEnabled(False)


    def loadJdata(self,jfile):
        
        with open(jfile,"r") as jdata:
            data = json.load(jdata)
            jdata.close()
        
        # print(data)
        return data
    
    def refreshAssetTypeCBox(self,level):
        """
        These refresh methods are there to update the combo box values based off of the kitsue json data.
        Remember any call to a widget that has a valid signal will call the widgets slot. That is why you have to block / enable the signal.
        """

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
        """
        These refresh methods are there to update the combo box values based off of the kitsue json data.
        Remember any call to a widget that has a valid signal will call the widgets slot. That is why you have to block / enable the signal.
        """

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
        """
        This refresh isnt technically dependent on any other cobmo box as the tasks section is build by getting all the available tasks on kitsu
        This needs to eventually directly pull from the project to make it dynamic and only pull the tasks that are asigned to people
        """

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
        """
        Create the data in a combo box. At the moment it simple iterates through the list and assigns the label / value to an index in the list
        args:
        conbobox = a Qwidget.combobox 
        itemlist = a list of strings that you want to add into the combobox
        """

        if itemlist:

            for item in itemlist:
                combobox.addItem(item,item)
            return combobox
        else:
            print("there are no items in the itemlist")
            return None

        assettype = self.asset_type_box.currentData()
        asset = self.asset_box.currentData()
        
        path = proj_root / seq

        

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
       
    def detectImageSeq(self,filepath):
        """
        Detects if there is an image sequece for the given filepath and returns a dict of useful info:
        ARGS:
            filepath : (str) full path to file. 
        RETURNS : dict
        
        Keys:
            start   :start frame
            end     :end frame
            total   :total frames
            oiiop   :filepath for openimageIO padding
            ffmpegp : filepath for ffmpeg padding

        """

        #this is here just to quickly detect if the input path is a container format, and just skip this if it is
        video_formats = [".mp4",".mov",".avi"]

        filelist = []
        
        path = pathlib.Path(filepath)
        filename = path.name
        parent = path.parent

        if path.suffix in video_formats:
            return None

        #This looks for 1 group of of any series of 4 numbers together. Begins the search starting at the end of the string
        research = r"(\d{4})(?!.*\d)"

        #creates the regex patterns for searching. Splitting the search means that you are 99.9% certain that you will get the correct file
        split = re.split(research,filename)

        if len(split) == 1:
            return None

        #creating a more comprehensive pattern
        pattern = split[0] + r"(\d+)" + split[2]

        oiio =  split[0] + "#" + split[2]
        ffmpeg = split[0] + r"%04d" + split[2]

        oiiopath = str(parent / oiio)
        ffmpegpath = str(parent / ffmpeg)

        #builds the filelist for getting the start and end frames
        for child in parent.iterdir():

            match = re.search(pattern,str(child))
            
            try:
                frame = match.group(1)
                filelist.append(int(frame))
            except:
                None

        filelist.sort()
        
        start = filelist[0]
        end = filelist[-1]
        total = end - (start-1)

        filedict = {"start":start,"end":end,"total":total,"parentpath":parent,"oiiop":oiiopath,"ffmpegp":ffmpegpath}

        return filedict


    def submitToDailies(self):
        """
        The FFMPEG conversion.
        """
                
        input_path = self.select_file.text()
        
        if not input_path:
            QtWidgets.QMessageBox.critical(self, "Transcode Error", "Input path not set")
            return
        if not os.path.exists(input_path):
            QtWidgets.QMessageBox.critical(self, "Transcode Error", "Input path does not exist")
            return

        output_path = self.output_file.text()
        if not output_path:
            QtWidgets.QMessageBox.critical(self, "Transcode Error", "Output path not set")
            return

        pathdict = self.detectImageSeq(input_path)

        if pathdict == None:
            
            self.runFfmpegContainer(input_path,output_path)
        
        else:

            temppath = self.runOiio(pathdict)
            filedict = self.detectImageSeq(temppath)
            self.runFfmpegSeq(filedict["ffmpegp"],output_path)

    def runOiio(self,pathdict):
        # oiiotool basic command to export file and color convert
        # oiiotool --frames 1001-1050 --colorconvert "ACES - ACEScg" "Output - rec709" .\scientific_wizard_lodge_pangolin_lodge_test_v01_#.exr -ch R,G,B -o test.#.jpeg

        args = [self.OIIO]                                                                      #oiio path
        args.extend(["--frames",str(pathdict["start"]) + "-" + str(pathdict["end"])])           #globals
    
        if self.enable_col_man.isChecked():
            args.extend(["--colorconvert",self.from_space.currentData(),self.to_space.currentData()])                      #globals    
    
        args.extend([pathdict["oiiop"]])                                                        #input
        args.extend(["-ch","R,G,B"])                                                            #locals
        
        #create temp directory
        tempdir = pathdict["parentpath"] / "conversion_temp"
        if not tempdir.exists():
            tempdir.mkdir()
        
        args.extend(["-o",str(pathdict["parentpath"] / "conversion_temp" / "conversion_temp.#.png")])              #output    

        subprocess.call(args)

        QtWidgets.QMessageBox.information(self, "Transcode Complete", "File transcode operation complete.")

        temppath = str(tempdir / os.listdir(tempdir)[0])

        return temppath

    def runFfmpegSeq(self,input_path,output_path):

        preset = "medium"

        args = [self.FFMPEG]                                                    
        args.extend(["-hide_banner", "-y"])
        args.extend(["-start_number","1001","-framerate","24"])                                    
        args.extend(["-i", input_path ,"-i",self.LOGO])
        args.extend(["-filter_complex","[0]scale=1920:-2[mainscale];[1]scale=iw*.15:ih*.15[logo_scale];[logo_scale]lut=a=val*.2[logo_overlay];[mainscale][logo_overlay]overlay=(W-w):(H-h-20)[overlay];[overlay]drawtext=fontfile='\/\/YARN\/projects\/pipeline\/utilities\/fonts\/arial.ttf':text=%\{frame_num\}:start_number=1001:x=(w*0.05):y=(h*0.9):fontcolor=white@0.5:fontsize=50[final]"])
        args.extend(["-c:v", "libx264", "-crf", "23", "-preset", "medium","-r","24"])
        args.extend(["-map","[final]"])
        args.append(output_path)  
        
        subprocess.call(args)
        QtWidgets.QMessageBox.information(self, "Transcode Complete", "File transcode operation complete.")        
        
   
    def runFfmpegContainer(self,input_path,output_path):
        
        preset = "medium"

        args = [self.FFMPEG]                                                    
        args.extend(["-hide_banner", "-y"])                                    
        args.extend(["-i", input_path ,"-i",self.LOGO])
        args.extend(["-filter_complex","[0]scale=1920:-2[mainscale];[1]scale=iw*.15:ih*.15[logo_scale];[logo_scale]lut=a=val*.2[logo_overlay];[mainscale][logo_overlay]overlay=(W-w):(H-h-20)[overlay];[overlay]drawtext=fontfile='\/\/YARN\/projects\/pipeline\/utilities\/fonts\/arial.ttf':text=%\{frame_num\}:start_number=1001:x=(w*0.05):y=(h*0.9):fontcolor=white@0.5:fontsize=50[final]"])
        args.extend(["-c:v", "libx264", "-crf", "23", "-preset", "medium","-r","24"])
        args.extend(["-map","[final]"])
        args.append(output_path)  
        
        
        subprocess.call(args)
        QtWidgets.QMessageBox.information(self, "Transcode Complete", "File transcode operation complete.")
    



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


#ffmpeg cheat sheet
"""
to avoide any complications makes sure that the one output always is the input to the next filter [outfilter][outfilter]
ins and outs can only be used once in combination one out and one in
"""


""" overlay logo with scale and opacity """
# ffmpeg -hide_banner -y -i .\scn0010_cut0010_comp_v01.mp4 -i '\\YARN\projects\pipeline\utilities\images\logos\polycat_white_1024x1024.png' -filter_complex "[0]scale=1920:-2[mainscale];[1]scale=iw*.15:ih*.15[logo_scale];[logo_scale]lut=a=val*.2[logo_overlay];[mainscale][logo_overlay]overlay=(W-w):(H-h-20)[render]" -map "[render]" ./complex_filter_test.mp4
""" draw box for text clarity """
# ffmpeg -hide_banner -y -i .\scn0010_cut0010_comp_v01.mp4 -filter_complex "drawbox=y=ih*.9:color=black@0.4:width=iw:height=ih*0.1:t=fill" drawbox_test_v01.mp4
""" frame number overlay !!! remember to escape the slashes and colons in the path especially when in quotes"""
# ffmpeg -hide_banner -y -i .\scn0010_cut0010_comp_v01.mp4 -filter_complex "drawtext=fontfile='\/\/YARN\/projects\/pipeline\/utilities\/fonts\/arial.ttf':text=%{frame_num}:start_number=1001:x=(w*0.05):y=(h*0.9):fontcolor=white:fontsize=50" text_test_v01.mp4

""" all together - no draw box """
# ffmpeg -hide_banner -y -i .\scn0010_cut0010_comp_v01.mp4 -i '\\YARN\projects\pipeline\utilities\images\logos\polycat_white_1024x1024.png' -filter_complex "[0]scale=1920:-2[mainscale];[1]scale=iw*.15:ih*.15[logo_scale];[logo_scale]lut=a=val*.2[logo_overlay];[mainscale][logo_overlay]overlay=(W-w):(H-h-20)[overlay];[overlay]drawtext=fontfile='\/\/YARN\/projects\/pipeline\/utilities\/fonts\/arial.ttf':text=%{frame_num}:start_number=1001:x=(w*0.05):y=(h*0.9):fontcolor=white@0.5:fontsize=50[final]" -map "[final]" .\allsettings.mp4