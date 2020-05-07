import os
import scandir
import pymel.core as pm

def goFindDirectory(start_path,folder):
    """
    Goes up from a starting directory and tries to find a folder
    RETURNS : STRING - path to folder if found
    """

    mydirs = scandir.scandir(start_path)

    geopath = False
    origpath = start_path
    
    while not geopath:
        
        for i in mydirs:
                            
            if i.is_dir() and i.name == folder:
                geopath = i.path
                print("The folder was found : {0}".format(geopath))
                break

        start_path = os.path.abspath(os.path.join(start_path,"../"))
        print start_path
        
        if start_path == os.path.realpath(os.path.join(start_path,"../")):
            print "the path could not be found"
            geopath = origpath
        else:
            mydirs = scandir.scandir(start_path)
    
    return geopath

def checkForPath(basepath,assetname):
    """
    Checks for a path + assetname, if it doesnt exist it makes it. If somthing goes wrong it returns None
    """
    
    basepath = os.path.normpath(basepath)
    assetpath = os.path.join(basepath,assetname)

    if not os.path.exists(assetpath):
        os.mkdir(assetpath)
        
        return assetpath
    
    else:
        return assetpath
       