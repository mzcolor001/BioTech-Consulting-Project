'''this is made to read Experimental Result schema
1. the fq.gz file is in the /wgs11/trimmed folder
2. list the file names in this directory and read the file name in the format {"name": filename}
   and save the data in the listfile.json file
'''


from __future__ import print_function
import os
import json
import sys
import operator

# define the Experimental Result location
path = './wgs11/trimmed'
# list the file names
files = os.listdir(path)
# define nameList list and store the extracted .fg.gz file into this list
nameList = []
for name in files:
	if name.endswith(".fq.gz"):
		nameList.append(name)
# print("nameList", nameList)

temp = [{"fileAbbre": name1[:2], 'filename': name1} for name1 in nameList]
# print(temp)

# write the temp into listfile.json file
with open('listfile.json', 'w') as filehandle:
    json.dump(temp, filehandle)


path_tsv = './wgs11/analysis/centrifuge'
'''
find the location for .tsv files
'''
def getListFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

temp_1 = [{'key': item[28:30], 'path_file': item} for item in getListFiles(path_tsv)]
# print(temp_1)

with open('analysis.json', 'w') as filehandle_1:
    json.dump(temp_1, filehandle_1)
