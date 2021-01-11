"""
Polycat animations maya scene exporter

"""
import sys,os,json,logging
import maya.cmds as cmds

# getting to the logging module
sys.path.append(os.path.join(__file__,"../../../"))
from pipeline_utilities.pc_logging.pc_logger import Pc_Logger

Pc_Logger.set_log_level(logging.DEBUG)


# texture and shader prep
def filter_shaders(shader):
    """
    Filter used to exclude all shaders other that the aiStandardSurface
    """
    return cmds.objectType(shader,isType="aiStandardSurface")

def get_selection():

    selection = cmds.ls(dag=True,o=True,s=True,sl=True)

    return selection


def get_assigned_shaders(selection):
    """
    Gets all the assigned shaders for the selected geometry
    Return (set) : a filtered set of shader names assigned to the selected geometry
    """
    if not selection:
        Pc_Logger.error("Nothing has been selected")
        return False
        
    shading_grps = cmds.listConnections(selection,type='shadingEngine')
    all_shaders = cmds.ls(cmds.listConnections(shading_grps),materials=True)
    filtered_shaders = set(filter(filter_shaders,all_shaders))

    return filtered_shaders

def create_material_dict(shader_list,selection):
    """
    Creates a material dictionary entry for each shader in shader_list.
    Returns (dict) : A dict with keys for [ objects, color, texture ]
    """
    materials = {}
    assigned_list = []
    
    for shader in shader_list:
        
        #get the meshes return as a list,!! OUTCOLOR IS THE SHADERS OUTPUT NOT THE BASECOLOR OF THE SHADER !!
        if cmds.listConnections("{0}.outColor".format(shader))[0] in assigned_list:
            continue
        else:
            assigned = cmds.listConnections("{0}.outColor".format(shader))[0]
            assigned_list.append(assigned) 
        
        transforms = cmds.listRelatives(selection,type="transform",p=True)
        all_meshes = cmds.listConnections(assigned,type="mesh")
        mesh = []
        for node in all_meshes:
            if node in transforms:
                mesh.append(node)
            else:
                Pc_Logger.warning("skipping {} as it is not in the current selections".format(node))

        

        # sets the texture and color attributes
        if cmds.connectionInfo("{0}.baseColor".format(shader),isDestination=True):
            color = "texture"
            file_node = cmds.listConnections("{0}.baseColor".format(shader),type="file")[0]
            texture = cmds.getAttr("{0}.fileTextureName".format(file_node))
        else:
            color = cmds.getAttr("{0}.baseColor".format(shader))[0]
            texture = "color"
        
        # created the dictionary entries for each assigned shader
        materials[shader] = {"objects":mesh,"color":color,"texture":texture}

    return materials

def write_material_json(materail_dict,export_path):
    """
    Creates a json object from the material dict and writes is to export_path.
    """
    try:
        with open(export_path,"w") as f:
            data = json.dumps(materail_dict,indent=4)
            f.seek(0)
            f.write(data)
        
        return True
    except IOError:
        Pc_Logger.exception("Could not write the json file")
        
        return False
        