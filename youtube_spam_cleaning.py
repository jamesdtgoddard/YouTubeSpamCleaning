import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from random import random
import glob

#Set default parameters
FILE_PATH = "/Users/relativeinsight/Desktop/Youtube Spam Cleaning"
FEATURES_LIST = ['LENGTH', 'SYMBOLS', 'CAPITALS']
PROPORTION_TESTING = 0.25

#Load all csv files into dataframe 'df'
def importData(file_path):

	global df

	all_files = glob.glob(file_path+"/*.csv")
	temporary_list = []

	for filename in all_files:
		temporary_df = pd.read_csv(filename)
		temporary_list.append(temporary_df)

	df = pd.concat(temporary_list, axis=0, ignore_index=True)

#Create a list 'features' that contains all the extracted features listed in 'features_list'
def extractFeatures(features_list):

	global features

	if('LENGTH' in features_list):
		df['LENGTH'] = df['CONTENT'].str.len()

	if('CAPITALS' in features_list):
		capitals = []
		if('LENGTH' in features_list):
			for i in range(0, len(df['CONTENT'])):
				sum = 0
				for j in df['CONTENT'][i]:
					if(j.isupper()):
						sum += 1
				capitals.append(float(sum / df['LENGTH'][i]))
		else:
			for i in df['CONTENT']:
				sum = 0
				for j in i:
					if(j.isupper()):
						sum += 1
				capitals.append(sum)
		df['CAPITALS'] = capitals

	if('SYMBOLS' in features_list):
		symbols = []
		if('LENGTH' in features_list):
			for i in range(0, len(df['CONTENT'])):
				sum = 0
				for j in df['CONTENT'][i]:
					if(not j.isalpha() and not j.isdigit() and j != ' '):
						sum += 1
				symbols.append(float(sum / df['LENGTH'][i]))
		else:
			for i in df['CONTENT']:
				sum = 0
				for j in i:
					if(j.isupper()):
						sum += 1
				symbols.append(sum)
		df['SYMBOLS'] = symbols

	features = []
	individual_features = []
	for i in range(0, len(df['CONTENT'])):
		individual_features = []
		if('LENGTH' in features_list):
			individual_features.append(df['LENGTH'][i])
		if('CAPITALS' in features_list):
			individual_features.append(df['CAPITALS'][i])
		if('SYMBOLS' in features_list):
			individual_features.append(df['SYMBOLS'][i])
		features.append(individual_features)
	features = np.array(features)

#Create labels list and split data for training and testing
def splitData(proportion_testing):

	global train_features, test_features, train_labels, test_labels

	labels = np.array(df['CLASS'])

	train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = proportion_testing)


#Train model and create predictions on test data
def runModel():

	global predictions, actual_values, predictions_ratio

	model = RandomForestClassifier(n_estimators = 100)
	model.fit(train_features, train_labels);
	predictions_float = model.predict(test_features)

	predictions = []
	for i in predictions_float:
		if(i > 0.5):
			predictions.append(1)
		else:
			predictions.append(0)

	actual_values = []
	for i in test_labels:
		actual_values.append(i) #Maybe remove loop

	predictions_correct = 0
	predictions_wrong = 0
	for i in range(0, len(actual_values)):
		if(predictions[i] == actual_values[i]):
			predictions_correct += 1
		else:
			predictions_wrong += 1
	predictions_ratio = float(predictions_correct / (predictions_correct + predictions_wrong))


#Guess 1 or 0 to get an idea of the proportion we would expect to get right randomly
def runRandom():

	global random_guesses, random_ratio

	random_guesses = []
	random_number = 0
	random_correct = 0
	random_wrong = 0

	for i in range(0, len(actual_values)):
		random_number = random()
		if(random_number > 0.5):
			if(actual_values[i] == 1):
				random_correct += 1
			else:
				random_wrong += 1
		else:
			if(actual_values[i] == 0):
				random_correct += 1
			else:
				random_wrong += 1
	random_ratio = float(random_correct / (random_correct + random_wrong))

#Check difference in proportion predicted right and proportion guessed right
def checkImprovement():

	global improvement

	improvement = (predictions_ratio - random_ratio) * 100

#Run all functions
def main(file_path, features_list, proportion_testing):
	importData(file_path)
	extractFeatures(features_list)
	splitData(proportion_testing)
	runModel()
	runRandom()
	checkImprovement()
	return improvement
