import pandas as pd
import os
import pymongo
import json
client = pymongo.MongoClient("mongodb+srv://Nelson_1601:nelson1601@cluster0.nxxmtd3.mongodb.net/?retryWrites=true&w=majority")



if __name__== "__main__":

    

	DATA_FILE_PATH = (r"C:\ineuron_intership\thyroid_classification\raw_data\hypo_data.csv")
	DATABASE_NAME = "Thyroid_database"
	COLLECTION_NAME = "hypothyroid_data"

	df = pd.read_csv(DATA_FILE_PATH)
	print(f'rows and columns: {df.shape}')

	json_record = list(json.loads(df.T.to_json()).values())
	print(json_record[0])

	client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)
	