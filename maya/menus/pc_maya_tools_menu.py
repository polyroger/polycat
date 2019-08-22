import pymel.core as pm

main_window = pm.language.melGlobals["gMainWindow"]
menu_obj = "pcToolsMenu"
menu_label = "Polycat Tools"

if pm.menu(menu_obj,label=menu_label,exists=True,parent=main_window):
    pm.delete(pm.menu(menu_obj,e=True,deleteAllItems=True))

custom_tools_menu = pm.menu(menu_obj, label=menu_label, parent=main_window, tearOff=True)