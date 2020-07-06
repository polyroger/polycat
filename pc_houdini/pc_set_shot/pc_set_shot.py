import os
import hou
import json

ROOT = "$JOB"
CLIENT = hou.parm("client").eval()
PROJECT = hou.parm("project").eval()
LEVEL = hou.parm("level").eval()


def getScene():
    return hou.parm("scene").eval()

def getCut():
    return hou.parm("cut").eval()



def setFrameRange(cutname=getCut(),scenename=getScene()):
    """
    Looks at the projects kdata json file that is build from kitsu and sets the frame range according to the shot
    that has been selected
    """

    with open(r"\\YARN\projects\mov\eos\0_aaa\0_internal\0_project_data\\kdata.json","r") as jdata:
        data = json.load(jdata)
        jdata.close()

    try:
        start = int(data[scenename][cutname]["frame_in"])
        end = int(data[scenename][cutname]["frame_out"])
    except:
        hou.ui.displayMessage("No json data for {}, setting range to 1001-1100".format(cutname),buttons=["OK"],title="Wa")
        start = int(1001)
        end = int(1100)


    hou.playbar.setFrameRange(int(start),int(end))
    hou.playbar.setPlaybackRange(int(start),int(end))
    hou.setFrame(start)

    return (start,end)

  




    