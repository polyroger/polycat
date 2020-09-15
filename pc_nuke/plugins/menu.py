#Polycat nuke menu

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

#version up and save startnuk
def CreatePath():
   file = nuke.filename(nuke.thisNode())
   dir = os.path.dirname(file)
   osdir = nuke.callbacks.filenameFilter(dir)
   try:
      os.makedirs (osdir)
   except OSError:
      pass
      
      
nuke.addBeforeRender(CreatePath, nodeClass = 'Write')
#version up and save end

