import os
import re

def walk_error_handler(exception_instance):
    print ("no files found....creating version 001")
    latest_plus = int(1)
    return latest_plus

def getVersion(camerapath):

    for root,dirs,files in os.walk(camerapath):
        for folder in dirs:
            mypath = os.path.join(camerapath,folder).replace("\\","/")
            # print(mypath)
           
            
            for root,dirs,files in os.walk(mypath):
                files.sort()
                # print (files)
                temp = files
                if temp:
                    for file in files:
                        noext = os.path.splitext(file)[0]
                        # this regex looks for numbers matching 0-9 only at the end of a filenam. The extension is stripped to make it easier.
                        latest = re.search("\d[0-9]$",noext).group()
                        latest_plus = int(latest) + int(1)
                else:
                    print("there were no files in the folder...creating version 001")
                    latest_plus = int(1)
                
                print(folder)
                print(latest_plus)
                    
                        


        

getVersion("C:/Users/roger/Documents/local_dev/testing")

# need to find the file with the highest version
# add in a better regex to get any numbered version, currently its only getting two platces , 1 - 99 addin int two /d seemed to do it but i think that its incorrect