import gazu
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Google sheets info

def getGSheetdata(sheetname):

    """
    opens a google sheet and gets the data in the specifiec range and returns a dictionaty of data.
    The data is expected to be in a format where the name of the data appeats first in the row eg
    name , frame_in , frame_out, nb_frames. This way the dictionaty can be nicely defined.
    The default is to read rows.

    paramaters
    sheetname : (str) name of the google sheet
    rstart : (int) row to start at
    rend : (int) row to end at
    colstart: (str) col to start at
    colend: (str) col to end and at
    """
    
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("project_data\google_api_json\mov_eos_cred.json",scope)
    client = gspread.authorize(creds)
    sheet = client.open("Eosis 10 Production Sheet").worksheet(sheetname)

    sheetdict = sheet.get_all_records(head=5)
    tempdict = {}
    
    for i in sheetdict:
       tempdict[i["name"]] = {"shot-order":str(i["shot order"]).zfill(4),"frame_in":i["in"],"frame_out":i["out"],"frames":i["frames"],"description":i["description"]}

    return tempdict


def setkData(datadict):
    """
    There is often data duplication where the key does not form part of the data dictionary, in this case it will put the data in both.
    """

    # Kitsu login
    USERNAME = os.getenv("KUSER")
    PASSWORD = os.getenv("KPWORD")

    gazu.set_host("https://polycat.cg-wire.com/api")
    gazu.log_in(USERNAME, PASSWORD) 
    project = gazu.project.get_project_by_name("Eosis")
    scn = gazu.shot.get_sequence_by_name(project,"scn0010_wizardlodge_interior")

    #sets the frame ranges
    for key,value in datadict.items():
        
        shot = gazu.shot.get_shot_by_name(scn,key)
        shot["data"].update(value)
        shot["nb_frames"] = value["frames"]
        shot["description"]= value["description"]
        gazu.shot.update_shot(shot)


if __name__ == "__main__":

    print("Connecting to google sheet api....")
    try:
        scenedict = getGSheetdata("scn0010")
        print("Created scenedict")
        print("Connecting to the Kitsu api")
        setkData(scenedict)
        print("finished setting kitsu data")

    except Exception as error:
        print("There was a {} error, when running".format(error))

