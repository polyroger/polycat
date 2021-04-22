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


def pcABCCameraArgs(rootname,filepath,start,end,userattrlist=None,step=str(1.0)):
    """
    Built for abc camera exporters, this skips things like namespace and reference checks
    Args 
    rootname: str the name of the root object in the maya outliner
    filepath: str the full filepath including the filename and extension of the file to export
    start: int start frame
    end: int end frame
    userlist: str list of custom user attributes defaults to None
    step: float The frame subsampling defaults to 1.0

    return: str of the command (j) argument for the AbcExporter
    """
    
    exportargs = ["-root",rootname]
    exportargs.extend(["-file",filepath])
    exportargs.extend(["-framerange",str(start-1),str(end+1)])
    exportargs.extend(["-step",step])
    
    if userattrlist:
        for attr in userattrlist:
            exportargs.extend(["-userAttr",attr])
    
    exportargs.extend(["-worldspace","-eulerFilter","-stripNamespaces"])

    command = " ".join(exportargs)
    
    return command


def createExportSet():

    EXPORTSET = "EXPORTSET"
    setname = EXPORTSET

    try:
        exportset =  pm.ls(setname)[0]
        
        return exportset           
    
    except:
        print("the set does not exist, creating a new set")
        exportset = pm.sets(em=True,n=setname)
        
        return exportset

def create_rig_export_set():

    EXPORTSET = "RIGEXPORTSET"
    setname = EXPORTSET

    try:
        exportset =  pm.ls(setname)[0]
        
        return exportset           
    
    except:
        print("the set does not exist, creating a new set")
        exportset = pm.sets(em=True,n=setname)
        
        return exportset


def getExportSet():

    EXPORTSET = "EXPORTSET"
    setname = EXPORTSET

    try:
        exportset = pm.ls(setname)
        return exportset[0]
    except:
        print("Export Set could not be found")
        return False

def getExportList(table):

    print ("export list cleared")
    exportlist = []

    for i in range(table.rowCount()):

        exportme = table.item(i,0)
        exportitem = table.item(i,1)

        if exportme.checkState() == QtCore.Qt.Checked:
            exportlist.append(exportitem)
            print("{0} added to abc export list".format(exportitem.text()))
        else:
            print("{0} not added to abc export list".format(exportitem.text()))
    
    return exportlist  

def stripNameSpace(name):
    
    if ":" in name:
        nons = name.split(":")[-1]
        return nons
    else:
        return name

def getReferenceVersion(nodename):
    """
    Expexts the name of the node that contains the referenceVersion attribute
    """
    reference = pm.ls(nodename)[0]
    
    try:
        getver = reference.referenceVersion.get()
        
        if getver:
            refver = "_" + getver
            return refver
        else:
            return ""
    except:
        print("There is no ref version attr, returning an empty string")
        return ""

def getItemValue(item):
    return item.data(self.VALUE_ROLE)

def getFrameRanges():
    """
    Returns a tuple of (int playbackstart, int playbackend)
    """

    start = int(pm.playbackOptions(query=True, min=True) - 1)
    end = int(pm.playbackOptions(query=True, max=True))

    return (start,end)

def checkBoxStateBool(checkboxitem):
    """
    Returns True or False depening on whether a pyside2 checkbox is checked or not rather that a pyside2 state
    """
    if checkboxitem.checkState() == QtCore.Qt.CheckState.Checked:
        return True
    else:
        return False


   

