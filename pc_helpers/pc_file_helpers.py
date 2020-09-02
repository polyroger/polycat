import os
import re
import clique


def listAllFilesInFolder(folderpath):
    """
    Need to import os module
    Returns a list of all the files in a folder.
    """

    try:
        dircontents = os.listdir(folderpath)
    except:
        return None
       
    filelist = []

    for item in dircontents:
        itempath = os.path.join(folderpath,item)
        if os.path.isfile(itempath):
            filelist.append(item)
            
    return filelist

def getLatestFromList(filelist):

    """
    Given a list of files return an int of the latest version file
    """
    collections,remainder = clique.assemble(filelist,minimum_items=1)

    if not collections:
        return int(0)
    
    if len(collections) > 1:
        print("ERROR There is more that one type of sequence in this folder")
        return None
    
    fileseq = collections[0]

    versionlist = []
    for version in fileseq.indexes:
        versionlist.append(version)
    
    versionlist.sort()
    latestversion = versionlist[-1]

    return int(latestversion)

def getLatestFile(filelist):
    """
    Returns the highest versioned file in a file list
    """
    #if there is unexpoected results it is most likely the regex in paatters
    collections,remainder = clique.assemble(filelist,minimum_items=1,patterns=[r"\_v(?P<index>(?P<padding>0*)\d+)"])
    print(collections)
    if not collections:
        return int(0)
    
    if len(collections) > 1:
        print("ERROR There is more that one type of sequence in this folder")
        return None
    
    fileseq = collections[0]

    filelist = []
    for version in fileseq:
        filelist.append(version)
    
    filelist.sort()
    latestversion = filelist[-1]

    return latestversion

  
def versionPlusOne(version):

    """
    Expects and integer version as an input

    RETURNS: str double padded version + 1

    """
    if version == None:
        return None

    versionplus = "v" + (str(version + 1).zfill(3))
    print("new version number : %s")%versionplus

    return versionplus

# testpath = r"\\YARN\projects\ply\nod\2_sequences\E10\cut0010\0_camera\houdini"
# testpath = r"\\YARN\projects\ply\nod\3_development\pipeline_tools\cameratesting\0_camera\houdini"

# version = getLatestFile(listAllFilesInFolder(testpath))
# print(version)