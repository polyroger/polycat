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
    pm.menuItem(label="Scene tools",subMenu=True, parent=custom_tools_menu, tearOff=True)
    pm.menuItem(label="Import Alembic",command="from pc_maya.snippets import snippets;snippets.importAlembicFile()")
    pm.menuItem(label="Scene Exporter",command="from pc_dialogs.scene_export_dialog import PcSceneExporter;PcSceneExporter.openExportDialog()")
    pm.menuItem(label="Export Camera",command="menu_gui.initCameraExportGui()")
    pm.menuItem(label="Playblast Camera",command="menu_gui.initPlayblastCameraGui()")
    # sets the parent back to the specified menu
    pm.setParent("..",menu=True)

    #start of Model tools
    pm.menuItem(label="Model tools",subMenu=True, parent=custom_tools_menu, tearOff=True)
    pm.menuItem(label="Model Prep",command="from pc_dialogs.export_prep_dialog import NameGGRP;NameGGRP.openNameGGRP_dialog()")



    # sets the parent back to the specified menu
    pm.setParent("..",menu=True)


    # add in other pm.menu and pm.menuItem after this to create more menus



