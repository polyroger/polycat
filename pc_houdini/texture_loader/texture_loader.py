import hou
import os
import re

def replaceYarn(filepath):
    
    editedfilepath = filepath.replace("\\","/")
    serverpath = hou.getenv("JOB")
    newfilepath = editedfilepath.replace(serverpath,"$JOB")

    return newfilepath


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


def findUdim(filepath):
    """
   Expexts a texture path or filename and returns true if the file is a normal texture or it has 1001 in the name.
   All UDIMS should start at 1001
   Use udimRename() to replace the 1001 with <udim> for arnold
    
    """
    udimpattern = r"(?!1001)\d{4}"
    if not re.search(udimpattern,filepath):
        return True
    else:
        return False

def udimRename(filename,replacewith):
    """
    Just a function to be used with replaceing the 1001 to arnolds <udim>
    """

    pattern = r"(1001)"
    newfilename = re.sub(pattern,replacewith,filename)

    return newfilename

def clearTextureParms(node,parmgroup):
    """
    creates and empty folder template and replaces the current "textures" template so that the textures can be refreshed.
    returns a copy of the input parmgroup that has an empty "textures" folder
    """

    texturefolder = parmgroup.findFolder("textures")
    emptyfolder = hou.FolderParmTemplate("textures","textures")
    parmgroup.replace(texturefolder,emptyfolder)

    return parmgroup

def createArnoldShader(node,foldername):

    shop = node.parent()
    children = []
    
    for child in shop.children():
        children.append(child.name())
    
    if foldername in children:
        print "there is already a shader with the same name as the texture folder" 
        return None
    else:
        shader = shop.createNode("arnold_vopnet",foldername)
        return shader

def createImageNodes(shader,filename):

    imagenode = shader.createNode("arnold::image",filename)

    return imagenode


def createTextureParms(node,texturecat,parmgroup):
    """
    Creates a parmgroup that consists of string paramaters it will create as many paramaters as there are 
    files in texturelist, removes the <udim> tag for naming of the paramater

    Expects a texture catagory path and the parmgroup of a node

    Returns a parm group object that coinains a paramater entry for each item in the texture catagory foder
        
    """
    print("refreshing texture contents....")

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
                    
                    # if the file is of the correct type and it gets udim checked it appends a [filename,filepath] list to the current dictionary key value. 
                    if ext != ".tx" and ext != ".db" and findUdim(i):
                        
                        filepath = udimRename(filepath,"<udim>")
                        filename = udimRename(filename,"")
                        mydict[key].append([filename,filepath])

    # at this stage mydict shoudl have this structure {texturefolder:[[filename,filepath],[filename,filepath],etc,etc]} - a dictionary that contains foldername key and a value of a list of lists
    # this loops over the items in the dictionary
    for key,value in mydict.items():
     
        # this loops over the value list [filename,filepath] and creates the houdini string paramater using the filename and sets the default value with to the filepath
        for i in mydict[key]:

            sparm = hou.StringParmTemplate(i[0].lower(),i[0].upper(),1,string_type=hou.stringParmType.FileReference)
            sparm.setDefaultValue([replaceYarn(i[1])])
            # appends all the string paramaters that are ascociated with the current texture folder and stores them in a list
            filelist.append(sparm)
       
        # creates the folder template with the dict key as the name and adds the list of ascociated string templates to it, this folder variable will be overwritten at each stage of the loop       
        folder = hou.FolderParmTemplate(key.lower(),key.upper(),parm_templates=filelist)
        
        # creating the shader and image nodes
        shader = createArnoldShader(node,folder.name())
        shader.createNode("arnold::standard_surface")
        
        for path in filelist:
            imagefilename = path.name()
            imagenode = createImageNodes(shader,imagefilename)
            imagenode.parm("filename").set(path.defaultValue()[0])
        
        # stores that folder template so it doesnt get lost in the loop
        pfolders.append(folder)
        # clears the filelist so that the new list can be built from the new key, if this isnt cleared you will just append the next paramater list and your last folder parm will contain all the files
        filelist = []

   
   
    #  sets an in memory copy of the textures folder that now contains all the folders and the folders all the string paramaters, then replaces the current parmgroup textures folder with the in memory one
    textures.setParmTemplates(pfolders)
    parmgroup.replace("textures",textures)

    #you need to return the parmgroup so you can set the parmgroup in the hda script.
    return parmgroup
       
#TODO
"""
Add in a way to create arnold image nodes that auto link to the texture path.
some sort of reload or refresh - done

"""



            
        
       


        
    



     