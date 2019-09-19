import pymel.core as pm

#setting the render settings



def getEditor():
    """
    The modelEditor is the node in maya that contains all the information about a modelPanel. A panel is an object in maya that acts as the root of a ui element. The model editor
    for instance holds information about what cameras have been added to a panel.
    """

    modpanels =  pm.getPanel(type="modelPanel")

    for panel in modpanels:
        if pm.modelPanel(panel,query=True,camera=True) == "camera2":
            modpanel = panel #modpanel is a panel object, so it uses pymel object methods
                
    cameditorname =  pm.modelPanel(modpanel,query=True,modelEditor=True) #cameditor is the name of the editor attatched to the modpanel object
    modeditor = pm.modelEditor(cameditorname)
    # print type(modeditor)
   
   
def runPlayblast():
    
    createWindow()
    pm.playblast(format="image",filename="C:/Users/roger/Documents/maya/projects/default/images/test",compression="jpg",widthHeight=[1920,1080],percent=100)
    

  
