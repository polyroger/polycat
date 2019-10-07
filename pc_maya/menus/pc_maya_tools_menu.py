# CREATES A POLYCAT MENU IN MAYA
# !! This script is run with pm.evalDeferred() in the userSetup.py !!
# POLYCAT ANIMATION

import pymel.core as pm

def createCameraOptions():
    mywin = pm.window(title="Camera Exporter Settings")
    pm.columnLayout(columnOffset=("both",20),height=100,rowSpacing=10)
    pm.separator()
    pm.floatSliderGrp(label="Camera Scale",parent=mywin,field=True,value=0.1,columnAlign=(1,"left"))
    pm.checkBoxGrp("houdiniexp",label="Export Houdini Camera",value1=True,parent=mywin,columnAlign=(1,"left"))
    pm.checkBoxGrp("mayaexp",label="Export Maya Camera",value1=True,parent=mywin,columnAlign=(1,"left"))
    pm.separator()
    pm.rowLayout(numberOfColumns=2,width=300,adjustableColumn=1)
    pm.button(label="Export")
    pm.button(label="Cancel")
    pm.showWindow(mywin)


def createMayaMenus():

    main_window = pm.language.melGlobals["gMainWindow"]
    menu_obj = "pcToolsMenu"
    menu_label = "Polycat Tools"

    # this starts building a heiracy. setParent automatically gets assigned to the parent of the last created menu.

    custom_tools_menu = pm.menu(menu_obj, label=menu_label, parent=main_window, tearOff=True)
    pm.menuItem(label="Scene",subMenu=True, parent=custom_tools_menu, tearOff=True)
    pm.menuItem(label="Export Camera",command="reload(pc_maya_tools_menu)\nreload(pc_ABC_camera_exporter)\npc_ABC_camera_exporter.runCameraExport()")
    pm.menuItem(optionBox=True,command="pc_maya_tools_menu.createCameraOptions()")

    # sets the parent back to the specified menu
    pm.setParent("..",menu=True)

    # add in other pm.menu and pm.menuItem after this to create more menus
