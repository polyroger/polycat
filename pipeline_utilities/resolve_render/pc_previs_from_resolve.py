"""
python3.6
For resolve to connect you need to have these variables set up

!!!! YOU NEED TO BE RUNNING RESOLVE STUDIO..REGULAR RESOLVE DOES NOT ALLOW ACCESS OUTSIDE OF THE FUSION PANEL

RESOLVE_SCRIPT_API="%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\"
RESOLVE_SCRIPT_LIB="C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
PYTHONPATH="%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules\"

As resolve is not widely used this can remain local and not added to the environment

A single running instance of resolve is required as well as running the tool with python 3.6 (it seems that resolve is sensitive to the version)

"""
import os,sys,logging
import DaVinciResolveScript as dvs

# getting to the logging module
sys.path.append(os.path.join(__file__,"../../../"))
from pipeline_utilities.pc_logging.pc_logger import Pc_Logger



def connetToResolve():
    """
    Creates the resolve projec variables for easier creation of functions
    """

    Pc_Logger.set_log_level(logging.DEBUG)

    resolve_dict = {}
    
    try: 
        
        resolve_dict["resolve"] = dvs.scriptapp('Resolve')
        resolve_dict["ms"] = resolve_dict["resolve"].GetMediaStorage()
        resolve_dict["pm"] = resolve_dict["resolve"].GetProjectManager()
        resolve_dict["proj"] = resolve_dict["pm"].GetCurrentProject()
        resolve_dict["mp"] = resolve_dict["proj"].GetMediaPool()
        resolve_dict["timeline"] = resolve_dict["proj"].GetCurrentTimeline()

        Pc_Logger.info( "resolve =  {0}\n"
                        "ms =       {1}\n"
                        "pm =       {2}\n"
                        "proj =     {3}\n"
                        "mp =       {4}\n"
                        "timeline = {5}".format(resolve_dict["resolve"],resolve_dict["ms"],resolve_dict["pm"],resolve_dict["proj"],resolve_dict["mp"],resolve_dict["timeline"]))

        return resolve_dict
    
    except:
        
        Pc_Logger.exception("There was an error in the {0} try block. !! Make sure that resolve is running and using python3.6 !!".format(connetToResolve.__name__))

        return False

def createCBoxItemsList(combobox,itemlist):
    """
    Create the data in a combo box. At the moment it simple iterates through the list and assigns the label / value to an index in the list
    args:
    conbobox = a Qwidget.combobox 
    itemlist = a list of strings that you want to add into the combobox
    """

    if itemlist:

        for item in itemlist:
            combobox.addItem(item,item)
        
        return combobox
    
    else:
    
        Pc_Logger.error("The list of items passed to the createCBoxItems is not True")
        
        return None

def createCBoxItemsFromObj(combobox,obj):
    """
    Use this when you what to return objects from combo boxes rather than just strings
    It assumes that the object has a method that allows it to get a string that can be used as its label
    ARGS
    combobox (combobox pyside2 object) : The combobox you want to edit
    obj (list) : list of objects

    note that the findData method on a combobox will only find Qtcore.Qobject objects
    https://stackoverflow.com/questions/34024525/why-doesnt-qcombobox-finddata-accept-an-object-as-input
    
    """

    if obj:

        for item in obj:
            combobox.addItem(item.GetName(),item)
        
        return combobox

    else:

        Pc_Logger.error("createCBoxItemsDict: The combodict is false")

        return None

def getTrackList(resolve_project,timeline_name,tracktype="video"):
    """
    Gets the number of tracks available in the timeline and returns a list to be used with createCBoxItems
    ARGS
    resolve_timeline (resolve timeline object) : The timeline retured from quering the project
    tracktype (str) : "audio" "video" "subtitle"
    """
    # gets the timeline name from the ui, the sets it to be the currect so that the timeline object can be sourced from the name rather than and index
    resolve_timeline = resolve_project.GetCurrentTimeline()

    total_tracks = int(resolve_timeline.GetTrackCount(tracktype))
    track_list = []

    for track in range(total_tracks):
        track_list.append(str(track+1))

    return track_list

def getTimelineObjects(resolve_project):
    """
    For a given project return a list of objects, resolce api doesnt have anythin that gets the timeline by name
    sets the currect timeline as the fist option in the list.
    ARGS
    resolve_project(obj) - The resolve project object
    """

    num_timelines = int(resolve_project.GetTimelineCount())
    current_timeline = resolve_project.GetCurrentTimeline()
    timeline_objects = []
    
    for index in range(num_timelines):
        
        index = float(index+1)
        timeline = resolve_project.GetTimelineByIndex(index)

        if timeline.GetName() == current_timeline.GetName():
            continue

        timeline_objects.append(timeline)
    
    # there is a special method that python uses to check object equality [__eq__] if an object does not have this you can not directly compare objects.
    # so I compare the name in the loop and skip it if its true, then add as the first index in the list so that its set as the starting timeling in the ui
    timeline_objects.insert(0,current_timeline)
        
    Pc_Logger.info("timeline list = {}".format(timeline_objects))
    
    return timeline_objects

def currentTimeline(resolve_project):
    """
    Gets the current timeline from resolve
    """
    return resolve_project.GetCurrentTimeline()

def renderPrevisCuts(proj,savepath,timeline,tracknum,renderpreset):

    """
    Adds a render item for every in and out point (clip) on a video track in resolve

    savepath (str) - The path where you want the expoted clips to go to
    timeline (str) - The timeline name that you want to act on
    renderpreset (str) - The name of the render preset to use in resolve
    tracknum (int) - The track number you want to use for in and our points

    """
    timeline_name = timeline.GetName()
    items  = timeline.GetItemListInTrack("video",tracknum)

    scene_path = os.path.join(savepath,timeline_name)

    for item in items:
    
        proj.LoadRenderPreset(renderpreset)
        
        mp_item = item.GetMediaPoolItem()
        namedict = mp_item.GetClipProperty("Clip Name")
        name = os.path.splitext(namedict["Clip Name"])[0]

        render_path = os.path.join(scene_path,name)

        if not os.path.isdir(render_path) :
            os.makedirs(render_path)
        
        duration = item.GetDuration()
        start = item.GetStart()
        end = item.GetEnd()-1

        settings = {"MarkIn":start,"MarkOut":end,"TargetDir":render_path,"CustomName":name}
        
        # logging for debug
        Pc_Logger.info("{0}\nin\t{1}\nout\t{2}\npath\t{3}\n".format(name,settings["MarkIn"],settings["MarkOut"],settings["TargetDir"]))
        
        proj.SetRenderSettings(settings)
        proj.AddRenderJob()


    # there seems to be a bug where the in and outs of the last clip dont get set correctly. So you have to add a dummy clip to the end then delete it
    # this just hangles the render job
    
    lastjob = len(proj.GetRenderJobList())

    if lastjob > 0:

        proj.DeleteRenderJobByIndex(lastjob)


    # proj.StartRendering()

