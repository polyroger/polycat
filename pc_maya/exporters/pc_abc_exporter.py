"""
Polcat maya alembic exporter
"""

import os
import pymel.core as pm

from pc_maya.maya_helpers import export_helpers
from pc_helpers import pc_path_helpers as pathhelp
from pc_helpers import pc_file_helpers as filehelp


def pcAbcExporter(rootname,assetpath,start,end,single):
    """
    nested referenced objects will have the same name once the namespace is stored
    this is handled in the getReferenceVersion on the main group node but not on any of the child nodes.
    step through children, check if it is a reference if it is check then check the reference version and augment the name
    try only do this if there is going to be a confilct rather than on every one.

    """

    print ("running export")

    if single:
        start = 1
        end = 1
    
    #pm.AbcExport(help=True)   use this in maya for the pm.AbcExporter help

    ext = ".abc"
    
    stripns = export_helpers.stripNameSpace(rootname)
    refversion = export_helpers.getReferenceVersion(rootname)
    exportname = stripns.replace("_GGRP", "")

    exportpath = pathhelp.checkForPath(assetpath,exportname,refversion)
    refattr = "referenceVersion"

    latest = filehelp.getLatestVersion(exportpath,exportname)
    latestplus = filehelp.versionPlusOne(latest)
    
    exportgeoflag = "-root " + rootname
    exportpathflag = "-file " + exportpath + "\\"  + exportname + refversion + latestplus + ext
    exportrangeflag = "-framerange " + str(start) + " " + str(end)   
    exportattrflag = "-userAttr " + refattr
    abcflags = "-worldspace -eulerFilter -stripNamespaces -uv -wv"
    
    sep = " "
    flaglist = [exportgeoflag,exportpathflag,abcflags,exportrangeflag,exportattrflag]
    exportflags = sep.join(flaglist)

    print (exportflags)
    pm.AbcExport(j=exportflags)
   



    