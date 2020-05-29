import hou
import os
import re

def getTextureCatagory(texpath):

    """
    Create a Label ( folder name) / token (path of folder) pair to use in buildin a menu in the type properties.

    Returns a even list of name and token value

    TIP : hou.evalAsString() to the the string token value
    """
    
    texcat = []
    for i in os.listdir(texpath):
        catpath = texpath + i
        texcat.extend((catpath,i))

    return texcat    



def udimCheck(texturedict):
    """
    Expects a list of texture files, checks the file for udim number padding eg file_1001.exr
    and replaces the 1001 with the arnold <udim> tag and removes all but one instance of the file with the new name

    Returns: A sorted list of files, with udim handling
    
    """
    for key,value in texturedict.items():
            
        #checks for udim and replaces the padding to the udim tag
        edited = re.sub(r"[0-9]{4}","<udim>",value)
        texturedict[key] = edited
    
    cleanudim = {}

    for key,value in texturedict.items():
        if value not in cleanudim.values():
            cleanudim[key] = value
    

#   use the get() method on a dictionary so that the code doesnt error when going through the loop. It will only find the dictionary entry if is exists in the current iteration
#   of the loop.
    # print cleanudim.get("frog_body_cavity_1002")

    return cleanudim
    
      
def createTextureParms(texturecat,parmgroup):
    """
    Creates a parmgroup that consists of string paramaters it will create as many paramaters as there are 
    files in texturelist, removes the <udim> tag for naming of the paramater

    Expects a texture catagory path and the parmgroup of a node

    Returns a parm group object that coinains a paramater entry for each item in the texture catagory foder
        
    """
    print("\n\nStart of createTextureParms \n **************************************************** \n")
    
    folderlist = os.listdir(texturecat)
    textures = parmgroup.find("textures")

    pfolders = []
    filelist = []
    mydict = {}
  
    # makes the initial dictionary that consists of the names of all the folders in the base texture catagory and then assigns an empty list as its value
    for folder in (folderlist):
        
        mydict[folder] = []

    # runs over every key (texture folder name) and finds all the files / file paths from that point down the folder structure
    for key in mydict.keys():

        texpath = os.path.abspath(os.path.join(texturecat,key))
        
        for root,dirs,files in os.walk(texpath):
                    
                for i in files:
                    
                    filepath = os.path.abspath(os.path.join(root,i))
                    basepath = os.path.basename(filepath)
                    filename,ext = os.path.splitext(basepath)
                    
                    # if the file is of the correct type it appends a [filename,filepath] list to the current dictionary key value. 
                    if ext != ".tx" and ext != ".db":
                        mydict[key].append([filename,filepath])

    # at this stage mydict shoudl have this structure {texturefolder:[[filename,filepath],[filename,filepath],etc,etc]} - a dictionary that contains foldername key and a value of a list of lists
    # this loops over the items in the dictionary
    for key,value in mydict.items():
     
        # this loops over the value list [filename,filepath] and creates the houdini string paramater using the filename and sets the default value with to the filepath
        for i in mydict[key]:

            sparm = hou.StringParmTemplate(i[0].lower(),i[0].upper(),1,string_type=hou.stringParmType.FileReference)
            sparm.setDefaultValue([i[1]])
            # appends all the string paramaters that are ascociated with the current texture folder and stores them in a list
            filelist.append(sparm)
       
        # creates the folder template with the dict key as the name and adds the list of ascociated string templates to it, this folder variable will be overwritten at each stage of the loop       
        folder = hou.FolderParmTemplate(key.lower(),key.upper(),parm_templates=filelist)
        # stores that folder template so it doesnt get lost in the loop
        pfolders.append(folder)
        # clears the filelist so that the new list can be built from the new key, if this isnt cleared you will just append the next paramater list and your last folder parm will contain all the files
        filelist = []

    
    #  sets an in memory copy of the textures folder that now contains all the folders and the folders all the string paramaters, then replaces the current parmgroup textures folder with the in memory one
    textures.setParmTemplates(pfolders)
    parmgroup.replace("textures",textures)

    #you need to return the parmgroup so you can set the parmgroup in the hda script.
    return parmgroup
       

# #  START of the simple working setup that i used for a base understanding


#     parm1 = hou.StringParmTemplate("parm1","parm1",1,string_type=hou.stringParmType.FileReference)
#     parm2 = hou.StringParmTemplate("parm2","parm2",1,string_type=hou.stringParmType.FileReference)

#     parm3 = hou.StringParmTemplate("parm3","parm3",1,string_type=hou.stringParmType.FileReference)
#     parm4 = hou.StringParmTemplate("parm4","parm4",1,string_type=hou.stringParmType.FileReference)
    
    
#     parmlist1 = [parm1,parm2]
#     parmlist2 = [parm3,parm4]

#     folder1 = hou.FolderParmTemplate("arrow_name","arrow_label",parm_templates=parmlist1)
#     folder2 = hou.FolderParmTemplate("body_name","body_label",parm_templates=parmlist2)

#     parmteplatelist = [folder1,folder2]

#     textures.setParmTemplates(parmteplatelist)

#     parmgroup.replace("textures",textures)     


#     return parmgroup 


            
        
       


        
    



     