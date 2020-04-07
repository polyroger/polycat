# General helper functions

def mayaMainWindow():
    """
    Helper function that returns a python object for maya's main window, so that you can use this python object as the parent for qt widgets 
    in maya.
    """
    mainwindowpointer = omui.MQtUtil.mainWindow()
    mainwindowobject = wrapInstance(long(mainwindowpointer),QtWidgets.QWidget)

    return mainwindowobject

def refreshPysideTableWidget():
    print("TODO: implement the table refresh")

    self.geo_table.setRow
    self.cam_table
