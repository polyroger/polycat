import gazu
import pathlib
import json
import os


# Kitsu login
USERNAME = os.getenv("KUSER")
PASSWORD = os.getenv("KPWORD")

gazu.set_host("https://polycat.cg-wire.com/api")
gazu.log_in(USERNAME, PASSWORD) 

project = gazu.project.get_project_by_name("Eosis")
sequences = gazu.shot.all_sequences_for_project(project)

# Setting up json paramaters
seqdata = {}
cutdata = {}

for seq in sequences:

    cuts = gazu.shot.all_shots_for_sequence(seq)
    seqdata[seq["name"]] = {}
    
    for cut in cuts:

        if cut["data"]:

            cutdata[cut["name"]] = cut["data"]
            seqdata[seq["name"]].update(cutdata)

        else:

            standindata = {"frame_in": "NA","fps":"NA","frame_out":"NA"}
            cutdata[cut["name"]] = standindata
            seqdata[seq["name"]].update(cutdata)


sequence_path = pathlib.Path("//YARN/projects/mov/eos/0_aaa/0_internal/0_project_data")
sequence_file = sequence_path / "kdata.json"
with open(sequence_file,"w") as f:
    jdata = json.dumps(seqdata,indent=4)
    f.write(jdata)







   


