import os
import sys
import pickle
import pandas as pd
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from thyroid.logger import logging
from thyroid.exception import ThyroidException

class ModelTrainer:
	def __init__(self, resampled_data_path):
		try:
			self.resampled_data_path = resampled_data_path			

		except Exception as e:
			raise ThyroidException(e, sys)


	def random_forest(self, X, y):
		try:
			model = RandomForestClassifier()
			model.fit(X, y)
			return model
		except Exception as e:
			raise ThyroidException(e, sys)

	def decision_tree(self, X, y):
		try:
			model = DecisionTreeClassifier()
			model.fit(X, y)
			return model
		except Exception as e:
			raise ThyroidException(e, sys)


	def initiate_model_trainer(self):
		try:

			classification_models = {'random_forest': self.random_forest,
								 'decision_tree': self.decision_tree}

			logging.info(f'creating accuracy table to store the accuracy of machine learning models')
			accuracy_table = pd.DataFrame(columns=['accuracy'], 
										  index=classification_models.keys(), 
										  dtype=object)

			logging.info(f"Reading the data for training and testing the model")
			x_train = pd.read_csv(f'{self.resampled_data_path}/x_train.csv')
			y_train = pd.read_csv(f'{self.resampled_data_path}/y_train.csv')

			x_test = pd.read_csv(f'{self.resampled_data_path}/x_test.csv')
			y_test = pd.read_csv(f'{self.resampled_data_path}/y_test.csv')
			 

			for i, model in enumerate(classification_models.values()):

				logging.info(f'training model using {accuracy_table.index[i]}')
				thyroid_model = model(x_train, y_train)

				predictions = thyroid_model.predict(x_test)
				score = accuracy_score(predictions, y_test)
				score = round(score*100, 2)

				logging.info(f'accuracy using {accuracy_table.index[i]}: {score}')

				accuracy_table['accuracy'][i] = score

				model_dir = f'saved models/models'
				os.makedirs(model_dir, exist_ok=True)

				pickle.dump(thyroid_model, open(f'{model_dir}/{accuracy_table.index[i]}.pkl', 'wb'))

			accuracy_table.to_csv('model_accuracy.csv')

		except Exception as e:
			raise ThyroidException(e, sys)