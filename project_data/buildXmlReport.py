import xml.etree.ElementTree as ET

def buildReport():

    xmlfile = r"\\YARN\projects\mov\eos\0_aaa\0_internal\0_project_data\xml_reports\xmls\scn0010_wizards_lodge.xml"
    report = r"\\YARN\projects\mov\eos\0_aaa\0_internal\0_project_data\xml_reports\reports\scn0010_wizards_lodge_report.txt"

    tree = ET.parse(xmlfile)

    root = tree.find("sequence/media/")
    clipitems = root.getchildren()

    for item in clipitems:
        try:
            _ = (item.attrib["MZ.TrackName"])
            if _ == "Video 2":
                v2 = item
        except :
            print("no track attribute")


    with open(report,"w") as r:

        for i in v2:

            try:
            
                fin = int(i.findtext("in"))+1
                fout = int(i.findtext("out"))
                usedframes = fout - fin
                
                r.write(f"Name: cut{i.findtext('name')}\n")
                r.write(f"Frames in folder: {i.findtext('duration')}\n")
                r.write(f"Frames in timeline: {usedframes+1}\n")
                r.write(f"Frame Segment: {fin} : {fout}\n")
                r.write("\n")
            
            except :
                print("no data")

if __name__ == "__main__":
    buildReport()

    
    
    

