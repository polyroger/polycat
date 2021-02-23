import pymel.core as pm
import maya.cmds as cmds
from pc_maya.maya_helpers import export_helpers
from pc_maya.snippets import snippets


def createStructure(justgeo,groupname,freezetrans,delhistory):
    """
    Creates the correct stucture for exporting geometry.
    Used with the model prep dialog.
    """
    """
    model prep needs to create a group for each refernece
    the group needs to be names with the refname + refversion
    if it fails everything must go back to what it was.

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
        
        asset = pm.group(empty=True,world=True,n=assetname)
        asset.addAttr("referenceVersion",dt="string")
        
        #nested to prevent suffixing _geo on the GGRP
        for i in selectedgeo:
            #if its a transform node, it doesnt have a shape and it is not a reference
            if i.nodeType() == "transform" and i.getShape() == None and not cmds.referenceQuery(i.name(), inr=True) :
                print("The selected node is a group, skipping _geo suffix")
                pm.parent(i,transgroup)
            
            elif cmds.referenceQuery(i.name(), inr=True):
                ref_version = export_helpers.getReferenceVersion(i.name())
                if ref_version:
                    ref_name = export_helpers.stripNameSpace(i.name()).replace("_GGRP", "") + ref_version
                    ref_group = pm.group(i, parent=transgroup, name=ref_name )
                else:
                    cmds.confirmDialog(title="ERROR", message="If you are prepping references, each reference needs to have a unique reference version attribute. Please set this in the reference group")
                    i.parent(world=True)
                    pm.delete(transgroup)
                    pm.delete(asset)
                    return
            
            else:
                snippets.addGeoSuffix(i,geosuffix)
            
                pm.parent(i,transgroup)

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