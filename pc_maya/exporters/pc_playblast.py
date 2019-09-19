import pymel.core as pm

#setting the render settings


def createWindow():

    # just for testing so the if a window gets created from the script it will get deleted first
    # pm.deleteUI("window",window=True,panel=True)

    #windows are created in a heiracy so the order of these commands are important,
    #when you create a window everything after that becomes a child of the window object

    window = pm.window('window')
    form = pm.formLayout()
    editor = pm.modelEditor()
    column = pm.columnLayout('true')

    pm.formLayout( form, edit=True, attachForm=[(column, 'top', 0), (column, 'left', 0), (editor, 'top', 0), (editor, 'bottom', 0), (editor, 'right', 0)], attachNone=[(column, 'bottom'), (column, 'right')], attachControl=(editor, 'left', 0, column))


    camera= pm.ls(selection=True)[0]

    #    Attach the camera to the model editor.
    pm.modelEditor( editor, edit=True, camera=camera[0], activeView=True )

    pm.showWindow( window )


    return editor

def runPlayblast():
    
    createWindow()
    pm.playblast()

  
