'''
This file is to complete the human and sample schema.
Read the cleaned data for human which is two excel, "metadata_sanguine_Cancer-human.xlsx"
"metadata_sanguine_Controls-human.xlsx"

Read the cleaned data for sample which is two excel, "metadata_sanguine_Cancer.xlsx"
"metadata_sanguine_Controls.xlsx"

'''

import xlrd
from collections import OrderedDict
import simplejson as json


cancerHuman = xlrd.open_workbook('../data/metadata_sanguine_Cancer-human.xlsx')
controlHuman = xlrd.open_workbook('../data/metadata_sanguine_Controls-human.xlsx')

cancerSample = xlrd.open_workbook('../data/metadata_sanguine_Cancer.xlsx')
controlSample = xlrd.open_workbook('../data/metadata_sanguine_Controls.xlsx')

sh1 = cancerHuman.sheet_by_index(0)
sh2 = controlHuman.sheet_by_index(0)

sh3 = cancerSample.sheet_by_index(0)
sh4 = controlSample.sheet_by_index(0)

# expResult = xlrd.open_workbook("MiniSeq Submission Sheet.xlsx")

# sh5 = expResult.sheet_by_index(0)

# to generate human schema in JSON format
def excel2json_human(file1):
	human_list = []

	for rownum1 in range(1, file1.nrows):

		human = OrderedDict()
		row_values1 = file1.row_values(rownum1)

		human['PatientID'] = str(row_values1[0])
		human['Age']= str(row_values1[3])
		human['Height']= str(row_values1[6])
		human['Weight']= str(row_values1[7])
		human['Cancer Status']= 'Cancer'
		human['Cancer Type'] = str(row_values1[13])

		human_list.append(human)
	return human_list


j1_human = excel2json_human(sh1)
# print(len(j1_human))
j2_human = excel2json_human(sh2)
# print(len(j2_human))


for i in range(len(j2_human)):
	j1_human.append(j2_human[i])


humanJSON = json.dumps(j1_human)
print("records count in the human.json : ", len(j1_human))
# print(humanJSON)

with open('human.json', 'w') as f_human:
	f_human.write(humanJSON)

# to generate sample schema in JSON format
def excel2json_sample(file2):

	sample_list = []

	for rownum2 in range(1, file2.nrows):
		sample = OrderedDict()
		row_values2 = file2.row_values(rownum2)

		sample['Patient_trial'] = str(row_values2[0])
		sample['Type']= 'fecal'
		sample['Appointment Date']= str(row_values2[1])

		sample_list.append(sample)
	return sample_list

j1_sample = excel2json_sample(sh3)
# print(j1)
j2_sample = excel2json_sample(sh4)

for k in range(len(j2_sample)):
	j1_sample.append(j2_sample[k])

sampleJSON = json.dumps(j1_sample)
print("records count in the sample.json : ", len(j1_sample))
with open('sample.json', 'w') as f_sample:
	f_sample.write(sampleJSON)

# to generate the correlation between sampleID and sample number in JSON format
# def excel2json_expResult(file3):
# #
# 	expResult_list = []
# #
# 	for rownum3 in range(1, file3.nrows):
# 		expResult = OrderedDict()
# 		row_values3 = file3.row_values(rownum3)
# #
# 		expResult['SampleNum'] = str(row_values3[0])
# 		expResult['SampleID']= str(row_values3[1])
#
# #
# 		expResult_list.append(expResult)
# 	return expResult_list
# #
# experim_D = excel2json_expResult(sh5)
# #
# experimJSON = json.dumps(experim_D)
#
# # print("records counts in the expRun.json : ", len(experim_D))
# with open('expRun.json', 'w') as f_sample:
# 	f_sample.write(experimJSON)
