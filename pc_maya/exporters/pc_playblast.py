import pymel.core as pm
from pipeline_utilities import filenaming

#setting the render settings


def getEditor():
    """
    The modelEditor is the node in maya that contains all the information about a modelPanel. A panel is an object in maya that acts as the root of a ui element. The model editor
    for instance holds information about what cameras have been added to a panel.
    """
    camview = pm.ls(selection=True)[0]
    modpanels =  pm.getPanel(type="modelPanel")

    for panel in modpanels:
        print(panel)
        if pm.modelPanel(panel,query=True,camera=True) == camview:
            modpanel = panel #modpanel is a panel object, so it uses pymel object methods

    print (type(modpanel))
             
    cameditorobj =  pm.modelPanel(modpanel,edit=True) #cameditor is a modelPanel object, you pass a panel object to get the modelPanel
    print (type(cameditorobj))
    modeditor = pm.modelEditor(cameditorobj,edit=True,activeView=True) #this is a modeleditor object

def saveLocation():
    
    startpath = filenaming.getexportdir("playblast")
    print (startpath)
    # savepath = pm.fileDialog2(am=1,ds=2,fm=2,)
 
   
   
def runPlayblast():
    
    getEditor()
    pm.playblast(format="image",filename="C:/Users/roger/Documents/maya/projects/default/images/test",compression="jpg",widthHeight=[1920,1080],percent=100)
    

  

