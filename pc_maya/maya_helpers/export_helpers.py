"""
Polycat Maya Export Helpers
"""

import pymel.core as pm


def pcABCCameraArgs(rootname,filepath,start,end,userattrlist=None,step=str(1.0)):
    """
    Built for abc camera exporters, this skips things like namespace and reference checks
    Args 
    rootname: str the name of the root object in the maya outliner
    filepath: str the full filepath including the filename and extension of the file to export
    start: int start frame
    end: int end frame
    userlist: str list of custom user attributes defaults to None
    step: float The frame subsampling defaults to 1.0

    return: str of the command (j) argument for the AbcExporter
    """
    
    exportargs = ["-root",rootname]
    exportargs.extend(["-file",filepath])
    exportargs.extend(["-framerange",str(start-1),str(end+1)])
    exportargs.extend(["-step",step])
    
    if userattrlist:
        for attr in userattrlist:
            exportargs.extend(["-userAttr",attr])
    
    exportargs.extend(["-worldspace","-eulerFilter","-stripNamespaces"])

    command = " ".join(exportargs)
    
    return command



