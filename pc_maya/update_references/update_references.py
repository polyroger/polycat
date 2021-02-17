import sys, os
import maya.cmds as cmds
from pc_maya.maya_helpers import scene_helpers
from pc_helpers import pc_file_helpers

def printmap(n):
    """
    used to map list values and print them out in new lines with the .format method
    """
    print(n)

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
    
    Returns (list) : A list of strings, each string being the name of a reference node that can be updated
    """
    
    nodes_to_update = []
    all_nodes = get_all_references()
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

def get_latest_reference_path(node):
    
    node_path = cmds.referenceQuery(node, f=True)
    node_dir = os.path.dirname(node_path)
    dir_contents = os.listdir(node_dir)
    updated_path = os.path.join(node_dir,pc_file_helpers.getLatestFile(dir_contents)).replace("\\","/")

    return updated_path

def update_one(node, latest_reference_path):
    """
    This function is desigend to run in a loop
    """
    print("Updating one")
    latest = cmds.file(latest_reference_path, lr=node)
    
    return latest


def ignore_one():
    print("ignoring one")   
    return

def update_all(reference_node_list):
    """
    Update all nodes in the list
    """
    for node in reference_node_list:
        updated_path = get_latest_reference_path(node)
        update_one(node, updated_path)
    
    cmds.confirmDialog(title="Referece Status", message="There are no more references that need to be updated", button=["WooHoo!"])


def ignore_all():
    print("Ignoring All Reference Updates")
    return


def update_reference(reference_node_list, run_from="scriptJob"):
    """
    updates references to the latest version.
    ARGS
    reference_node_list (list): A list of reference node names
    KWARGS
    run_from (str): one of "scriptJob" or "menu". This is really just to skip the dialog when run from a script job
    """
    # makes sure that the reference list is not empty
    if not reference_node_list:
        print("running not reference node")
        if run_from == "scriptJob":
            update = "running as script job"
        elif run_from == "menu":
            cmds.confirmDialog(title="References Uptodate", message="No references need to be updated", button=["Nice!"])
            update = None
    else:
        update = cmds.confirmDialog(title="Update References", message="These references need to be updated,\n\n{0}\n\nWould you like to update them ?".format("\n".join(str(x) for x in reference_node_list)), button=["I will Choose","Update All", "Ignore All"], defaultButton="Ignore", cancelButton="Ignore", dismissString="Ignore")
    
        if update == "Ignore All":
            ignore_all()
            return
        
        elif update == "Update All":
            update_all(reference_node_list)
            return
        
        elif update == "I will Choose":
            for node in reference_node_list:
                updated_path = get_latest_reference_path(node)
                response = cmds.confirmDialog(title="Reference {0}", message="{1}\n\ncan be updated to :\n\n{2}".format(node, node, updated_path), button=["Update", "Ignore"])

                if response == "Update":
                    update_one(node, updated_path)
                elif response == "Ignore":
                    ignore_one()
                else:
                    cmds.confirmDialog(title="Reference Error", message="There was an error when attempting to update {0}")
            
            cmds.confirmDialog(title="Referece Status", message="There are no more references that need to be updated", button=["WooHoo!"])
        
        else:
            print("there as an error")


def run_reference_update(context):
    """
    context is one of either "scriptJob" or "menu"
    """
    print(context)
    reference_node_list = update_reference_check()
    update_reference(reference_node_list, run_from=context)


            


        
            


    


    


    