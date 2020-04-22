from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as cmds


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


class OutputResolutionDialog(QtWidgets.QDialog):

    DATA = [["HD",1920.0,1080.0],["720p",1280.0,720.0]]

    def __init__(self, parent=maya_main_window()):
        super(OutputResolutionDialog, self).__init__(parent)

        self.setWindowTitle("Output Resolution")
        self.setFixedWidth(220)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        
        self.resolution_list_wdg = QtWidgets.QListWidget()

        for i in self.DATA:

            item = QtWidgets.QListWidgetItem(i[0])
            item.setData(QtCore.Qt.UserRole,[i[1],i[2]])
            self.resolution_list_wdg.addItem(item)


        # self.resolution_list_wdg.addItems(["1920x1080 (1080p)","1280x720 (720p)","960x540 (540p)"])
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.resolution_list_wdg)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.resolution_list_wdg.itemClicked.connect(self.setOutputResolution)
        self.close_btn.clicked.connect(self.close)

    def setOutputResolution(self, item):
        print(item.data(QtCore.Qt.UserRole)[0])
        print("resoution {0}".format(item.text()))


if __name__ == "__main__":

    try:
        output_resolution_dialog.close() # pylint: disable=E0601
        output_resolution_dialog.deleteLater()
    except:
        pass

    output_resolution_dialog = OutputResolutionDialog()
    output_resolution_dialog.show()
