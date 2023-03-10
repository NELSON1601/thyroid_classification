import os
import sys
import pandas as pd
from thyroid.logger import logging
from thyroid.exception import ThyroidException


class DataIngestion:
	def __init__(self, mongo_client, database_name, collection_name):
		try:
			self.mongo_client = mongo_client
			self.database_name = database_name
			self.collection_name = collection_name

		except Exception as e:
			raise ThyroidException(e, sys)

	def initiate_data_ingestion(self):
		try:
			logging.info(f'exporting hyperthyroid data as dataframe from mongodb database')
			thyroid_data = pd.DataFrame(list(self.mongo_client[self.database_name][self.collection_name].find()))

			logging.info(f'creating a data directory')
			raw_data_dir = os.path.join(os.getcwd(), 'Data/raw_data')
			os.makedirs(raw_data_dir, exist_ok=True)

			thyroid_data.drop(295, inplace=True)

			thyroid_data.reset_index(drop=False, inplace=False)

			logging.info(f'saving thyroid dataset in raw data directory')
			thyroid_data.to_csv(path_or_buf=f'{raw_data_dir}/thyroid_data.csv', index=False, header=True)

			return raw_data_dir

		except Exception as e:
			raise ThyroidException(e, sys)