import hou

def importCheck():
    print("texture loader imported")
    print("test")

    mynode = hou.node(".")
    parmgroup = mynode.parmTemplateGroup()
    
    print("running1")

    myfile = hou.StringParmTemplate("filename","filelabel",1,string_type=hou.stringParmType.FileReference)
    myfile2 = hou.StringParmTemplate("filename2","filelabel2",1,string_type=hou.stringParmType.FileReference)
    
    myfolder = hou.FolderParmTemplate("foldername","folderlabel")
    myfolder.addParmTemplate(myfile)
    myfolder.addParmTemplate(myfile2)

    print "running2"

    parmgroup.append(myfolder)

    mynode.setParmTemplateGroup(parmgroup)



"""
folderSetTemplate
    folderTEmplates
        parmTemplates


"""

 

   


    


