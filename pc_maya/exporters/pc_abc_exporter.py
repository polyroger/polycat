#fix the model prep to always make the correcy heireacy
# get all the objests in the scene that are in the correct heiracy 
# add those objects to the table in the gui
# autofill out the lineedit in the gui to the path
# in a loop exporalembics for all the items returned by the getallexportobjects

import os
import pymel.core as pm
from pc_maya.helpers.export_helpers import export_helpers
from pipeline_utilities import path_manipulation
from pipeline_utilities import file_manipulation


def pcAbcExporter(rootname,assetpath,start,end,single):

    print ("running export")

    if single:
        start = 1
        end = 1
    
    #pm.AbcExport(help=True)   use this in maya for the pm.AbcExporter help

    ext = ".abc"
    
    stripns = export_helpers.stripNameSpace(rootname)
    refversion = export_helpers.getReferenceVersion(rootname)
    exportname = stripns.replace("_GGRP", "")

    exportpath = path_manipulation.checkForPath(assetpath,exportname,refversion)
    refattr = "referenceVersion"

    latest = file_manipulation.getLatestVersion(exportpath,exportname)
    latestplus = file_manipulation.versionPlusOne(latest)
    
    exportgeoflag = "-root " + rootname
    exportpathflag = "-file " + exportpath + "\\"  + exportname + refversion + latestplus + ext
    exportrangeflag = "-framerange " + str(start) + " " + str(end)   
    exportattrflag = "-userAttr " + refattr
    
    exportflags = exportgeoflag + " " + exportpathflag + " " + "-worldspace -eulerFilter -stripNamespaces -uv" + " " + exportrangeflag + " " + exportattrflag


    print (exportflags)
    pm.AbcExport(j=exportflags)
     

    