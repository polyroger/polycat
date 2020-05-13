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

def freezeTransforms():
    print("freeze me")  

def deleteHistory():
    print("delete my history") 

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
    getver = reference.referenceVersion.get()

    if getver:
        refver = "_" + getver
        return refver
    else:
        print("No referenceVersion attrubute value was found, returing an empty string")
        return ""

def getItemValue(item):
    return item.data(self.VALUE_ROLE)


   

