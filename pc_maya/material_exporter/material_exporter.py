"""
Polycat animations maya scene exporter

"""
import sys,os,json,logging
import maya.cmds as cmds
from pc_helpers import pc_file_helpers as pfh

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
    """
    selects dag objects, only objects not connections and shapes from the currently selected object
    """
    selection = cmds.ls(dag=True,o=True,s=True,sl=True)
    if selection:
        return selection
    else:
        Pc_Logger.warning("The selection is empty, returning None")
        return None


def get_assigned_shaders(selection):
    """
    Gets all the assigned shaders for the selected geometry
    Return (set) : a filtered set of shader names assigned to the selected geometry
    """
    if not selection:
        Pc_Logger.error("Nothing has been selected")
        return None
    
    try:
        shading_grps = cmds.listConnections(selection,type='shadingEngine')
        all_shaders = cmds.ls(cmds.listConnections(shading_grps),materials=True)
        filtered_shaders = set(filter(filter_shaders,all_shaders))

    except:
        Pc_Logger.error("Error getting the asigned shaders")
        return None
    
    if filter_shaders:
        return filtered_shaders
    else:
        Pc_Logger.error("There are no shaders assigned")
        return None

def create_mesh_list(shader,selection):

    assigned_list = []
    
    #get the meshes return as a list,!! OUTCOLOR IS THE SHADERS OUTPUT NOT THE BASECOLOR OF THE SHADER !!
    if cmds.listConnections("{0}.outColor".format(shader))[0] in assigned_list:
        pass
    else:
        assigned = cmds.listConnections("{0}.outColor".format(shader))[0]
        assigned_list.append(assigned) 
    
    transforms = cmds.listRelatives(selection,type="transform",p=True)
    all_meshes = cmds.listConnections(assigned,type="mesh")
    
    mesh_list = []
    for node in all_meshes:
        if node in transforms:
            mesh_list.append(node)
        else:
            Pc_Logger.warning("skipping {} as it is not in the current selections".format(node))
    
    return mesh_list

def create_shader_parm_dict(shader,shader_parms):
    """
    Given a shader and a paramater list, get all the values of those paramaters
    Returns a dictionary mapping of the paramaters and thier values.
    """
    parm_dict = {}
    value = None
    print(shader)
    for parm in shader_parms:

        file_parm_connections = cmds.listConnections("{0}.{1}".format(shader,parm), p=False, type="file")
        all_parm_connections = cmds.listConnections("{0}.{1}".format(shader,parm), p=False)
        is_destination = cmds.connectionInfo("{0}.{1}".format(shader,parm),isDestination=True)

        #checks plugs for files plugged into parms
        if file_parm_connections:
            file_node = file_parm_connections[0]
            node_tex_path = str(cmds.getAttr("{0}.fileTextureName".format(file_node)))
            server_tex_path = pfh.create_server_location(node_tex_path).replace("\\","/")
            
            if pfh.udim_check(server_tex_path): # checking for udim
                value = os.path.realpath(pfh.replace_udim_filepath(server_tex_path,"<udim>")).replace("\\","/") # the \ confuses arnold in houdini
            else:
                value = server_tex_path
        
        #this should be its own function.
        #checks plugs for nodes that arent files ( normal map ) and have somthing plugged in
        # at the end of this there should be a dict with paths set for the 3 potential states, I am using the height dict key|value in houdini to determine
        # whether or not to use the bump or normal node.
        elif not file_parm_connections and is_destination:
            connected_node = all_parm_connections[0]
            #handling normal node
            # if a normal map is connected, it can have two potential inputs( input and normal). input is required but normal is not.
            if cmds.nodeType(connected_node) == "aiNormalMap":
                print("normal map connected")
                node_in_input = cmds.listConnections("{}.input".format(connected_node))[0]
                try:
                    node_in_normal = cmds.listConnections("{}.normal".format(connected_node))[0]
                except:
                    node_in_normal = None
                
                # handling the normal nodes input paramater
                if node_in_input:
                    input_filepath = cmds.getAttr("{0}.fileTextureName".format(node_in_input))
                    input_server_path = pfh.create_server_location(input_filepath).replace("\\","/")
                    if pfh.udim_check(input_server_path): # checking for udim
                        normal_input = os.path.realpath(pfh.replace_udim_filepath(input_server_path,"<udim>")).replace("\\","/") # the \ confuses arnold in houdini)
                    else:
                        normal_input = input_server_path
                else:
                    print("No map is plugged into the {} input".format(shader))
                    normal_input = None
                
                # handling the normal nodes normal paramater
                if node_in_normal and cmds.nodeType(node_in_normal) == "file":
                    normal_filepath = cmds.getAttr("{0}.fileTextureName".format(node_in_normal))
                    normal_server_path = pfh.create_server_location(normal_filepath).replace("\\","/")
                    if pfh.udim_check(normal_server_path): # checking for udim
                        normal_height = os.path.realpath(pfh.replace_udim_filepath(normal_server_path,"<udim>")).replace("\\","/") # the \ confuses arnold in houdini)
                    else:
                        normal_height = normal_server_path
                else:
                    print("No map is plugged into the {} input".format(shader))
                    normal_height = None
                    
                height = None
            
                value = {"normal_input": normal_input, "normal_height": normal_height, "height": height}
            
            # handling height node
            elif cmds.nodeType(connected_node) == "aiBump2d":
                print("height map is connected")
                print(connected_node)
                height_file_node = cmds.listConnections("{}.normal".format(connected_node))[0]
                if height_file_node and cmds.nodeType(height_file_node) == "file":
                    height_filepath = cmds.getAttr("{0}.fileTextureName".format(height_file_node))
                    height_server_path = pfh.create_server_location(height_filepath).replace("\\","/")
                    if pfh.udim_check(height_server_path): # checking for udim
                        height = os.path.realpath(pfh.replace_udim_filepath(height_server_path,"<udim>")).replace("\\","/") # the \ confuses arnold in houdini)
                    else:
                        height = height_server_path
                else:
                    height = None
                
                normal_height = None
                normal_input = None
                height = "TODO: make sure that the udim normal texture path is loaded here"
                
                value = {"normal_input": normal_input, "normal_height": normal_height, "height": height}
            else:
                print("Niether a normal map or a height map is connected to the paramater, make sure that you are using a file node")
                normal_input = None
                normal_height = None
                height = None
                value = {"normal_input": normal_input, "normal_height": normal_height, "height": height}

        #checks for parms that dont have anything connected to them
        elif not is_destination:
            if parm == "normalCamera": # users shouldnt be manaully setting the normal
                value = None
                parm_dict[parm] = value # just setting this here so that the dict gets updated before the continue
                continue
            if isinstance(cmds.getAttr("{0}.{1}".format(shader,parm)),list): #if nothing is plugged in and the value is a color this prevents value from being a nested list
               value = cmds.getAttr("{0}.{1}".format(shader,parm))[0]
            else:
                value = cmds.getAttr("{0}.{1}".format(shader,parm))

        #catches everything that is not accomodated for.
        else:
            print("there is somthing plugged in {0} that isnt a file node".format(parm))
            value = None

        parm_dict[parm] = value

    return parm_dict        

def create_shader_engine_dict(shader, shader_engine_parms):

    shader_engine_dict = {}
    engine = cmds.listConnections("{}.outColor".format(shader))[0]

    for parm in shader_engine_parms:
        
        file_parm_connections = cmds.listConnections("{0}.{1}".format(engine,parm), p=False, type="file")
        is_destination = cmds.connectionInfo("{0}.{1}".format(engine,parm),isDestination=True)
        
        if engine and is_destination: # is somthing connected
            if file_parm_connections: # is it a file node
                file_node = file_parm_connections[0] # sets the first found file node as the value
                file_path = str(cmds.getAttr("{0}.fileTextureName".format(file_node)))
                server_tex_path = pfh.create_server_location(file_path).replace("\\","/")

                if pfh.udim_check(server_tex_path):
                    value = pfh.replace_udim_filepath(server_tex_path,"<udim>")
                else:
                    value = server_tex_path

            else:
                value = None
        else:
            value = None

        shader_engine_dict[parm] = value

        return shader_engine_dict


def create_material_dict(shader_list,selection):
    """
    Creates a material dictionary that consists of a list of objects a shader is assigned to, a shader paramater dict, a shading engine dict
    Returns (dict) : A dict with keys for [ objects, shader_parms, shading_engine_parms]
    """
    materials = {}
    
    shader_parms = [
        "baseColor",
        "metalness",
        "specularRoughness",
        "transmission",
        "normalCamera",
        ]

    shading_engine_parms = [
       "displacementShader"
        ]

    for shader in shader_list:
       
        mesh_list = create_mesh_list(shader,selection)
        shader_parm_dict = create_shader_parm_dict(shader,shader_parms)
        shader_engine_parm_dict = create_shader_engine_dict(shader,shading_engine_parms)
          
        # created the dictionary entries for each assigned shader
        materials[shader] = {"objects":mesh_list,"shader_parms":shader_parm_dict, "shader_engine_parms":shader_engine_parm_dict}

    return materials


def write_material_json(materail_dict,export_path):
    """
    Creates a json object from the material dict and writes is to export_path.
    """
    if not export_path:
        Pc_Logger.error("The export path is invalid")
        
        return None
    try:
        with open(export_path,"w") as f:
            data = json.dumps(materail_dict,indent=4)
            f.seek(0)
            f.write(data)
        
        return True
    except IOError:
        Pc_Logger.exception("Could not write the json file")
        
        return None

def run_material_export(export_path):
    """
    Runs the material export from maya
    """
    selection = get_selection()
    if selection:
        shaders = get_assigned_shaders(selection)
        mat_dict = create_material_dict(shaders, selection)
        jfile = write_material_json(mat_dict, export_path)
        if not jfile:
            Pc_Logger.error("The material decriptions could no be exported")
            return None
        Pc_Logger.info("Material descriptions exported successfully")
        return mat_dict
    else:
        Pc_Logger.error("The material decriptions could no be exported")
        return None