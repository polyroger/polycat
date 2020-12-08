"""
Backend function for the simple ffmpeg wav converter ui
"""

import pathlib,subprocess


def convert_to_wav(ffmpeg_path,filelist):

    wavcodec = "pcm_s16le"
    ffmpeg_args = ffmpeg_path
    map_inc = 0
    ffmpeg_args = [ffmpeg_path]

    for f in filelist:
        filename = pathlib.Path(f)
        parent = filename.parent
        x = filename.stem
        newname = str(x) + "_mayawav.wav"
        newpath = parent / newname
        
        ffmpeg_args.extend(["-i","{0}".format(f)])
        ffmpeg_args.extend(["-map","{0}:a".format(str(map_inc))])
        ffmpeg_args.extend(["-acodec","{0}".format(wavcodec)])
        ffmpeg_args.extend(["{0}".format(newpath)])

        map_inc += 1
    
    subprocess.run(ffmpeg_args)