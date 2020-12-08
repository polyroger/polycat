
"""

read the json
count the amount of material dict entires
create a material node that has as many parms as there are dict entires
for each Key
    create a counter to match the material parm
    make a group from the geo list
    assign the group to the material parm
    make an arnold shader named after the dict Key
    check the json for texture files
    set the basecolor paramater to either a color or a texture.
    assign the new shader to the current paramater in the texture node

"""

import json
import hou

def read_pc_material(pcmatfile):
    """
    Reads the material file and outputs a python dict
    """
    with open(pcmatfile) as f:
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

def find_out_material(vopnet):

    for node in vopnet.children():
        if node.type() == "arnold_material":
            a_material = node
            return a_material
        else:
            print("a material node could not be found in the {0}".format(vopnet))
            return None


def create_ai_shader(parent_node,shader_name):

    shader_node = parent_node.createNode("arnold::standard_surface",shader_name)
    shader_node.moveToGoodPosition()

    return shader_node

def create_image_node(parent_node,image_name):

    image_node = parent_node.createNode("arnold::image",image_name)
    image_node.moveToGoodPosition()

    return image_node

def connect_outs_to_in(parm_out,parm_in):
    """
    Connects houdini paramaters
    """
    

def create_material_parms(material_node,matdict):
    """
    sets up the material node with the values from the material dict
    """
    # dont know how else to set the mulitparm bloc so i do it twice
    parent = material_node.parent()
    num_materials = len(matdict.keys())
    material_node.parm("num_materials").set(num_materials)
    index = 1

    shop = create_shop(parent,"shop_from_file")

    for key in matdict.keys():
        group = "group"+str(index)
        material_node.parm(group).set(key)

        material_path = "shop_materialpath"+str(index)
        
        vopnet = create_ai_vopnet(shop,key)
        shader = create_ai_shader(vopnet,key)
        material_node.parm(material_path).set(vopnet.path())
        
        index += 1
    
    






        
    


        











    



# x = read_pc_material(r"\\YARN\projects\mov\test\1_assets\characters\bob\0_sourcegeo\bob\tex\latest\bob_materials.json")








