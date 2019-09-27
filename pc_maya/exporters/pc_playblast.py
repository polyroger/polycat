import pymel.core as pm
<<<<<<< HEAD
=======
from pipeline_utilities import filenaming
>>>>>>> 6df99589bff6912da484cf221b46ec5e4ec05804

#setting the render settings


<<<<<<< HEAD
pm.deleteUI("window",window=True,panel=True)

#windows are created in a heiracy so the order of these commands are important,
#when you create a window everything after that becomes a child of the window object

window = pm.window('window')
form = pm.formLayout()
editor = pm.modelEditor()
column = pm.columnLayout('true')

pm.formLayout( form, edit=True, attachForm=[(column, 'top', 0), (column, 'left', 0), (editor, 'top', 0), (editor, 'bottom', 0), (editor, 'right', 0)], attachNone=[(column, 'bottom'), (column, 'right')], attachControl=(editor, 'left', 0, column))


camera= pm.ls(selection=True)[0]

#    Attach the camera to the model editor.
pm.modelEditor( editor, edit=True, camera=camera[0] )

pm.showWindow( window )

#This deletes the window after it has been created
#pm.deleteUI("window",window=True,panel=True)
=======
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

    print type(modpanel)
             
    cameditorobj =  pm.modelPanel(modpanel,edit=True) #cameditor is a modelPanel object, you pass a panel object to get the modelPanel
    print type(cameditorobj)
    modeditor = pm.modelEditor(cameditorobj,edit=True,activeView=True) #this is a modeleditor object

def saveLocation():
    
    startpath = filenaming.getexportdir("playblast")
    print startpath
    # savepath = pm.fileDialog2(am=1,ds=2,fm=2,)
 
   
   
def runPlayblast():
    
    getEditor()
    pm.playblast(format="image",filename="C:/Users/roger/Documents/maya/projects/default/images/test",compression="jpg",widthHeight=[1920,1080],percent=100)
    

  
>>>>>>> 6df99589bff6912da484cf221b46ec5e4ec05804

