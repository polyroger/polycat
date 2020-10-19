import inspect,os,sys,logging
import DaVinciResolveScript as dvs

# importing outside the main module
sys.path.append(os.path.abspath(os.path.join(__file__,"../../")))

from pipeline_utilities.pc_logging.pc_logger import Pc_Logger


def printMembers(obj):

    members = inspect.getmembers(obj)

    for i in members:
        print(i)

def renderPrevisCuts(savepath,renderpreset,tracknum):

    """
    Adds a render item for every in and out point (clip) on a video track in resolve

    savepath (str) - The path where you want the expoted clips to go to
    renderpreset (str) - The name of the render preset to use in resolve
    tracknum (int) - The track number you want to use for in and our points

    """

    resolve = dvs.scriptapp('Resolve')
    ms = resolve.GetMediaStorage()
    pm = resolve.GetProjectManager()
    proj = pm.GetCurrentProject()
    mp = proj.GetMediaPool()
    timeline = proj.GetCurrentTimeline()

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



if __name__ == "__main__":
    
    #setting the logging level
    Pc_Logger.set_log_level(logging.CRITICAL)
    
    savepath = r"\\YARN\projects\mov\gra\0_aaa\0_internal\0_project_data\previs_sequences"
    renderpreset = "DCPcine"
    tracknum = 1

    renderPrevisCuts(savepath,renderpreset,tracknum)
