import json
import hou
import os

def read_pc_material(pcmatfile):
    """
    Reads the material file and outputs a python dict
    """
    with open(pcmatfile, mode="r") as f:
        matdict = json.load(f)

    return matdict

def make_prim_groups(matdict):
    
    prim_groups = matdict.keys()
    node = hou.pwd()
    geo = node.geometry()
    
    for group in prim_groups:
        prim_group = geo.createPrimGroup(group)
        for shape in matdict[group]["objects"]:
            add_group = geo.findPrimGroup(shape)
            print(add_group)
            prim_group.add(add_group)

def create_default_shader(shop):
    
    vopnode = shop.createNode("arnold_vopnet", "default_shader")
    out_material = hou.node(vopnode.path()+"/OUT_material")
    standard_surface = vopnode.createNode("arnold::standard_surface","base")
    out_material.setInput(0,standard_surface,0)

    standard_surface.parm("base").set(1)
    standard_surface.parm("base_colorr").set(.75)
    standard_surface.parm("base_colorg").set(.75)
    standard_surface.parm("base_colorb").set(.75)
    standard_surface.parm("specular_IOR").set(1)

    return vopnode


def create_material_node():
    """
    Creates the material node 
    """
    node = hou.node(".")
    nodeparent = node.parent()

    material = nodeparent.createNode("material","material_from_file")
    material.setInput(0,hou.node("."))
    material.moveToGoodPosition()
    material.setDisplayFlag(True)
    material.setRenderFlag(True)

    return material

def create_shop(parent_node,shop_name):

    shop = parent_node.createNode("shopnet",shop_name)
    shop.moveToGoodPosition()

    return shop

def create_ai_vopnet(parent_node,vopnet_name):

    vopnet_node = parent_node.createNode("arnold_vopnet",vopnet_name)
    vopnet_node.moveToGoodPosition()

    return vopnet_node

def create_ai_shader(shop,shader_name,material_dict):
    """
    Creates a shader and sets its paramaters
    Takes in the shader name and its paramaters in the material dict and according to each paramaters type and apply a different method depending
    on the data that is being recieved from the parm.

    """
    # a mapping from maya parm name to houdini names with its node index, this could be more dynamic with a loop checking the name agains the houdini index
    parm_name_mapping = {"baseColor":["base_color", 1],
                         "metalness":["metalness", 3],
                         "specularRoughness":["specular_roughness", 6], 
                         "transmission":["transmission", 10],
                         "normalCamera":["normal", 39]} # the keys need to match the names in maya

   
    vopnode = create_ai_vopnet(shop,shader_name)
    
    out_material = hou.node(vopnode.path()+"/OUT_material")
    
    #setting some base paramaters
    standard_surface = vopnode.createNode("arnold::standard_surface",shader_name)
    standard_surface.parm("base").set(1)
    standard_surface.parm("specular_IOR").set(1.4)

    out_material.setInput(0,standard_surface,0)
    standard_surface.setPosition((-4.6,0))

    #connecting the material dict to the shader
    parms = material_dict[shader_name][ "shader_parms"]

    node_y_pos = 4

    for parm in parms.keys():
        parm_name = parm_name_mapping[parm][0]
        parm_index = parm_name_mapping[parm][1]
        parm_value = parms[parm]

        # if a single map is plugged in
        if isinstance(parm_value, unicode): # unicode in python 2.x/ str / bytes in 3.x
            if parm_name == "base_color":
                image_node = create_image_node(vopnode, parm_name, color_family="Output", color_space="Output - Rec.709")
            else:
                image_node = create_image_node(vopnode, parm_name)
            
            image_node.parm("filename").set(str(parm_value))
            standard_surface.setInput(parm_index,image_node,0)
            image_node.setPosition((-11.1,node_y_pos))
        
        #if there is a float value set
        elif isinstance(parm_value, float):
            standard_surface.parm(parm_name).set(parm_value)

        #if there is a vector value set   
        elif isinstance(parm_value, list):
            #RGB
            r = parm_name + "r"
            g = parm_name + "g"
            b = parm_name + "b"
            #XYZ
            x = parm_name + "x"
            y = parm_name + "y"
            z = parm_name + "z"

            try:
                standard_surface.parm(r).set(parm_value[0])
                standard_surface.parm(g).set(parm_value[1])
                standard_surface.parm(b).set(parm_value[2])
            except:
                print("RGB failed, attempting XYZ")
                try:
                    standard_surface.parm(x).set(parm_value[0])
                    standard_surface.parm(y).set(parm_value[1])
                    standard_surface.parm(z).set(parm_value[2])
                except:
                    print("XYZ failed")
        
        elif isinstance(parm_value, dict):
            # handles the normal paramater
            if parm_name == "normal":
                normal_height_path = parm_value["normal_height"]
                normal_input_path = parm_value["normal_input"]
                height_path = parm_value["height"]
               
                if not parm_value["height"]:
                    normal_node = vopnode.createNode("arnold::normal_map", "normal")
                    height_node = vopnode.createNode("arnold::bump2d", "height")
                    normal_height_image_node = create_image_node(vopnode, "normal_input")
                    normal_normal_image_node = create_image_node(vopnode, "normal_normal")
                    #settting the filename parm
                    normal_height_image_node.parm("filename").set(normal_height_path)
                    normal_normal_image_node.parm("filename").set(normal_input_path)
                    # setting the inputs
                    normal_node.setInput(0, normal_normal_image_node, 0)
                    normal_node.setInput(2, height_node, 0)
                    height_node.setInput(0, normal_height_image_node, 0)
                    standard_surface.setInput(parm_index, normal_node, 0)
                
                else:
                    height_node = vopnode.createNode("arnold::bump2d","height")
                    height_image_node = create_image_node(vopnode,"height")
                    #settting the filename parm
                    height_image_node.parm("filename").set(height_path)
                    # setting the inputs
                    height_node.setInput(0, height_image_node, 0)
                    standard_surface.setInput(parm_index, height_node, 0)
                
                #setting node parm values
                height_node.parm("bump_height").set(0.01)

            else:
                print("cant set dict instance")
            
        else:
            print("{0}.{1} \t the paramater cant / doesnt need to be set".format(vopnode, parm_name))

        node_y_pos -= 2.0
    
    return vopnode

def create_image_node(parent_node, image_name, color_family="Utility", color_space="Utility - Raw"):
    """
    Creates an image node within the parent node and set to the given color space.
    parent_node: The node that you want the new image node to be inside
    image_name: The name of the image node
    color_family: one of the color family options listed in the houdini color family menu, default = "Utility", usually the alternative is "Output"
    color_space: one of the color space options listed in the houdini color space menu, default = "Utility - Raw", usually the alternative is "Output - Rec.709"
    """

    image_node = parent_node.createNode("arnold::image",image_name)
    image_node.parm("ignore_missing_textures").set(1)
    image_node.parm("color_family").set("{0}".format(color_family))
    image_node.parm("color_space").set("{0}".format(color_space)) # the name of the spaces are in the menu of the image node

    return image_node

def makeMaterials():
    """
    This is the main function that gets run on the pc_material_loader in houdini
    """

    node = hou.node(".")
    parent = node.parent()
    nodein = hou.node("./IN")
    nodeout = hou.node("./OUT")
    matfile_path = os.path.realpath(node.parm("pcmat_file").eval())
    shop = create_shop(parent,"shop_from_file")
    mdict = read_pc_material(matfile_path)

    # get group node
    for n in node.children():
        if n.name() == "shader_name_to_group":
            group_comb = n

    #set group node parms
    material_groups = mdict.keys()
    num_materials = len(material_groups)+1          #adding 1 for defualt shader
    num_mat_groups = len(material_groups)+1         #adding 1 for defualt shader
    group_comb.parm("numcombine").set(num_mat_groups)

    material_node = create_material_node()
    material_node.parm("num_materials").set(num_materials) # adding 1 so the default material can be added first
    default_shader = create_default_shader(shop)
    rel_path_to_vopnode = os.path.relpath(default_shader.path(), material_node.path()).replace("\\","/")
    material_node.parm("shop_materialpath1").set(rel_path_to_vopnode) # sets the default_shader to the 1 group on the material node
    
    index = 2 # starts after the default material
    for group in material_groups:
        #create the houdini groups
        group_comb.parm("group"+str(index)).set(group)
        objects = " ".join(mdict[group]["objects"])
        group_comb.parm("group_a"+str(index)).set(objects)
        #create shaders
        shader = create_ai_shader(shop,group,mdict)
        shader.layoutChildren()
        
        # #materail assignment
        material_node.parm("group"+str(index)).set(group)
        rel_path_to_vopnode = os.path.relpath(shader.path(), material_node.path()).replace("\\","/")
        material_node.parm("shop_materialpath"+str(index)).set(rel_path_to_vopnode)
        
        index += 1

    
    return "Done loading materials"


        











    



# x = read_pc_material(r"\\YARN\projects\mov\test\1_assets\characters\bob\0_sourcegeo\bob\tex\latest\bob_materials.json")








