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

def createExportSet(setname):
    try:
        exportset =  pm.ls(setname)[0]
        
        return exportset           
    
    except:
        print("the set does not exist, creating a new set")
        exportset = pm.sets(em=True,n=setname)
        
        return exportset

   

def pc_ABCExporter():
    print("this is the pc_ABCExporter from export helpers")