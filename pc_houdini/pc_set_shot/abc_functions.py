import _alembic_hom_extensions as abc


def getResolutionFromCamera(filepath):

    camtransform = "/houdini_camera"
    camshape = "/houdini_camera/houdini_cameraShape"

    x = abc.alembicUserProperty(filepath,camtransform,"resx",1)[0][0]
    y = abc.alembicUserProperty(filepath,camtransform,"resy",1)[0][0]

    return (x,y)

    