import hou
import json


def scaleUpCut():
    ss = hou.node("/obj/pc_set_shot1")
    sscut = ss.parm("cut")
    node = hou.node(".")
    root = node.parm("root").eval()
    null = hou.node(root + "/" + "proxy")
    nullscale = null.parm("scale")

    nullscale.set(10)

    return nullscale

def scaleDownCut(nullscale):

    nullscale.set(1)

def setFrameRange(cutname):
    print("running set frame range")

    with open(r"\\YARN\projects\mov\eos\2_sequences\scn0010_wizardlodge_interior\sdata.json") as jdata:
        data = json.load(jdata)
        jdata.close()

    start = data["frameranges"][cutname]["start"]
    end = data["frameranges"][cutname]["end"]

    hou.playbar.setFrameRange(int(start),int(end))

    print("set frame range end")

    

    

    


    