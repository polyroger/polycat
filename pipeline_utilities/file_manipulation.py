import os
import re

def checkFileVersion(afile):
    """
    Expects a file name string as an input, looks for "v001" styled versioning. Aims to extract the current version in the filename
    
    RETURNS: The version of the file as an integer or False if no version was found

    """
    
    repattern = "v\d+"
    match = re.findall(repattern, afile)
    
    if match:
        print("there is a version in the filename")
        print("current version is : %s"%match[0])

        version = int(match[0].replace("v",""))

        return version
    else:
        print("There is not a correctly nameed version in the filename")

        return False

def getLatestVersion(filepath,assetname):
    
    versionlist = [0]
    contents = os.listdir(filepath)
    
    for file in contents:
        
        path = os.path.join(filepath,file)
        
        if os.path.isfile(path):

            fileversion = checkFileVersion(file)
            versionlist.append(fileversion)
    
    versionlist.sort()
    
    return versionlist[-1]
  
  
        
def versionPlusOne(version):

    """
    Expects and integer version as an input

    RETURNS: a string integer, double padded version + 1

    """ 
    versionplus = "_v" + (str(version + 1).zfill(3))
    print("new version created : %s")%versionplus

    return versionplus






