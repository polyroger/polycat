import sys, os
import maya.cmds as cmds
from pc_maya.maya_helpers import scene_helpers
from pc_helpers import pc_file_helpers

def get_all_references():
    """
    Gets all the references in a maya scene
    
    Returns (list): A list of reference nodes
    """

    all_ref_nodes = cmds.ls(type="reference")

    return all_ref_nodes

def update_reference_check():
    """
    Does a check to see if a reference node in the scene is at the latest version or not
    args
    reference_node (str): A maya reference node name
    """
    
    nodes_to_update = []
    all_nodes = cmds.ls(type="reference")
    for node in all_nodes:
        if node == "sharedReferenceNode":
            continue

        node_path = cmds.referenceQuery(node, f=True)
        node_dir = os.path.dirname(node_path)
        dir_contents = os.listdir(node_dir)
        node_version = pc_file_helpers.extract_version(node_path)
        latest_version = pc_file_helpers.getLatestFromList(dir_contents)

        if latest_version > node_version:
            nodes_to_update.append(node)
    
    return nodes_to_update

def update_reference(reference_node):
    """
    updates references to the latest version.
    """
    node_path = cmds.referenceQuery(reference_node, f=True)
    node_dir = os.path.dirname(node_path)
    dir_contents = os.listdir(node_dir)
    node_version = pc_file_helpers.extract_version(node_path)
    latest_version = pc_file_helpers.getLatestFromList(dir_contents)

    update = cmds.confirmDialog(title="Update References", message="One of your references, {0} are not on its latest version, would you like to update them ?".format(reference_node), button=["Update", "Ignore"], defaultButton="Ignore", cancelButton="Ignore", dismissString="Ignore") 
    
    if update == "Update":
        latest_file = pc_file_helpers.getLatestFile(dir_contents)
        new_ref_path = os.path.join(node_dir, latest_file).replace("\\","/")
        
        if os.path.isfile(new_ref_path):
            cmds.file(new_ref_path, lr=reference_node)
            cmds.confirmDialog(title="Updated Reference", message="Reference {0} updated from v{1} to v{2}".format(reference_node, node_version, latest_version), button=["Nice!"])
            
            return new_ref_path
        else:
            print("There was an error updating the reference node {0}".format(reference_node))
            
            return node_path
    
    else:
        return None


def run_reference_update():

    all_nodes = cmds.ls(type="reference")
    nodes_to_update = update_reference_check()
    
    if nodes_to_update:
        for node in nodes_to_update:
            update_reference(node)
        
        cmds.confirmDialog(title="All Up To Date", message="All Reference Nodes Have Been Updated", button=["Woohoo!"])
        return True


def run_reference_update_menu():

    all_nodes = cmds.ls(type="reference")
    nodes_to_update = update_reference_check()
    
    if nodes_to_update:
        for node in nodes_to_update:
            update_reference(node)
    else:
        cmds.confirmDialog(title="All Nodes Updated", message="There are no reference nodes that need to be updated", button=["Nice!"])
    


    


    