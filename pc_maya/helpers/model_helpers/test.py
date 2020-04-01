import re

mystrings = ["test_geo","test11_geo19541","test1_geo","test_geo1"]

for i in mystrings:
    print(re.sub("\\d","",i))

print (mystrings)


