import xml.etree.ElementTree as ET

def buildReport():

    xmlfile = r"sample_files\xmls\scn0010_wizards_lodge_v04.xml"
    report = r"\\YARN\projects\mov\eos\0_aaa\0_internal\0_project_data\xml_reports\reports\scn0010_wizards_lodge_report.txt"

    tree = ET.parse(xmlfile)

    clipitems = tree.findall("sequence/media/video/track/clipitem")

    for clip in clipitems:
        print(f"name : {clip.findtext('name')}\t\tstart : {clip.findtext('start')}\tend : {clip.findtext('end')}\tin :{clip.findtext('in')}\tout :{clip.findtext('out')} ")

        






buildReport()

#     with open(report,"w") as r:

#         for i in v2:

#             try:
            
#                 fin = int(i.findtext("in"))+1
#                 fout = int(i.findtext("out"))
#                 usedframes = fout - fin
                
#                 r.write(f"Name: cut{i.findtext('name')}\n")
#                 r.write(f"Frames in folder: {i.findtext('duration')}\n")
#                 r.write(f"Frames in timeline: {usedframes+1}\n")
#                 r.write(f"Frame Segment: {fin} : {fout}\n")
#                 r.write("\n")
            
#             except :
#                 print("no data")

# if __name__ == "__main__":
#     buildReport()

    
    
    

