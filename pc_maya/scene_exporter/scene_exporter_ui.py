import scene_exporter as sce

def generate_material_json(export_path):

    selection = sce.get_selection()
    shaders = sce.get_assigned_shaders(selection)

    if shaders:
        materials = sce.create_material_dict(shaders,selection)
        if not sce.write_material_json(materials,export_path):
            return

    elif shaders == False:
        return
    else:
        sce.Pc_Logger.error("There was an error obtaining the shader list: shaders = {0}".format(shaders))

# if name == "__main__":
#     generate_material_json(r"\\YARN\projects\mov\test\1_assets\characters\bob\0_sourcegeo\bob\tex\latest\bob_materials")