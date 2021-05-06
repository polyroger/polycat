"""
Polycat animaions rig exporter backend

TODO:
remove the filename validation from the ui and add it here

"""
import maya.cmds as cmds


def hideNodeHistory(x):
    """
    Hides the "interesting" history on all nodes in the scene.
    Arguments
    x (bool) : Is the history worth keeping or not, False hides, True unhides.
    """
    nodeList = cmds.ls()
    for n in nodeList:
        cmds.setAttr(str(n) + '.isHistoricallyInteresting', x)