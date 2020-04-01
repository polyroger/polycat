import pymel.core as pm

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
        name = self.export_prep_name.text() + namesuffix
    except:
        name = groupname + namesuffix
 

    transgroup = pm.group(empty=True,world=True,n=transname)
    
    #nested to prevent suffixing _geo on the GGRP
    for i in selectedgeo:
        
        if i.nodeType() == "transform" and i.getShape() == None:
            print("this is a group bitches")
        
        else:

            if not "_geo" in i.name():
                i.rename(i.name() + geosuffix)


            
        
        pm.parent(i,transgroup)

    asset = pm.group(empty=True,world=True,n=name)
    pm.parent(transgroup,asset)