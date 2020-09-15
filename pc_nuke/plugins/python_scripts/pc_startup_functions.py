"""
Polycats nuke startup functions
"""
import nuke

def addResolutions():

    reslist = ["2048 858 2K_DCP_cinescope","1080 1920 noodle_and_bun"]

    for res in reslist:
        nuke.addFormat(res)
        print("{} was added to the resolution list".format(res))

  
