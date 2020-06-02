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


   

