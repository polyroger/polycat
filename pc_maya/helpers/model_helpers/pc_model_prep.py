import pymel.core as pm
from pc_maya.helpers.export_helpers import export_helpers

def createStructure(groupname="no_group_specified"):
    """
    Creates the correct stucture for exporting geometry.
    Expexts a string as an input to the groupname kwarg EG : createStructure(groupname="rocks")
    """
    
    namesuffix = "_GGRP"
    transname = "SRT"
    geosuffix = "_geo"

    selectedgeo = pm.ls(selection=True)

    try:
        assetname = self.export_prep_name.text() + namesuffix
    except:
        assetname = groupname + namesuffix
 

    transgroup = pm.group(empty=True,world=True,n=transname)
    
    #nested to prevent suffixing _geo on the GGRP
    for i in selectedgeo:
        
        if i.nodeType() == "transform" and i.getShape() == None:
            print("The selected node is a group, skipping _gep suffix")
        
        else:

            if not "_geo" in i.name():
                i.rename(i.name() + geosuffix)

        pm.parent(i,transgroup)

    asset = pm.group(empty=True,world=True,n=assetname)
    asset.addAttr("referenceVersion",dt="string")

    pm.parent(transgroup,asset)

    #freeze transforms and delete history
    pm.makeIdentity(transgroup,apply=True)
    pm.delete(selectedgeo,ch=True)

    exportset = export_helpers.createExportSet("EXPORTSET")
    exportset.add(asset)