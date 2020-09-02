# CREATES A POLYCAT MENU IN MAYA
# !! This script is run with pm.evalDeferred() in the userSetup.py !!
# POLYCAT ANIMATION

import pymel.core as pm

def createMayaMenus():

    main_window = pm.language.melGlobals["gMainWindow"]
    menu_obj = "pcToolsMenu"
    menu_label = "Polycat Tools"

    # this starts building a heiracy. setParent automatically gets assigned to the parent of the last created menu.

    custom_tools_menu = pm.menu(menu_obj, label=menu_label, parent=main_window, tearOff=True)
    
    #start of Scene tools
    pm.menuItem(label="Scene Tools",subMenu=True, parent=custom_tools_menu, tearOff=True)
    pm.menuItem(label="Import Alembic",command="from pc_maya.snippets import snippets;snippets.importAlembicFile()")
    pm.menuItem(label="Scene Exporter",command="from pc_dialogs.scene_export_dialog import PcSceneExporter;PcSceneExporter.openExportDialog()")
    pm.menuItem(label="Export Camera",command="from pc_maya.camera_exporter.pc_camera_exporter_ui import CameraExporter;CameraExporter.openCameraExportDialog()")
    pm.menuItem(label="Set Frame Range",command="pullframerange.makeRange()")

    # sets the parent back to the specified menu
    pm.setParent("..",menu=True)

    #start of Model tools
    pm.menuItem(label="Model Tools",subMenu=True, parent=custom_tools_menu, tearOff=True)
    pm.menuItem(label="Model Prep",command="from pc_dialogs.export_prep_dialog import NameGGRP;NameGGRP.openNameGGRP_dialog()")
    pm.menuItem(label="Create Export Set", command="from pc_maya.helpers.export_helpers import export_helpers;export_helpers.createExportSet()")
    pm.menuItem(label="Scale Reference",subMenu=True,tearOff=True)
    pm.menuItem(label="Measurement Man",command="from pc_maya.snippets import snippets;snippets.importAlembic('//YARN/projects/gen/models/measurement_man/male/male_scaleref_185cm_maya.abc')")
    pm.menuItem(label="Measurement Man Rig",command="pm.importFile('//YARN/projects/gen/models/measurement_man/male/mm_rig_01.ma')")
    pm.menuItem(label="Measurement Woman",command="from pc_maya.snippets import snippets;snippets.importAlembic('//YARN/projects/gen/models/measurement_man/female/female_scaleref_165cm_maya.abc')")
    pm.menuItem(label="Measurement Woman Rig",command="pm.importFile('//YARN/projects/gen/models/measurement_man/female/rig/mw_rig_02.ma')")


    # sets the parent back to the specified menu
    pm.setParent("..",menu=True)

    #start of Animation Tools
    pm.menuItem(label="Animation Tools",subMenu=True, parent=custom_tools_menu, tearOff=True)
    pm.menuItem(label="Playblast Camera",command="from pc_maya.playblast.pc_playblast_ui import PcPlayblast;PcPlayblast.openPcPlayblast_dialog()")
    pm.menuItem(label="Studio Library",command="from pc_maya.studio_lib import pc_studiolibrary;pc_studiolibrary.launchSL()")





    # add in other pm.menu and pm.menuItem after this to create more menus



