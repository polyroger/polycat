import os
import scandir

def goFindFolder(start_path,folder):
    """
    Goes up from a starting directory and tries to find a folder
    RETURNS : STRING - path to folder if found
    """
    print "trying to find directory"
    print start_path
    print folder

    if not start_path:
        return "\\\\YARN\\projects"
    else:
        folderpath = False
        mydirs = scandir.scandir(start_path)
        origpath = start_path

    while not folderpath:
        
        for i in mydirs:
                            
            if i.is_dir() and i.name == folder:
                folderpath = i.path
                print("The folder was found : {0}".format(folderpath))
                break

        start_path = os.path.abspath(os.path.join(start_path,"../"))
  
        
        if start_path == os.path.realpath(os.path.join(start_path,"../")):
            print "the path could not be found"
            folderpath = origpath
        else:
            mydirs = scandir.scandir(start_path)
    
   
    return folderpath


def checkForPath(basepath,assetname,refversion):
    """
    Checks for a path + assetname, if it doesnt exist it makes it. If somthing goes wrong it returns None
    """
    print("running checkForPath()")
    
    foldername = assetname + refversion
    basepath = os.path.normpath(basepath)
    assetpath = os.path.abspath(os.path.join(basepath,foldername,"mod"))

    if not os.path.exists(assetpath):
        print "making path"
        os.makedirs(assetpath)
        
        return assetpath
    
    else:
        return assetpath

