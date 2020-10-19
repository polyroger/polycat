import gazu,os

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

