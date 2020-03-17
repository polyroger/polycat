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
    
    while not geopath:
        
        for i in mydirs:
                            
            if i.is_dir() and i.name == folder:
                geopath = i.path
                print("The folder was found : {0}".format(geopath))
                break

        start_path = os.path.abspath(os.path.join(start_path,"../"))
        
        if start_path == "Y:\\":
            print("the path could not be found")
            break      
       
        mydirs = scandir.scandir(start_path)
    
    return geopath
