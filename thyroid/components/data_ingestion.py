import os
import sys
import pandas as pd
from thyroid.logger import logging
from thyroid.exception import ThyroidException


class DataIngestion:
	def __init__(self, mongo_client, database_name, collection_name1, collection_name2):
		try:
			self.mongo_client = mongo_client
			self.database_name = database_name
			self.collection_name1 = collection_name1
			self.collection_name2 = collection_name2
		except Exception as e:
			raise ThyroidException(e, sys)

	def initiate_data_ingestion(self):
		try:
			logging.info(f'exporting hyperthyroid data as dataframe from mongodb database')
			hyperthyroid_data = pd.DataFrame(list(self.mongo_client[self.database_name][self.collection_name1].find()))
			
			logging.info(f'exporting hypothyroid data as dataframe from mongodb database')
			hypothyroid_data = pd.DataFrame(list(self.mongo_client[self.database_name][self.collection_name2].find()))


			logging.info(f'creating a data directory')
			raw_data_dir = os.path.join(os.getcwd(), 'Data/raw_data')
			os.makedirs(raw_data_dir, exist_ok=True)

			thyroid_data = pd.concat([hypothyroid_data, hypothyroid_data], ignore_index=True)
			thyroid_data.reset_index(drop=False, inplace=False)

			logging.info(f'saving thyroid dataset in raw_data directory')
			thyroid_data.to_csv(path_or_buf=f'{raw_data_dir}/thyroid_data.csv', index=False, header=True)

			return raw_data_dir

		except Exception as e:
			raise ThyroidException(e, sys)