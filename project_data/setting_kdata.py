import gazu
import os

# Kitsu login
USERNAME = os.getenv("KUSER")
PASSWORD = os.getenv("KPWORD")

gazu.set_host("https://polycat-visual-effects-pty-ltd.cg-wire.com/api")
gazu.log_in(USERNAME, PASSWORD) 

project = gazu.project.get_project_by_name("Eosis")
scn = gazu.shot.get_sequence_by_name(project,"scn0010")
cuts = gazu.shot.all_shots_for_sequence(scn)

# updating / setting the shot data dict with values
for cut in cuts:
    newdata = {"fps":"24"}

    if cut["data"]:
        cut["data"].update(newdata)
        gazu.shot.update_shot_data(cut,newdata)
    else:
        cut["data"] = newdata
        gazu.shot.update_shot_data(cut,cut["data"])


   