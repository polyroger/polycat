# POLYCAT ANIMATION FILE STRUCTURE CREATION
# PYTHON3

"""
This is the basic setup for creating a project structure,
Everything is essentially a cut, whether its an asset or a shot. This keeps the structure familiar no matter what what you are working on.
All cut level items are at the same strucute depth and have a [sequence type] / [sequence name] / [cut name]
"""

import pathlib
import os
import json
from kitsu_helpers import kfunctions

#THE MAIN FOLDER CREATION FUNCTIONS
def createJobBase(jobject,root,proj_name):
    """
    Creates the base structure of the project with no sequences
    ARGS:
    jobject  = the json structure object
    proj_name = the client / project name eg mov/eos
    """

    proj_root = root / proj_name

    #create job level
    for key,value in jobject["jobLevel"].items():
        makeDir(proj_root / value )
        #create base sub dirs
        try:
            for i,j in jobject[value].items():
                makeDir(proj_root / value / j)
        except :
            print(f"no sub directories found in {j}")
        
    return proj_root

def createSequence(job_base,parent,sequence_name):
    """
    Creates a sequence with the given parent
    ARGS:
    job_base = a path lib object to the name of the base of the project eg //YARN/projects/mov/eos or what is returned by the createJobBase funtion
    parent = The job level catagory that you want to add a sequence too. eg 1_assets
    sequence_name = The name of the sequnece type. eg scn0010 or characters or anamatic
    name = the name of the shot type eg cut0010 or croaker or forest

    Returns: A path lib object to the created sequence
    """
    sequence = job_base / parent / sequence_name
    makeDir(sequence)

    return sequence

def createCut(jobject,sequence,name="cut0010"):
    """
    Creates the cut structure for a sequece
    Args
    jobject  = the json structure object
    sequence = a path lib object to the name of the sequece most likely will be the createSequence function
    name = the name of the cut, in sequences it would be cut00xx but in asssets it will be the name of the asset
    num_cuts = how many cuts to make, only to be used when you want to create multiple cuts
    """
    cutpath = sequence / name
    
    for key,value in jobject["cutLevel"].items(): 
        makeDir(cutpath / value)
    
    #MAKING ADDITIONAL CUT DIRS
    try:
        for user in jobject[jobject["cutLevel"]["cutUsers"]]:
            userpath = makeDir(cutpath / jobject["cutLevel"]["cutUsers"] / user )
            for software in jobject["software"]:
                makeDir(userpath / software )
    except:
        print("skipping folder creation for")
    
    
    return cutpath

#START OF HELPER FUNCTIONS FOR FOLDER CREATION
def getStructure(json_structure):
    """
    Opens a json file and retuns a json object of that file
    """

    with open(json_structure,"r") as f:
        jdata = json.load(f)

    return jdata

def makeDir(path):
    
    try:
        dirpath = path.mkdir(parents=True,exist_ok=True)
        return path
    except:
        print("there was an error making {0} directory".format(path))
        return None     


def createNewProject(serverclient,servername,kprojectname):
    
    JFILE = r"pc_project\json\structure.json"
    ROOT = pathlib.Path("//YARN/projects")

    n = serverclient + "/" + servername

    #CREATING THE JOBLEVEL FOLDERS
    structure = getStructure(JFILE)
    base = createJobBase(structure,ROOT,n)

    #PULLING KITSU DATA
    kfunctions.kLogin()
    project = kfunctions.getKProject(kprojectname)
    sequences = kfunctions.getKProjectSequences(project)

    #CREATING ALL THE CUTS BASED OFF THE KITSU PROJECT
    for seqname,seqdict in sequences.items():
        sequence = createSequence(base,structure["jobLevel"]["jobSequences"],seqname)
        cuts = kfunctions.getKSequenceCuts(seqdict)
        for i in cuts:
            createCut(structure,sequence,name=i["name"])
        

if __name__ == "__main__":
    
    createNewProject("mov","test","Eosis")







    


    
