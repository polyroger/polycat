"""
Polycat animations nuke init

NOTES
The nuke init is able to read variables set in the shell nuke was launched from.
To set dynamic properties from shell varaibles you need to set them in the init.
Use the menu.py for settings that dont rely on shell variables.
"""


import os

#keep adding the path to the new pluginn
nuke.pluginAddPath(r"./python_scripts")
nuke.pluginAddPath(r"./cryptomatte")
nuke.pluginAddPath(r"./autoflare")
nuke.pluginAddPath(r"./victor_tools")
nuke.pluginAddPath(r"./x_tools")
nuke.pluginAddPath(r"./pc_plugins")

def add_favorite_directory():

    """
    Sets the default script directory to the cut\username where nuke was launced from
    """
    try:
        nuke_artist = os.environ["COMP_ARTIST_PATH"]
        nuke.addFavoriteDir(
            name = "CUT_USER",
            directory = nuke_artist,
            type = nuke.SCRIPT
        )
    except:
        print("could net set the script favorite directory")


add_favorite_directory()