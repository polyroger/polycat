import os
from pipeline_utilities.conform import sequence_data
from pipeline_utilities import path_manipulation
import pymel.core as pm

def makeRange():

    jfile = "\\\\YARN\\projects\\mov\\eos\\2_sequences\\scn0010_wizardlodge_interior\\sdata.json"
    data = sequence_data.getJData(jfile)
    asspath = path_manipulation.goFindDirectory(os.path.dirname(pm.sceneName()),"0_assfile")
    cutname =  os.path.basename(os.path.abspath(os.path.join(asspath,"../")))
    framerange = sequence_data.getFrameRange(data,cutname)
    s = framerange["start"]
    e = framerange["end"]
    pm.playbackOptions(ast=s,minTime=s,aet=e,maxTime=e)
