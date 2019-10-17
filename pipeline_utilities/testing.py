import os

def getCameraDir():
    temp = "Y:\\tul\\kno\\cut0060\\andre_01\\maya\\scenes\\cut0060_anim_v02_001.mb"
    # temp = "Y:\\ber\\ggg\\cut_011\\sam_01\\maya\\anim\\cut_011_anim_v02.ma"
    scenedir = os.path.dirname(temp)
    dirlist = os.listdir(scenedir)
       
    old = "0_Camera"
    new = "0_camera"
    while old not in dirlist or new not in dirlist:
        scenedir = os.path.abspath(os.path.join(scenedir,"../"))
        # print(scenedir)
        dirlist = os.listdir(scenedir)
        # print(dirlist)
    cameradir = scenedir + "\\0_Camera"
    print(cameradir)
    
                           

getCameraDir()
print("has run")