import hou
import os
import re
import clique

#houdini python libs
import nodegraphalign as nga

def replaceYarn(filepath):
    
    editedfilepath = filepath.replace("\\","/")
    serverpath = hou.getenv("JOB")
    newfilepath = editedfilepath.replace(serverpath,"$JOB")

    return newfilepath

def createArnoldShader(node,foldername):

    #checking for name conlficts in the shop
    shop = node.parent()
    children = []
    
    for child in shop.children():
        
        children.append(child.name())
    
    #checking for duplicates and renaming this will only work realaible until 9...there shouldnt be more than that
    if foldername in children:

        foldername = foldername + "_1"

        while foldername in children:
            
            nameinc = int(foldername[-1]) + 1
            foldername = foldername[:-1]
            foldername = foldername + str(nameinc)            
        
        print "Shader naming conflict. Renaming to {}".format(foldername)
        
        shader = shop.createNode("arnold_vopnet",foldername)
        surface = shader.createNode("arnold::standard_surface")
        surface.setPosition((-4,0))
        mat = hou.node(shader.path() + "/OUT_material")
        mat.setInput(0,surface,0)
     
        return shader 
        
    else:
        
        shader = shop.createNode("arnold_vopnet",foldername)
        surface = shader.createNode("arnold::standard_surface")
        surface.setPosition((-4,0))
        mat = hou.node(shader.path() + "/OUT_material")
        mat.setInput(0,surface,0)
        
        return shader

def createImageNodes(shader,filename):

    imagenode = shader.createNode("arnold::image",filename)

    return imagenode

def getNetworkEditor():

    network_editor = None

    for pane_tab in hou.ui.paneTabs():

        if isinstance(pane_tab, hou.NetworkEditor):
            
            network_editor = pane_tab
            
            return network_editor

def createTextureParms(node,texturecat,parmgroup):
    """
    Creates a parmgroup that consists of string paramaters it will create as many paramaters as there are 
    files in texturelist, removes the <udim> tag for naming of the paramater

    Expects a texture catagory path and the parmgroup of a node

    Returns a parm group object that coinains a paramater entry for each item in the texture catagory foder
        
    """
    shadernodes = []
    imagenodes = []
    
    
    #this section removes any trailing slashes from the path and checks whether there are files or folders or both in the texturepath
    
    if texturecat[-1] == "/" or texturecat[-1] == "\\":
        texturecat = texturecat[:-1]
    
    folderlist = []

    for i in os.listdir(texturecat):
        path  = texturecat + "/" + i
        if os.path.isdir(path):
            folderlist.append(i)
    if not folderlist:
        folderlist.append(os.path.basename(texturecat))
        
    textures = parmgroup.find("textures")

    pfolders = []
    filelist = []
    mydict = {}

    exclusionlist = [".tx",".db"]

    # makes the initial dictionary that consists of the names of all the folders in the base texture catagory and then assigns an empty list as its value
    for folder in (folderlist):
        
        mydict[folder] = []

    # runs over every key (texture folder name) and finds all the files / file paths from that point down the folder structure. If there are no folders in the
    # texture path which should be iether laters or dev then use the texurepath as the path
    for key in mydict.keys():

        if key == os.path.basename(texturecat):
            texpath = os.path.abspath(texturecat)
        else:
            texpath = os.path.abspath(os.path.join(texturecat,key))

        #creates dict with key of folder name and value as a list of lists that have a filenam and filepath for every texture in the folder.
        filecollection = os.listdir(texpath)
        collections,single = clique.assemble(filecollection,minimum_items=1)

        for i in collections:

            if i.tail in exclusionlist:
                continue

            head = i.head
            tail = i.tail
            tag = "<udim>"

            # if len(i.indexes) == 1:
            #     tag = str(list(i.indexes)[0])

            fname = head + tag + tail
            filepath = os.path.abspath(os.path.join(texpath,fname))
            filename = str(head.replace(" ","_"))
            mydict[key].append([filename,filepath])

        for i in single:

            head,tail = os.path.splitext(i)
            #this exculdes what is in the list of if there are and directories in the folder
            if tail in exclusionlist or not tail:
                continue
            
            filepath = os.path.abspath(os.path.join(texpath,i))
            filename = str(head.replace(" ","_"))
            mydict[key].append([filename,filepath])


    # at this stage mydict should have this structure {texturefolder:[[filename,filepath],[filename,filepath],etc,etc]} - a dictionary that contains foldername key and a value of a list of lists
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
        shadernodes.append(shader)
        shader.createNode("arnold::standard_surface")
        

        for path in filelist:
            imagefilename = path.name()
            imagenode = createImageNodes(shader,imagefilename)
            imagenodes.append(imagenode)
            imagenode.parm("filename").set(path.defaultValue()[0])
        
        # stores that folder template so it doesnt get lost in the loop
        pfolders.append(folder)
        
        # clears the filelist so that the new list can be built from the new key, if this isnt cleared you will just append the next paramater list and your last folder parm will contain all the files
        filelist = []
    
    # Aligns all the shaders
    for node in shadernodes:
        
        node.setSelected(True)
    
    nga.alignConnected(getNetworkEditor(),None,hou.Vector2(1,1),"down")
    
    #  sets an in memory copy of the textures folder that now contains all the folders and the folders all the string paramaters, then replaces the current parmgroup textures folder with the in memory one
    textures.setParmTemplates(pfolders)
    parmgroup.replace("textures",textures)

    #you need to return the parmgroup so you can set the parmgroup in the hda script.
    return parmgroup

def importTextures(folderroot,node):

    #Some checks to see if the texture path is valid or not
    if not os.path.exists(folderroot) or not os.path.isdir(folderroot):
    
        hou.ui.displayConfirmation("Please make sure that the texture path is a valid directory")
    
        return
    
    elif not os.listdir(folderroot):
    
        hou.ui.displayConfirmation("There are no textures in the selected texture path")
    
        return
    
    elif str(folderroot).endswith("/"):

        folderroot = folderroot[:-1]
    
    
    exclusionlist = [".tx",".db",".ass"]
    folderexclusionlist = [".mayaSwatches"]
    fixedfolderroot = folderroot.replace("/","\\")
    nodex,nodey = node.position()
    incx,incy = (5,0)

    #stepping through all the files within the selected folderroot
    for root,dirs,files in os.walk(fixedfolderroot):
        
        a = os.path.split(root)[1]
        
        if a in folderexclusionlist:
            continue

        filelist = []

        #creating a file list for a clique collection, this should iterate for each new root
        for f in files:
            
            if os.path.splitext(f)[1] not in exclusionlist:

                folder = os.path.split(root)[1]
                filelist.append(f)
        
        collections,single = clique.assemble(filelist,minimum_items=1)
        shader = createArnoldShader(node,a)
        shader.setPosition((nodex + incx,nodey + incy))

        #increments are for the node positions
        incx += 0
        incy += -1

        if single:
            
            singlex = -10
            singley = 0
        
            # iterating incase there is more than one single in a folder
            for s in single:

                filepath = replaceYarn(os.path.abspath(os.path.join(root,s)))
                imagenode = createImageNodes(shader,s)
                imagenode.setPosition((singlex,singley))
                imagenode.parm("filename").set(filepath)

                singlex += 0
                singley += -2

        collectionx = -10
        collectiony = 0
        udimcollectionx = -10
        udimcollectiony = 0

        #finding all the udim sequences
        for i in collections:

            head = i.head
            tail = i.tail
            tag = "<udim>"

            # sequence of udims
            if len(i.indexes) > 1:
                
                fname = head + tag + tail
                filepath = replaceYarn(os.path.abspath(os.path.join(root,fname)))
                imagenode = createImageNodes(shader,head)
                imagenode.setPosition((udimcollectionx,udimcollectiony))
                imagenode.parm("filename").set(filepath)

                print(udimcollectionx,udimcollectiony)

                udimcollectionx += 0
                udimcollectiony += -3
            
            # single udim
            else:
                
                index = list(i.indexes)
                fname = head + str(index[0]) + tail
                filepath = replaceYarn(os.path.abspath(os.path.join(root,fname)))
                imagenode = createImageNodes(shader,head)
                imagenode.setPosition((collectionx,collectiony))
                imagenode.parm("filename").set(filepath)

                collectionx += 0
                collectiony += -3