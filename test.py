from pipeline_utilities import path_manipulation
import scandir
import os

x = "C:\\Users\\roger\\Documents\\maya\\projects\\default\\scenes"
y = "ASSETS"

test = path_manipulation.goFindDirectory(x,y)
print test


# mytest = scandir.scandir("Y://")

# for i in mytest:
#     print i
