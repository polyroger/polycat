import os
import re

mysep = os.path.sep
links = []
answers = ["y","n"]
regex = r"^(.*?projects\\)"

while True:
    macdir = input("\nPaste the link here :")
    windir = macdir.replace("/","\\")
    try:
        myregex = str(re.search(regex,windir).group())
        regexwindir = windir.replace(myregex,"Y:\\")
        links.append(regexwindir)
    except:
        print("There was an error creating the new link, most likely projects was not in the name. Only changing the / to \\")
        links.append(windir)
    answer = str(input("do you want to convert another link? Y | N : ".lower()))
    
    while not answer in answers:
        answer = str(input("\nPlease enter iether Y or N : ".lower()))
    if answer == "n":
        break
print ("\n here is a list of your links:\n")
for i in links:
    print(i)
   
   
input("\nThank you..please come again")
