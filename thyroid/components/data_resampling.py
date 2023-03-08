import os 
import sys
import numpy as np
import pandas as pd
from thyroid.logger import logging
from thyroid.exception import ThyroidException
from imblearn.over_sampling import SMOTE
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
			over_sampling = SMOTE(random_state=0, k_neighbors=7)
			x, y = over_sampling.fit_resample(x, y)
			return x, y

		except Exception as e:
			raise ThyroidException(e, sys)


	def initiate_data_resampling(self):
		try:
			training_data = pd.read_csv(f"{self.transformed_data_path}/training_data.csv")
			testing_data = pd.read_csv(f"{self.transformed_data_path}/testing_data.csv")

			x_train, y_train = training_data.iloc[:,:-1], training_data.iloc[:, -1]
			x_test, y_test = testing_data.iloc[:, :-1], testing_data.iloc[:, -1] 

			x_train, y_train = self.over_sampling(x_train, y_train)
			x_test, y_test = self.over_sampling(x_test, y_test)

			# x_train, y_train = self.under_sampling(x_train, x_train)

			resampled_data_dir = os.path.join(os.getcwd(), 'Data/resampled_data')
			os.makedirs(resampled_data_dir, exist_ok=True)

			x_train.to_csv(f'{resampled_data_dir}/x_train.csv', index=False, header=True)
			y_train.to_csv(f'{resampled_data_dir}/y_train.csv', index=False, header=True)

			x_test.to_csv(f'{resampled_data_dir}/x_test.csv', index=False, header=True)
			y_test.to_csv(f'{resampled_data_dir}/y_test.csv', index=False, header=True)

			# print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

			return resampled_data_dir

		except Exception as e:
			raise ThyroidException(e, sys)
