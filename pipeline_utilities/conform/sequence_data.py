import json
import os
import pymel.core as pm

from pipeline_utilities import path_manipulation



def getJData(pathtofile):
    
    with open(pathtofile) as f:
        jdata = json.load(f)
        f.close()

    return jdata


def getFrameRange(jdata,cutname):
    
    framerange = (jdata["frameranges"][cutname])

    return framerange





