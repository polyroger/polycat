"""
Polycats nuke startup functions
"""
import nuke
import os

def addResolutions():
    """
    Adds custom resolutions to the standard nuke resolution list
    """

    reslist = ["2048 858 1 DCP_cinescope","1080 1920 1 noodle_and_bun"]

    for res in reslist:
        nuke.addFormat(res)
        print("{} was added to the resolution list".format(res))
  
def setNukeGlobalSettings():
    """
    I think that this is not working because the function is being executed before nuke is fully loaded,
    https://community.foundry.com/discuss/topic/101873/execute-python-code-after-nuke-script-is-loaded?mode=Post&postID=889226
    
    """
    root = nuke.Root()

    # for nuke 9
    root["defaultViewerLUT"].setValue(1)
    # for nuke 12
    root["colorManagement"].setValue(1)

    nuke.knobDefault("Viewer.viewerProcess","Rec.709 (ACES)") # this is the format if aces is loaded

def CreatePath():
    """
    Creates a path so that it existst when you render
    """
   
    file = nuke.filename(nuke.thisNode())
    dir = os.path.dirname(file)
    osdir = nuke.callbacks.filenameFilter(dir)
   
    try:
        os.makedirs (osdir)
    except OSError:
        pass
      
def register_viewers(also_remove = "default"):
    """
    So OCIO's python api is called pyOpenColorIO - https://opencolorio.readthedocs.io/en/stable/developers/bindings/PythonAPI.html
    all viewprocesses in nuke are "nodes" to set all the startup processes you have to deregister the current nodes and them register the new nodes.
    When you register the new nodes you can set those node defaults. do this to setup custom display nodes

    to set the nuke defaults on startup, Root() is the global nuke settings class, to get / set values use this syntax
    nuke.Root()["defaultViewerLUT"].setValue(1)
    nuke.Root()["defaultViewerLUT"].getValue()


        Registers the a viewer process for each display device/view, and
        sets the default viewer process.

        ``also_remove`` can be set to either:
        
        - "default" to remove the default sRGB/rec709 viewer processes
        - "all" to remove all processes
        - "none" to leave existing viewer processes untouched

    """

    if also_remove not in ("default", "none", "all"):
        raise ValueError("also_remove should be set to 'default', 'none' or 'all'")

    if also_remove == "default":
        nuke.ViewerProcess.unregister('rec709')
        nuke.ViewerProcess.unregister('sRGB')
    elif also_remove == "all":
        # Unregister all processes, but retain the useful "None" option
        for curname in nuke.ViewerProcess.registeredNames():
            nuke.ViewerProcess.unregister(curname)

        nuke.ViewerProcess.register(
            name = "None",
            call = nuke.nodes.ViewerProcess_None,
            args = ())

    # Formats the display and transform, e.g "Film1D (sRGB)"
    DISPLAY_UI_FORMAT = "%(view)s (%(display)s)"

    import PyOpenColorIO as OCIO
    config = OCIO.GetCurrentConfig()

    # For every display, loop over every viewth
    for display in config.getDisplays():
        for view in config.getViews(display):
            # Register the node
            nuke.ViewerProcess.register(
                name = DISPLAY_UI_FORMAT % {'view': view, "display": display},
                call = nuke.nodes.OCIODisplay,
                args = (),
                kwargs = {"display": display, "view": view})


    # Get the default display and view, set it as the default used on Nuke startup
    defaultDisplay = config.getDefaultDisplay()
    defaultView = config.getDefaultView(defaultDisplay)
    
    nuke.knobDefault(
        "Viewer.viewerProcess",
        DISPLAY_UI_FORMAT % {'view': defaultView, "display": defaultDisplay})

# def setWriteNodeSettings(nukenode):
#     nuke.tprint("running write settings")
#     nuke.tprint(nukenode.name())
