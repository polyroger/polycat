
import hou
import os
import re

# phsudocode for generating the folders / paramater templates, need to work on how to set the paramater values. Currently using a list wich wont work
# so nice now, look at setting the path before doing any udim tagging

# create paramater group

# def createTemplates(parmGroup):

# 	for folder in os.listdir(texture catagory):
		
# 		for name in os.listdir(texture catagory + folder)
			
# 			foldertemplate = mynode.folderParmTemplate()
# 			foldertemp.setName(name)
			
# 			for root,dirs,files in os.walk(texture catagory + "/" + folder + "/" + name):
				
# 				for i in files:
# 					parmtemplate = hou.StringParmTemplate()
# 					parmtemplate.setName(i)
# 					foldertemp.addParmTemplate(parmtemplate)

# 			parmGroup.addFolderTemplate()

# 	return parmGroup









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



def getTextureList(texpath):
    """
    Filters the given path for all files that DONT match certain extensions
    Uses the os module, you will need to import it for this to work
    Returns a list of files
    
    """
    #filter through the texture folder and get only the textures
    textures = []
    for root,dirs,files in os.walk(texpath):
        print root
        print dirs
        print files
               
        for i in files:
            
            filename,ext = os.path.splitext(i)
            if ext != ".tx" and ext != ".db":
                textures.append(i)
       
    textures.sort() 
    
    return textures    

def udimCheck(texturelist):
    """
    Expects a list of texture files, checks the file for udim number padding eg file_1001.exr
    and replaces the 1001 with the arnold <udim> tag and removes all but one instance of the file with the new name

    Returns: A sorted list of files, with udim handling
    
    """
    for j,i in enumerate(texturelist):
            
        #checks for udim and replaces the padding to the udim tag
        edited = re.sub("[0-9]{4}","<udim>",i)
        texturelist[j] = edited
    
    texturelist = list(set(texturelist))
    texturelist.sort()

    return texturelist
    
      
def createTextureParms(texturelist,parmgroup):
    """
    Creates a parmgroup that consists of string paramaters that are used a file paramaters, it will create as many paramaters as there are 
    files in texturelist, removes the <udim> tag for naming of the paramater

    Expects a sorted texture list and a hou.parmTemplateGroup object

    Returns a parm group object that coinains a paramater entry for each item in the texture list
        
    """

    for i in texturelist:

        f,ext = os.path.splitext(i)
        name = f.replace("_<udim>","")
        
      # creates a unique instance of a string template and adds it into the folder parm
        filetemplate = hou.StringParmTemplate(name,name,1,string_type=hou.stringParmType.FileReference)
      # folderparm.addParmTemplate(filetemplate)    this is if you want to add to a folder, append this to the parm group
        parmgroup.append(filetemplate)

  
    return parmgroup   


def setTextureParms(parmgroup,mynode,texpath,texturelist):
    """
    Sets the parms that are gernerated in the parmgroup to the texture path that they corrispond to

    This is dirty...the parmgroup.parmTemplate will include all the paramaters that are in the otl. so the list that gets generated also includes the folder
    "assettex" you have to bypass that to get to the parmtemplates that you have added, and then add that offset to the texturelist index to get the right value
    This is not ideal and will most likely break in the future. A better way would be to construct a fully new parmfolder or group and add in the items there but
    that creates another folder which I didnt want...just a heads up from me to you all these templates can get confusing.

    """

    #setting the texture path of the template
        
    for h,i in enumerate(parmgroup.parmTemplates()):

         if i.name() == "assettex":
             continue
         else:
             mynode.parm("./" + i.name()).set(texpath + texturelist[h-1])
            
             
        
       


        
    



     