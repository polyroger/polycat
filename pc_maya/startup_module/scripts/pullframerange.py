import os
import pymel.core as pm
import json

def makeRange():

    seqlevel = 7
    cutlevel = 8
    jfile = r"\\YARN\projects\mov\eos\0_aaa\0_internal\0_project_data\kshotdata.json"

    try:

        
        name = pm.sceneName()
        pathsplit = name.split("/")

        if not pathsplit[0] and not pathsplit[1] and pathsplit[2].upper() == "YARN":
            
            print("probably yarn")
            
            seqlevel = 7
            cutlevel = 8
            
            sequence =  pathsplit[seqlevel]
            cut = pathsplit[cutlevel]


        else:
            print("probably not yarn")
            
            seqlevel = 4
            cutlevel = 5
            
            sequence =  pathsplit[seqlevel]
            cut = pathsplit[cutlevel]


        with open(jfile,"r") as f:
            jdata = json.load(f)

        fstart = jdata[sequence][cut]["frame_in"]
        fend = jdata[sequence][cut]["frame_out"]

        pm.playbackOptions(minTime=fstart,animationStartTime=fstart,maxTime=fend,animationEndTime=fend)

    except:
        print("Could not find shot data, setting to 1001 - 1100")
        pm.playbackOptions(minTime=1001,animationStartTime=1001,maxTime=1100,animationEndTime=1100)