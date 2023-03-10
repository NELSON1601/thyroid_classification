import os
import sys
import numpy as np
import pandas as pd
from thyroid.exception import ThyroidException
from thyroid.logger import logging


class DataCleaning:
	def __init__(self, raw_data_path):

		try:
			self.raw_data_path = raw_data_path
			self.outlier_threshold = 3

		except Exception as e:
			raise ThyroidException(e, sys)

	def drop_unwanted_columns(self, data):
		try:
			unwanted_column_name = ['_id', 'ID','TBG','TBG_measured','referral_source']
			data.drop(columns=unwanted_column_name, inplace=True)
			return data

		except Exception as e:
			raise ThyroidException(e, sys)
		

	def fill_not_measured_values(self, data, columns):
		try:
			for column in columns:
				data[column].fillna(0, inplace=True)
			return data

		except Exception as e:
			raise ThyroidException(e, sys)


	def change_column_dtypes(self, data, columns, dtype):
		try:
			for column in columns:
				data[column] = data[column].astype(dtype)
			return data

		except Exception as e:
			raise ThyroidException(e, sys)


	def remove_outliers(self, data, columns, threshold):
		try:
			for column in columns:
				high_val = data[column].mean() + (threshold * data[column].std())
				low_val = data[column].mean() - (threshold * data[column].std())

				data = data[(data[column] >= low_val) & (data[column] <= high_val)]
			return data

		except Exception as e:
			raise ThyroidException(e, sys)


	def fill_missing_values(self, data):
		try:
			for column in data.columns:
				if data[column].dtypes == 'O':
					data[column].fillna(data[column].mode()[0], inplace=True)
				else:
					data[column].fillna(data[column].mean(), inplace=True)
			return data

		except Exception as e:
			raise ThyroidException(e, sys)

	def initiate_data_cleaning(self):

		try:
			logging.info(f"Reading the data for cleaning...")
			thyroid_data = pd.read_csv(f'{self.raw_data_path}/thyroid_data.csv')

			logging.info(f"Replacing ? as NaN")
			thyroid_data.replace(['?'], np.nan, inplace=True)

			logging.info(f"Droping unwanted columns")
			thyroid_data = self.drop_unwanted_columns(data=thyroid_data)

			logging.info(f"Filling the note measured value with zero")
			columns = ['TSH', 'T3', 'TT4', 'T4U', 'FTI']
			thyroid_data = self.fill_not_measured_values(data=thyroid_data, columns=columns)

			logging.info(f"Changing the dtype of numerical columns")
			columns = ['age', 'TSH', 'T3', 'TT4', 'T4U', 'FTI']
			thyroid_data = self.change_column_dtypes(data=thyroid_data, columns=columns, dtype=float)

			logging.info(f"Removing the outliers which are over {self.outlier_threshold} std")			
			thyroid_data = self.remove_outliers(data=thyroid_data, columns=columns, threshold=self.outlier_threshold)

			logging.info(f"Filling the missing values using mean and mode")
			thyroid_data = self.fill_missing_values(data=thyroid_data)

			thyroid_data.reset_index(drop=False, inplace=False)

			logging.info(f"Creating a directory for clean data")
			clean_data_dir = os.path.join(os.getcwd(), 'Data/clean_data')
			os.makedirs(clean_data_dir, exist_ok=True)

			logging.info(f"Saving the data into clean data directory")
			thyroid_data.to_csv(f'{clean_data_dir}/thyroid_data.csv', index=False, header=True)
			
			return clean_data_dir

		except Exception as e:
			raise ThyroidException(e, sys)




