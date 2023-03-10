import os 
import sys
import numpy as np
import pandas as pd
from thyroid.logger import logging
from thyroid.exception import ThyroidException
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler



class DataResampling:
	def __init__(self, transformed_data_path):
		try:
			self.transformed_data_path = transformed_data_path

		except Exception as e:
			raise ThyroidException(e, sys)



	def under_sampling(self, x, y):
		try:
			under_sampling = RandomUnderSampler()
			x, y = under_sampling().fit_resample(x, y)
			return x, y

		except Exception as e:
			raise ThyroidException(e, sys)


	def over_sampling(self, x, y):
		try:
			over_sampling = RandomOverSampler()
			x, y = over_sampling.fit_resample(x, y)
			return x, y

		except Exception as e:
			raise ThyroidException(e, sys)


	def initiate_data_resampling(self):
		try:
			logging.info(f"Reading the data for resampling...")
			training_data = pd.read_csv(f"{self.transformed_data_path}/training_data.csv")
			testing_data = pd.read_csv(f"{self.transformed_data_path}/testing_data.csv")

			logging.info(f"Splitting the data into dependant variable and independent variable")
			x_train, y_train = training_data.iloc[:,:-1], training_data.iloc[:, -1]
			x_test, y_test = testing_data.iloc[:, :-1], testing_data.iloc[:, -1] 

			logging.info(f"Oversampling using RandomOverSampler")
			x_train, y_train = self.over_sampling(x_train, y_train)
			# x_test, y_test = self.over_sampling(x_test, y_test)

			logging.info(f"Creating a resampled data directory")
			resampled_data_dir = os.path.join(os.getcwd(), 'Data/resampled_data')
			os.makedirs(resampled_data_dir, exist_ok=True)

			logging.info(f"Saving the data into resampled data directory")
			x_train.to_csv(f'{resampled_data_dir}/x_train.csv', index=False, header=True)
			y_train.to_csv(f'{resampled_data_dir}/y_train.csv', index=False, header=True)

			x_test.to_csv(f'{resampled_data_dir}/x_test.csv', index=False, header=True)
			y_test.to_csv(f'{resampled_data_dir}/y_test.csv', index=False, header=True)

			return resampled_data_dir

		except Exception as e:
			raise ThyroidException(e, sys)
