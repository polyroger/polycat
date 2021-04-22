import gazu,os

##### LOGGING IN ####

def kLogin():
    """
    A login function to make logging in to the kitsu api a little faster.
    Returns None
    """
    #manager
    USERNAME = os.getenv("KUSER")
    PASSWORD = os.getenv("KPWORD")

    gazu.set_host("https://polycat.cg-wire.com/api")
    gazu.log_in(USERNAME, PASSWORD)

    return "Logged into the kitsu api"

def k_local_Login():
    """
    A login function to make logging in to the kitsu api a little faster.
    Returns None
    """
    #manager
    USERNAME = os.getenv("KUSER")
    PASSWORD = os.getenv("KPWORD")

    gazu.set_host("http://192.168.4.11/api")
    gazu.log_in(USERNAME, PASSWORD)

    return "Logged into the kitsu api"


##### GETTING PROJECT DATA #######

def getKProject(projname):
    """
    Make sure that you log in to the kitsu api from the shell that you are running this from.
    args:
    projname = The name of the projcet on kitsu
    returns: A kitsu project dict
    """
    project = gazu.project.get_project_by_name(projname)

    return project

def getKProjectAssetTypes(kproject):
    """
    args:
    kproject = the kitsu project dict where you want to pull the assets from.
    returns a kdict for each assettype name
    """
    kassettypes = gazu.asset.all_asset_types_for_project(kproject)

    assettypes = {}

    for assetdict in kassettypes:
        assettypes[assetdict["name"]] = assetdict

    return assettypes

def getKProjectAssets(kproject,kassettype):
    """
    args:
    kproject = the kitsu project dict where you want to pull the assets from.
    kassettype = the asset type kitsu project dict
    returns a LIST of dicts where each dict represents the assets types in the project
    """
    assets = gazu.asset.all_assets_for_project_and_type(kproject,kassettype)

    return assets

def getKProjectSequences(kproject):
    """
    args:
    kproject = the kitsu project dict where you want to pull the assets from.
    returns a LIST of sequence dicts
    """
    ksequences = gazu.shot.all_sequences_for_project(kproject)
    sequences = {}
    
    for seqdict in ksequences:
        sequences[seqdict["name"]] = seqdict

    return sequences

def getKSequenceCuts(ksequence):
    """
    args:
    ksequence = The kitsu sequence dict that you want to grab the shots from
    returns a LIST of shot dicts for each shot in a sequence
    """
    cuts = gazu.shot.all_shots_for_sequence(ksequence)

    return cuts


#### SETTING DATA ######

def set_all_shot_data(project_name, fps=24,frame_in="1001"):
    """
    adds information to the "data" dict in the the shot info dict for every seqence in the project.
    currently only set up for fps and frame_in keys.
    The login function uses two env var keys,
    KPWORD and KUSER these need to be set for the function to work
    
    Requires gazu
    
    """
    
    kLogin()
    project = getKProject(project_name)
    all_seq = getKProjectSequences(project)
    
    for key,value in all_seq.items():
        seq = all_seq[key]
        shots = kpc.getKSequenceCuts(seq)
        for shot in shots:
            print("updating {0}/{1}".format(seq["name"], shot["name"]))
            gazu.shot.update_shot_data(shot,data={"fps":fps, "frame_in":frame_in})    


##### TEMP SPACE TO RUN OPERATIONS ######

# if __name__ == "__main__":
#     kLogin()