import gazu
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Google sheets info

def getGSheetdata(sheetname,rstart,rend,colstart,colend):

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

    scenedict = {}

    for i in range(rstart,rend+1):

        tempdict = {}
        row = str(i)    
        datarange = colstart+row+":"+colend+row
        head = sheet.get(datarange,major_dimension="ROWS")
        tempdict[head[0][0]] = {"frame_in":head[0][1],"frame_out":head[0][2],"frames":head[0][3]}
        scenedict.update(tempdict)
        print("running row {} our of 64".format(i))
        
    return scenedict     


def setkData():

    # Kitsu login
    USERNAME = os.getenv("KUSER")
    PASSWORD = os.getenv("KPWORD")

    gazu.set_host("https://polycat.cg-wire.com/api")
    gazu.log_in(USERNAME, PASSWORD) 
    project = gazu.project.get_project_by_name("Eosis")
    scn = gazu.shot.get_sequence_by_name(project,"scn0010_wizardlodge_interior")


    #sets the frame ranges
    for key,value in scenedict.items():
        
        shot = gazu.shot.get_shot_by_name(scn,key)
        shot["data"].update(value)
        shot["nb_frames"] = value["frames"]
        gazu.shot.update_shot(shot)



if __name__ == "__main__":

    print("Connecting to google sheet api....")
    try:
        scenedict = getGSheetdata("scn0010",6,63,"b","e")
        print("Created scenedict")
        print("Connecting to the Kitsu api")
        setkData()
        print("finished setting kitsu data")

    except:
        print("There was an error ..exiting)
        break

