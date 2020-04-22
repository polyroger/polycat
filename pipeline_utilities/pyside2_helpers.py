# General helper functions

def mayaMainWindow():
    """
    Helper function that returns a python object for maya's main window, so that you can use this python object as the parent for qt widgets 
    in maya.
    """
    mainwindowpointer = omui.MQtUtil.mainWindow()
    mainwindowobject = wrapInstance(long(mainwindowpointer),QtWidgets.QWidget)

    return mainwindowobject

def refreshPysideTableWidget(self,table,tablelist):
    """
    Takes in a table and a list of items, sets the rows to 0 then re builds the rows from the list.\n
    First argument : a table object \n
    Second argument : a list of row entries
    """

    print("Running table refresh")
    
    table.setRowCount(0)
    for i in range(len(tablelist)):
        table.insertRow(i)

