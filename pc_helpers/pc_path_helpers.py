import os
import scandir
import difflib

def goFindFolder(start_path,folder):
    """
    Goes up from a starting directory and tries to find a folder
    RETURNS : STRING - path to folder if found
    """
    print ("trying to find directory")
    print (start_path)
    print (folder)

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
            print ("the path could not be found")
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
        print ("making path")
        os.makedirs(assetpath)
        
        return assetpath
    
    else:
        return assetpath

def find_most_common_path(path_a, path_b):
    """
    Returns the longest common seqence of charactes shared between two strings, using difflib, from path_a
    This will return the first, longest sequence, if you want to get all the common segments use find_matching_blocks on the sequence matcher.
    This is really for finding out the "base" part of a path that is different so that we can replace the path with a env var.
    
    Arguments
    path_a (str) : A string sequence
    path_b (str) : A string sequence
    """

    match = difflib.SequenceMatcher(None, path_a, path_b).find_longest_match(0,len(path_a),0,len(path_b))
    common = path_a[match.a:match.a + match.size]
    
    return common

def find_not_common_path(path_a, path_b):
    """
    Returns the first longest sequence that is not common from path, using difflib, from path_b

    """
    match = difflib.SequenceMatcher(None, path_a, path_b).find_longest_match(0,len(path_a),0,len(path_b))
    common = path_b[:match.b]
    
    return common

def match_path_sequence(s1, s2):
    """
    Attempts to augment s1 so that it matches s2, using the difflib builtin.
    s2 would be the correct string, s1 would be the string that needs to be updated
    difflib.get_opcodes returns a list of tuples. Each tuple in the list contains the instructions, in order, of how to augment s1 into s2

    This is pretty useless because you already know the string that you want to replace.

    """
    # Creats a match object
    matcher = difflib.SequenceMatcher(None, s1, s2)
    new_string = ""
  
    for x in matcher.get_opcodes():
        # unpacking the tunple
        operation, s1_start, s1_end, s2_start, s2_end = x
        new_string = list(s1)
        # if the two strings are the same at those indexes then there is no need to do anything
        print(operation, s1[s1_start:s1_end], "with", s2[s2_start:s2_end])
        if operation == "equal":    
            continue
        elif operation == "delete":
            del new_string[s1_start:s1_end]            
        elif operation == "replace":
            new_string[s1_start:s1_end] = s2[s2_start:s2_end]
        elif operation == "insert":
            insert = s2[s2_start:s2_end]
            new_string.insert(s1_start, insert)
    
    return "".join(new_string)