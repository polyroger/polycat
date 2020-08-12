import gazu
import pathlib
import json
import os


def kLogin():
    """
    A login function to make logging in to the kitsu api a little faster.
    """
    #manager
    # USERNAME = os.getenv("KUSER")
    # PASSWORD = os.getenv("KPWORD")

    #artist
    USERNAME = os.getenv("KAUSER")
    PASSWORD = os.getenv("KAPWORD")

    gazu.set_host("https://polycat.cg-wire.com/api")
    gazu.log_in(USERNAME, PASSWORD)

    return None

def writeAssetKdata():
       
    """
    Writes the Json file required for setting asset data in the DCC apps.
    """

    project = gazu.project.get_project_by_name("Eosis")
    assettypes = gazu.asset.all_asset_types_for_project(project)
    
    tasks = []
    for task in gazu.task.all_task_types():
        tasks.append(task["name"])

    assetdict = {}
    chardict = {}

    for assettype in assettypes:

        assets = gazu.asset.all_assets_for_project_and_type(project,assettype)
        
        for asset in assets:
            info = {"name":asset["name"],"tasks":tasks}
            chardict[asset["name"]] = info
        
        assetdict[assettype["name"]] = chardict   
        chardict = {}   

    assetsfile = "kassetdata.json"

    kdata_path = pathlib.Path("//YARN/projects/mov/eos/0_aaa/0_internal/0_project_data")
    sequence_file = kdata_path / assetsfile
    
    with open(sequence_file,"w") as f:
        jdata = json.dumps(assetdict,indent=4)
        f.write(jdata)

def writeCutKdata():

    """
    Writes the Json file required for setting shot data in the DCC apps.
    """

    # Some boilerplate for getting data from kitsu
    project = gazu.project.get_project_by_name("Eosis")
    sequences = gazu.shot.all_sequences_for_project(project)
    

    #Write shot data
    cutdata = {}
    seqdata = {}
    taskdict = {}

    tasks = []
    for task in gazu.task.all_task_types():
        tasks.append(task["name"])
    taskdict["tasks"] = tasks
  
    for seq in sequences:
        
        seqdata[seq["name"]] = {}
        cuts = gazu.shot.all_shots_for_sequence(seq)
        
        for cut in cuts:
            
            if cut["data"]:
                cut["data"].update(taskdict)
                cutdata[cut["name"]] = cut["data"]
            else:
                standindata = {"frame_in": "NA","fps":"NA","frame_out":"NA","tasks":taskdict["tasks"]}
                cutdata[cut["name"]] = standindata
            seqdata[seq["name"]] = cutdata
        cutdata = {}


    shotsfile = "kshotdata.json"

    kdata_path = pathlib.Path("//YARN/projects/mov/eos/0_aaa/0_internal/0_project_data")
    sequence_file = kdata_path / shotsfile
    
    with open(sequence_file,"w") as f:
        jdata = json.dumps(seqdata,indent=4)
        f.write(jdata)


if __name__ == "__main__":
    
    kLogin()
    writeCutKdata()
    # writeAssetKdata()




   


