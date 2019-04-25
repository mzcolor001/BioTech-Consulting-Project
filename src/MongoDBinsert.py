'''
This file is to store data into the Mongodb database
and build the referencings among different schema.
'''

import MongoClient

from pymongo import MongoClient
import json
from pprint import pprint


# get a MongoClient object, connect to Mongodb
connectionObject = MongoClient('mongodb://localhost:27017/')

# access the database using object.attribute notation

databaseObject = connectionObject.data

# access the mongodb collection
collectionObject_human = databaseObject.human

collectionObject_sample = databaseObject.sample

collectionObject_sampleFinal = databaseObject.sampleFinal

collectionObject_samExp = databaseObject.samExp

collectionObject_expRun = databaseObject.expRun

collectionObject_fqgzLoc = databaseObject.fqgzLoc

collectionObject_analysis = databaseObject.analysis

collectionObject_expRun.insert_one({"Provider": "UCSD", "Date Submitted": "1/25/19",
									"Date Completed": "1/26/19", "Type": "DNA"})

# read human.json file and load the info. to human collection
with open('../data/human.json') as data_human:
	data_h = json.load(data_human)

	# print("debugging1 : ", len(data_h))

	for item_h in data_h:
		collectionObject_human.insert_one(item_h).inserted_id
# read sampleJSON.json file and load the info. to sample collection
with open('../data/sampleConv.json') as data_sample:
	data_s = json.load(data_sample)
	# print("debugging2 : ", data_s)

	for item_d in data_s:
		collectionObject_sample.insert_one(item_d).inserted_id

# map the human and sample collections through PatientID and Patient_trial
sampleFinal = []

for document_h in collectionObject_human.find():

	for document_s in collectionObject_sample.find():
# if the the first five strings match in PatientID and Patient_trial
		if document_h['PatientID'][0:5] == document_s['Patient_trial'][0:5]:
# then store the _id of human collection in the humanID field of sampleFinal collection
			document_s['humanID'] = document_h['_id']

			sampleFinal.append(document_s)
# # print(sampleFinal)
# store item_sF into sampleFinal collection
for item_sF in sampleFinal:
	collectionObject_sampleFinal.insert_one(item_sF).inserted_id

with open('../data/sam2exp.json') as data_samExp:
	data_se = json.load(data_samExp)

# store item_se into samExp collection
	for item_se in data_se:
		collectionObject_samExp.insert_one(item_se).inserted_id

with open('../data/listfile.json') as fqgzLoc:
	data_loc = json.load(fqgzLoc)

# store item_loc into fqgzLoc collection
	for item_loc in data_loc:
		collectionObject_fqgzLoc.insert_one(item_loc).inserted_id

with open('../data/analysis.json') as analysis:
	data_analy = json.load(analysis)

# store item_analy into analysis collection 
	for item_analy in data_analy:
		collectionObject_analysis.insert_one(item_analy).inserted_id

# connect human and sampleFinal collections
pipeline = [{'$lookup':
            {'from': "sampleFinal",       # samleFinal table name
            'localField': "_id",   # name of human table field
            'foreignField': "humanID", # name of sampleFinal table field
            'as': "sample_connection"         # alias for human table
        }},
    {'$unwind': "$sample_connection"}]

doc_list = []
for doc in (collectionObject_human.aggregate(pipeline)):
    # pprint(doc)
	doc_list.append(doc)

# connect sampleFinal and sampleExp collections
pipeline_1 = [{'$lookup':
            {'from': "samExp",       #  samExp table name
            'localField': "Patient_trial",   # name of sampleFinal table field
            'foreignField': "sampleID", # name of samExp table field
            'as': "sampleExp_connection"         # alias for sampleFinal table
        }},
    {'$unwind': "$sampleExp_connection"}]

doc_1_list = []
for doc_1 in (collectionObject_sampleFinal.aggregate(pipeline_1)):
    # pprint(doc_1)
	doc_1_list.append(doc_1)


# connect samExp and fqgzLoc collections
pipeline_2 = [{'$lookup':
            {'from': "fqgzLoc",       #  fqgzLoc table name
            'localField': "samplenumber",   # name of samExp field
            'foreignField': "fileAbbre", # name of fqgzLoc table field
            'as': "samplefile_connection"         # alias for samExp table
        }},
    {'$unwind': "$samplefile_connection"}]

doc_2_list = []
for doc_2 in (collectionObject_samExp.aggregate(pipeline_2)):
    # pprint(doc_2)
	doc_2_list.append(doc_2)

# connect samExp and analysis collections
pipeline_3 = [{'$lookup':
            {'from': "analysis",       #  analysis table name
            'localField': "fileAbbre",   # name of samExp table field
            'foreignField': "key", # name of analysis table field
            'as': "fqanalysis_connection"         # alias for samExp table
        }},
    {'$unwind': "$fqanalysis_connection"}]

doc_3_list = []
for doc_3 in (collectionObject_fqgzLoc.aggregate(pipeline_3)):
    # pprint(doc_3)
	doc_3_list.append(doc_3)


# type the PatientID "95797" in the info
# querydata(doc_list, doc_1_list, doc_2_list, doc_3_list, "95797")
