"""
Polycat Nuke menu and startup
"""

import nuke
import pc_startup_functions as pstart


toolbar = nuke.menu('Nodes')

#Victor tools
VMenu = toolbar.addMenu('V!ctor', icon='V_Victor.png')
VMenu.addCommand('V_Slate', 'nuke.createNode("V_Slate")', icon='V_Slate.png')

#X tools
xToolMenu = toolbar.addMenu("Xtools", icon="X_Tools.png")
xToolMenu.addCommand("X_Tesla","nuke.createNode('X_Tesla')",icon = "X_Tesla.png")

#Autoflare
AFMenu = toolbar.addMenu('&Autoflare2.2')
AFMenu.addCommand("AutoFlare 2.2", "nuke.createNode('AutoFlare2')")

#Setting Global settings
# Check out the nuke callbacks ( https://learn.foundry.com/nuke/developers/105/pythondevguide/callbacks.html ) these are loaded in order. and some of the names are not what they seem.
nuke.addOnUserCreate(pstart.setNukeGlobalSettings)
# nuke.addOnUserCreate(pstart.setWriteNodeSettings,(nuke.thisNode()),nodeClass="Write")

#Create directory before render
nuke.addBeforeRender(pstart.CreatePath, nodeClass = 'Write')

#adding resolutions
pstart.addResolutions()



