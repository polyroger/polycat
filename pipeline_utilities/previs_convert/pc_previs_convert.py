import pathlib
import os

def ffmpegArgList(filelist,fps,start_number):
    """
    Needs python3 and subprocess
    Splits the supplied video into frames and audio

    filelist   - The path list to the files that needs to be split
    fps     - The frame rate you want to have, ie 24
    start_number    - The starting frame number you want to exported sequence to start
    destination     - [optional] where you want the auido and video to go to

    Returns - An formatted argument to be used in ffmpeg

    """
    
    FFMPEG = r"\\YARN\projects\pipeline\utilities\ffmpeg\bin\ffmpeg.exe"
    FRAMES = "_frames"
    FEXT = ".jpg"
    AUDIO = "_audio"
    AEXT = ".wav"
    vfile_inc = 0

    # hides some of the ffmpeg output
    args = [FFMPEG]
    args.extend(["-hide_banner","-y"])

    for vfile in filelist:

        fileobj = pathlib.Path(vfile)
        name = fileobj.stem
        ext = fileobj.suffix

        path = fileobj.parent / name


        if not path.exists():
            path.mkdir(parents=True)
        
        framename = str(name) + FRAMES + "." + r"%04d" + FEXT
        audioname = str(name) + AUDIO + AEXT

        frame_path = str(path / framename)
        audio_path = str(path / audioname)


        args.extend(["-i","{}".format(vfile)])
        args.extend(["-map","{}:0".format(str(vfile_inc)),"-vf","fps={}".format(fps),"-start_number","{}".format(str(start_number)),frame_path])
        args.extend(["-map","{}:1".format(str(vfile_inc)),audio_path])

        vfile_inc += 1

    return args

def allFilesInFolders(folderpath):
    """
    Returns a list of the file paths for all files that are a child of the folderpath and whos extensions are in the ext_list

    folderpath (str) - A path the a folder
    """

    ext_list = [".mp4",".mov",".avi"]
    filelist = []

    for root,dirs,files in os.walk(folderpath):
        
        for f in files:
            vpath = os.path.join(root,f)
            filelist.append(vpath)
    
    return filelist

def copyFilesToShots():
    """
    Copies the previs files into the relative shot folders.
    """





