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
    # collections,remainder = clique.assemble(low_filelist,minimum_items=1,patterns=[r"\_v(?P<index>(?P<padding>0*)\d+)\.mb"])
    collections,remainder = clique.assemble(filelist,minimum_items=1,case_sensitive=False,patterns=[clique.PATTERNS["versions"]]) # versions is basically the same as the above regex

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
    Returns the highest versioned filename, note filename not version
    """
    #if there is unexpoected results it is most likely the regex in paatters. this is specifically looking for _v000 naming
    collections,remainder = clique.assemble(filelist,minimum_items=1,patterns=[r"\_v(?P<index>(?P<padding>0*)\d+)"])
    # if collections is none, then there is mostlikely only one file in the folder, that does not have correct versioning
    if not collections:
        return filelist[0]
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

def checkFileVersion(afile):
    """
    Expects a file name string as an input, looks for "v001" styled versioning. Aims to extract the current version in the filename
    This function is an alternative to the getlatestfromlist, which uses clique collections, this is a regex solution
    
    RETURNS: The version of the file as an integer or False if no version was found

    """
    
    repattern = "v\d+"
    match = re.findall(repattern, afile)
    
    if match:
        version = int(match[0].replace("v",""))

        return version
    else:
        print("There is not a correctly nameed version in the filename")

        return False

def getLatestVersion(filepath):
    """
    Gets the latest current version,expects a valide file path, use this with the version plus one.
    """
    
    versionlist = [0]
    
    # if the file path does not exist, I assume that the folder has yet to be created and the version should be 0
    if os.path.isdir(filepath):
        contents = os.listdir(filepath)
        for file in contents:
            path = os.path.join(filepath,file)
            if os.path.isfile(path):

                fileversion = checkFileVersion(file)
                versionlist.append(fileversion)
        
        versionlist.sort()
    latest = versionlist[-1]
    print("The latest version is: {}".format(latest))

    return latest
        
def versionPlusOne(version):
    """
    Expects and integer version as an input

    RETURNS: str double padded version + 1
    """
    if version == None:
        return None
    
    versionplus = "_v" + (str(version + 1).zfill(3))
    print("new version number : %s")%versionplus

    return versionplus

def extract_version(filepath):
    """
    Given a file path or a file name, extract the version number from the path string
    args
    path (str): A string of either the filename or filepath
    Alternative to clique collections, uses regex only

    returns (int) an extracted version number or None if nothing is found
    """
    no_version = None
    pattern = (r"_v(\d+)$")
    name,ext = os.path.splitext(filepath) # split off the filename extension
    
    try:
        match = re.search(pattern, name)
        version = str((match.group(1))).lstrip("0")
        return int(version)
    except:
        print("There was an error when attempting to get the version of {0}, make sure that the file has _v000 styled versioning\nSetting version to {1} ".format(name, no_version))
        return no_version

def udim_check(filepath):
    """
    Checks the filepath for a udim extension.
    Returns the regex match object if true, returns None if there is no match
    This should work with a filename or a file path as splittext will strip the extension and the regex searches backwards
    """
    pattern = r"(\d{4})$" # this simply looks to see if the string ends in 4 numbers eg 1001
    
    name,ext = os.path.splitext(filepath) # split off the filename extension
    
    match = re.search(pattern,name)

    return match

def replace_udim_filepath(filepath,replace_string):
    """
    Given a **full filepath**, return the full file path with the new replacement string.
    Use this when wanting to maintain the full file path, use replace_udim_file if you are just using a filename
    """
    pattern = r"(\d{4})$" # this simply looks to see if the string ends in 4 numbers eg 1001

    filename = os.path.basename(filepath)
    dirname = os.path.dirname(filepath)
    name,ext = os.path.splitext(filename)

    udim_name = re.sub(pattern, replace_string, name)
    full_udim_path = os.path.join(dirname, udim_name)+ext

    return full_udim_path

def replace_udim_file(filename, replace_string):
    """
    Given a **filename**, return the file name with the new replacement string.
    Use this when you are just working with file names and not the full path.
    """
    pattern = r"(\d{4})$" # this simply looks to see if the string ends in 4 numbers eg 1001
    name,ext = os.path.splitext(filename)

    udim_filename = re.sub(pattern, replace_string, name) + ext

    return udim_filename

def create_server_location(filepath,server_location=r"\\\\YARN\\projects"):
    """
    replaces an absolute path (d:\) with the UNC (unified naming convention) path.
    """
    pattern = r".+?:" # finds everything up to a :
    
    match = re.search(pattern,filepath)

    if match:
        new_path = re.sub(pattern,server_location,filepath)
        if not os.path.isfile(new_path):
            print("The filepath is not a valid path, make sure that you are using a file from the server")
            raise Exception("The filepath: {0} is not valid".format(filepath)) 
        
        return new_path
    elif not match:
        print("A match could not be found, returning the origional filepath")
        return filepath
    else:
        print("there was an error when attempting create a server location for {0}".format(filepath))
        raise Exception("The filepath: {0} is not valid".format(filepath)) 


# testpath = r"\\YARN\projects\mov\gra\3_development\pipeline_tools\cut0010\0_camera\maya"
# # testpath = r"\\YARN\projects\ply\nod\3_development\pipeline_tools\cameratesting\0_camera\houdini"
# testpath = r"//YARN/projects/mov/gra/1_assets/environment/house/0_sourcegeo/sophies_room/decor/vinyl_cover/tex/latest/vinyl_covers_col_1001.tif"

# udim = udim_check(testpath)
# allfiles = listAllFilesInFolder(testpath)
# latestfile = getLatestFile(allfiles)
# latestversion = getLatestFromList(allfiles)
# versionplus = versionPlusOne(latestversion)
# server_location = create_server_location(testpath)

# print(udim)
# print(server_location)
# print(allfiles)
# print(latestfile)
# print(latestversion)
# print(versionplus)
