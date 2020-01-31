import os
import re

def checkFileVersion(afile):
    """
    Expects a file name string as an input, looks for "v001" styled versioning.
    
    RETURNS: The version of the file as an integer or False if no version was found

    """
    digitlist = []
    repattern = r"v[\d\-\d]+"
    match = re.findall(repattern, afile)
    
    if match:
        print("there is a version in the filename")
        print("current version is : %s"%match[0])

        for i in match[0]:
            if i.isdigit():
                digitlist.append(i)
    
        version = int("".join(digitlist))

        return version
    else:
        print("There is not a correctly nameed version in the filename")

        return False

def versionPlusOne(aversion):

    """
    Expects and integer version as an input

    RETURNS: a integer, double padded version + 1

    """ 
    versionplus = "v" + (str(aversion + 1).zfill(3))
    print("new version created : %s")%versionplus

    return versionplus
   





