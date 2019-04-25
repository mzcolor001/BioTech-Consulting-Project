'''
this file is to convert sample.json file
change the field "PatientID": "95797 (VISIT 2)" to "PatientID": "95797-2"
so that we could use this "95797-2" convention / SampleID to link to Sample number
'''
import json

with open('../data/sample.json') as file1:
    data_temp = json.load(file1)

    for item in data_temp:
        if len(item["Patient_trial"]) > 5:
            temp = item["Patient_trial"]
            item["Patient_trial"] = temp[0:5] + "-" + temp[13]

# print(len(data_temp))

with open('../data/sampleConv.json', 'w') as file2:
    json.dump(data_temp, file2)
