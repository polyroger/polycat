"""
Polycats Houdini previs geometry exporter

"""
import os
import hou

def getSetShot():
    
    obj = hou.node("/obj")

    for node in obj.children():
        
        if node.type().nameComponents()[2] == "pc_set_shot":
            
            ss = node
            
            return ss

        else:
            hou.ui.displayConfirmation("Could not find the set shot", title="error")
            return None

def getCutName(subnetpath):

    subnet = hou.node(subnetpath)
    
    return subnet.name()


def checkSubnet(root,setshot,seqpath,subnetname):
    
    if setshot:
    
        cutlevel = root + seqpath
    
        if subnetname not in os.listdir(cutlevel):

            hou.ui.displayConfirmation("The subnet cut name is not a shot in the sequence",title="ERROR")

            return False

        else:
            return True

    print("there was an errot in the checkSubnet()")
    
    return None

def getRopnet():

    for node in hou.node(".").children():
        print(node)
        if node.name() == "ropnet1":
            abcrop = node.children()[0]
            return abcrop
        else:
            return None




