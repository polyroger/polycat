import pymel.core as pm
from pc_maya.helpers.export_helpers import export_helpers
from pc_maya.snippets import snippets


def createStructure(justgeo,groupname,freezetrans,delhistory):
    """
    Creates the correct stucture for exporting geometry.
    Used with the model prep dialog.
    """
    
    namesuffix = "_GGRP"
    transname = "SRT"
    geosuffix = "_geo"

    selectedgeo = pm.ls(selection=True)

    if justgeo:
        for i in selectedgeo:
            snippets.addGeoSuffix(i,geosuffix)
    else:

        try:
            assetname = groupname + namesuffix
        except:
            assetname = "no group name " + namesuffix
    

        transgroup = pm.group(empty=True,world=True,n=transname)
        
        #nested to prevent suffixing _geo on the GGRP
        for i in selectedgeo:
            
            if i.nodeType() == "transform" and i.getShape() == None:
                print("The selected node is a group, skipping _geo suffix")
            
            else:
                snippets.addGeoSuffix(i,geosuffix)
            
                pm.parent(i,transgroup)

        asset = pm.group(empty=True,world=True,n=assetname)
        asset.addAttr("referenceVersion",dt="string")

        pm.parent(transgroup,asset)

        #freeze transforms and delete history
        
        if freezetrans:
            pm.makeIdentity(transgroup,apply=True)
        else:
            print("Transforms preserved")
        
        if delhistory:
            pm.delete(selectedgeo,ch=True)
        else:
            print("History Preserved")

        exportset = export_helpers.createExportSet()
        exportset.add(asset)