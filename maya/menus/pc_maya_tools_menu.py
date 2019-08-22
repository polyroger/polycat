# CREATES A POLYCAT MENU IN MAYA
# this is run as a script rather that a imported and run as a function.
# POLYCAT 2019

import pymel.core as pm

def executthis():
    test = "this is working"
    print (test)


# THIS SECTION FOR DEV PURPOSES SO THAT WE CAN CREATE AND DELETE THE MENU
# main_window = pm.language.melGlobals["gMainWindow"]
# menu_obj = "pcToolsMenu"
# menu_label = "Polycat Tools"
#
# try:
#     if pm.menu(menu_obj,label=menu_label,exists=True,parent=main_window):
#         pm.delete(pm.menu(menu_obj,e=True,deleteAllItems=True))
# except:
#     print("there was an error deleting the menu")



# this starts building a heiracy. setParent automatically gets assigned to the parent of the last created menu.

custom_tools_menu = pm.menu(menu_obj, label=menu_label, parent=main_window, tearOff=True)
pm.menuItem(label="Scene",subMenu=True, parent=custom_tools_menu, tearOff=True)
pm.menuItem(label="Export Camera",command="executthis()")

# sets the parent back to the specified menu
pm.setParent("..",menu=True)

# add in other pm.menu and pm.menuItem after this to create more menus