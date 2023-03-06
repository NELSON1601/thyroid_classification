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
			self.outlier_threshold = 2.5

		except Exception as e:
			raise ThyroidException(e, sys)

	def drop_unwanted_columns(self, thyroid_data):
		try:
			unwanted_column_name = ['_id', 'ID', 'TSH_measured','T3_measured','TT4_measured','T4U_measured','FTI_measured','TBG_measured','referral_source']
			thyroid_data.drop(columns=unwanted_column_name, inplace=True)
			return thyroid_data

		except Exception as e:
			raise ThyroidException(e, sys)
		

	def clean_target_features(self, thyroid_data):
		try:
		
			thyroid_data.replace(['hyperthyroid', 'T3_toxic', 'goitre', 'secondary_toxic'], 'hyperthyroid', inplace=True)
			thyroid_data.replace(['hypothyroid', 'compensated_hypothyroid', 'primary_hypothyroid', 'secondary_hypothyroid'], 'hypothyroid', inplace=True)
			return thyroid_data

		except Exception as e:
			raise ThyroidException(e, sys)


	def fill_not_measured_values(self, thyroid_data, columns):
		try:
			thyroid_data.replace(['?'], np.nan, inplace=True)
			thyroid_data[columns].fillna(0, inplace=True)
			return thyroid_data

		except Exception as e:
			raise ThyroidException(e, sys)


	def change_column_dtypes(self, thyroid_data, columns, dtype):
		try:
			for column in columns:
				thyroid_data[column] = thyroid_data[column].astype(dtype)

			return thyroid_data

		except Exception as e:
			raise ThyroidException(e, sys)


	def remove_outliers(self, thyroid_data, columns, threshold):
		try:

			for column in columns:

				high_val = thyroid_data[column].mean() + (threshold * thyroid_data[column].std())
				low_val = thyroid_data[column].mean() - (threshold * thyroid_data[column].std())

				thyroid_data = thyroid_data[(thyroid_data[column] >= low_val) & (thyroid_data[column] <= high_val)]
				return thyroid_data

		except Exception as e:
			raise ThyroidException(e, sys)


	def initiate_data_cleaning(self):

		try:
			
			thyroid_data = pd.read_csv(f'{self.raw_data_path}/thyroid_data.csv')

			thyroid_data = self.drop_unwanted_columns(thyroid_data)

			thyroid_data = self.clean_target_features(thyroid_data)

			columns = ['TSH', 'T3', 'TT4', 'T4U', 'FTI', 'TBG']
			thyroid_data = self.fill_not_measured_values(thyroid_data, columns=columns)

			columns = ['age', 'TSH', 'T3', 'TT4', 'T4U', 'FTI', 'TBG']
			thyroid_data = self.change_column_dtypes(thyroid_data, columns=columns, dtype=float)
			print(thyroid_data.dtypes)
			print(thyroid_data.shape)
			thyroid_data = self.remove_outliers(thyroid_data, columns=columns, threshold=self.outlier_threshold)
			print(thyroid_data.shape)

			clean_data_dir = os.path.join(os.getcwd(), 'Data/clean_data')
			os.makedirs(clean_data_dir, exist_ok=True)

			thyroid_data.reset_index(drop=False, inplace=False)

			thyroid_data.to_csv(f'{clean_data_dir}/thyroid_data.csv', index=False, header=True)

			return clean_data_dir

		except Exception as e:
			raise ThyroidException(e, sys)




