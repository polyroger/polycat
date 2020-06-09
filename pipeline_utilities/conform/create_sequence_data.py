import pathlib
import re
import json

path = pathlib.Path("//YARN/projects/mov/eos/2_sequences/scn0010_wizardlodge_interior")
playblast = "0_playblast"
versionlist = []
filelist = []
pattern = r"([0-9]){4}$"
frameranges = {}
sdata = {}



for folder in path.iterdir():
    cutpath = path / folder
    currentp = path / folder / playblast

    for version in currentp.iterdir():
        
        if version.is_dir():
            versionlist.append(version)
            versionlist.sort()
            latestversion = (versionlist[-1])

            for file in latestversion.iterdir():
                
                if not file.suffix == ".db" and re.search(pattern,file.stem):

                    filelist.append(re.search(pattern,file.stem).group(0))
        
            filelist.sort()
            try:
                frameranges[folder.name] = {"start":filelist[0],"end":filelist[-1]}
            except IndexError:
                print("There is no version folder in the playblastfolder")
                frameranges[folder.name] = {"start":"null","end":"null"}
        
            filelist = []

sdata["frameranges"] = frameranges
tojson = json.dumps(sdata,indent=4)

with open(path / "sdata.json","x") as sequencedata:
    sequencedata.write(tojson)
    sequencedata.close()
    
            

         


    