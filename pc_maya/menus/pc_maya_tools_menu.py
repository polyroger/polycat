# CREATES A POLYCAT MENU IN MAYA
# !! This script is run with pm.evalDeferred() in the userSetup.py !!
# POLYCAT ANIMATION

import pymel.core as pm
# from pc_maya import callback_test

def createMayaMenus():

    main_window = pm.language.melGlobals["gMainWindow"]
    menu_obj = "pcToolsMenu"
    menu_label = "Polycat Tools"

    # this starts building a heiracy. setParent automatically gets assigned to the parent of the last created menu.

    custom_tools_menu = pm.menu(menu_obj, label=menu_label, parent=main_window, tearOff=True)
    pm.menuItem(label="Scene",subMenu=True, parent=custom_tools_menu, tearOff=True)
    pm.menuItem(label="Model Prep",command="NameGGRP.openNameGGRP_dialog()")
    pm.menuItem(label="Scene Exporter",command="PcSceneExporter.openExportDialog()")
    pm.menuItem(label="Export Camera",command="menu_gui.initCameraExportGui()")
    pm.menuItem(label="Playblast Camera",command="menu_gui.initPlayblastCameraGui()")
    
    # sets the parent back to the specified menu
    pm.setParent("..",menu=True)

    # add in other pm.menu and pm.menuItem after this to create more menus



