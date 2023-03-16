import os
import sys
import pandas as pd
from thyroid.logger import logging
from thyroid.exception import ThyroidException
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler


class DataTransformation:
	def __init__(self, clean_data_path):
		try:
			self.clean_data_path = clean_data_path
			self.target = 'Target'

		except Exception as e:
			raise ThyroidException(e, sys)


	def split_train_test_data(self, thyroid_data):
		try:
			train_data, test_data = train_test_split(thyroid_data, test_size=0.3, random_state=1)
			return train_data, test_data

		except Exception as e:
			raise ThyroidException(e, sys)


	def categorical_encoding(self, training_data, testing_data):
		try:
			encoder = LabelEncoder()
			training_data = encoder.fit_transform(training_data)
			testing_data = encoder.fit_transform(testing_data)

			return training_data, testing_data

		except Exception as e:
			raise ThyroidException(e, sys)

	def feature_scaling(self, training_data, testing_data):
		try:
			scaler = StandardScaler()
			scaler.fit(training_data)

			training_data = scaler.transform(training_data)
			testing_data = scaler.transform(testing_data)

			return training_data, testing_data

		except Exception as e:
			raise ThyroidException(e, sys)


	def initiate_data_transformation(self):
		try:
			logging.info(f"Reading the data for transformation...")
			thyroid_data = pd.read_csv(f'{self.clean_data_path}/thyroid_data.csv')

			logging.info(f"Spliting the data into training and testing")
			training_data, testing_data = self.split_train_test_data(thyroid_data)

			logging.info(f"Encoding the categorical features using LabelEncoder")
			for column in training_data.columns:
				if training_data[column].dtypes == 'O':
					training_data[column], testing_data[column] = self.categorical_encoding(training_data[column], testing_data[column])

			# logging.info(f"Scaling the data using StandardScaler")
			# columns = [i for i in training_data.columns if i != self.target]
			# training_data[columns], testing_data[columns] = self.feature_scaling(training_data[columns], testing_data[columns])

			logging.info(f"Creating a transformed data directory")
			transformed_data_dir = os.path.join(os.getcwd(), 'Data/transformed_data')
			os.makedirs(transformed_data_dir, exist_ok=True)

			logging.info(f"Changing the numpy array into dataframe")
			training_data, testing_data = pd.DataFrame(training_data), pd.DataFrame(testing_data)

			logging.info(f"Saving the data into transformed data directory")
			training_data.to_csv(f'{transformed_data_dir}/training_data.csv', index=False, header=True)
			testing_data.to_csv(f'{transformed_data_dir}/testing_data.csv', index=False, header=True)

			return transformed_data_dir

		except Exception as e:
			raise ThyroidException(e, sys)
