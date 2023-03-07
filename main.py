import pymongo
from thyroid.components.data_ingestion import DataIngestion
from thyroid.components.data_cleaning import DataCleaning
# from thyroid.components.model_training import ModelTrainer

database_name = "Thyroid_database"
collection_name1 = "hyperthyroid_data"
collection_name2 = "hypothyroid_data"
mongo_client = pymongo.MongoClient("mongodb+srv://Nelson_1601:<password>@cluster0.nxxmtd3.mongodb.net/?retryWrites=true&w=majority")


if __name__ == "__main__":

	data_ingestion = DataIngestion(mongo_client=mongo_client, database_name=database_name, collection_name1=collection_name1, collection_name2=collection_name2)
	raw_data_path = data_ingestion.initiate_data_ingestion()

	data_cleaning = DataCleaning(raw_data_path=raw_data_path)
	clean_data_path = data_cleaning.initiate_data_cleaning()
