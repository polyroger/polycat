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

def getCutName(subnetpath):

    subnet = hou.node(subnetpath)
    
    return subnet.name()


#not yet implemented
def checkIfPathExists(path):

    if os.path.exists(path):
        answer = hou.ui.displayConfirmation("That folder version already exists, are you sure you want to export?",title="WARNING")
        return answer

def createPath(path):

    if not os.path.exists():
        
        path = os.mkdir(path)
        
        return path

    else:
       
       hou.ui.displayMessage("The export path could not be created")

       return None



