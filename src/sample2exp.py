'''
Read "MiniSeq Submission Sheet.xlsx" to get the correlation between sampleID and sample
number referred later in the folder location
'''

import xlrd
from collections import OrderedDict
import simplejson as json

expResult = xlrd.open_workbook('../data/MiniSeq Submission Sheet.xlsx')

sh = expResult.sheet_by_index(0)

def excel2json_se(file):

    se_list = []

    for rownum in range(1, file.nrows):

        se = OrderedDict()
        row_value = file.row_values(rownum)

        se['samplenumber'] = str(row_value[0])
        se['sampleID'] = str(row_value[1])

        se_list.append(se)

    return se_list
temp = excel2json_se(sh)
samExJSON = json.dumps(temp)

# save the result in sam2exp.json file 
with open('../data/sam2exp.json', 'w') as filehandle:
    filehandle.write(samExJSON)
