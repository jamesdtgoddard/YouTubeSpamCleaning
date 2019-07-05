import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from random import random
import glob
import csv
import pickle

# Set file path to the project folder, the list of features to be trained and the 
# proportion of the data to be split for testing
FILE_PATH = "/Users/relativeinsight/Desktop/Youtube Spam Cleaning/Training/Data"
FEATURES_LIST = ['LENGTH', 'SYMBOLS', 'CAPITALS', 'DIGITS', 'URLS', 'WORDS']
PROPORTION_TESTING = 0.001

# Load all csv files into dataframe 'df'
def importData(file_path):

	global df

	all_files = glob.glob(file_path+"/*.csv")
	temporary_list = []

	for filename in all_files:
		temporary_df = pd.read_csv(filename)
		temporary_list.append(temporary_df)

	df = pd.concat(temporary_list, axis=0, ignore_index=True)

# Create a numpy array 'features' that contains all the extracted
# features listed in 'features_list'
def extractFeatures(features_list, reextract_features):

	if(reextract_features):

		# Finds the length of each comment
		if('LENGTH' in features_list):
			df['LENGTH'] = df['CONTENT'].str.len()

		# Finds the frequency of upper case characters in each comment
		# unless length is unavailable
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

		# Finds the frequency of symbols in each comment
		# unless length is unavailable
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

		# Finds the frequency of digits in each comment
		# unless length is unavailable
		if('DIGITS' in features_list):
			digits = []
			if('LENGTH' in features_list):
				for i in range(0, len(df['CONTENT'])):
					sum = 0
					for j in df['CONTENT'][i]:
						if(j.isdigit()):
							sum += 1
					digits.append(float(sum / df['LENGTH'][i]))
			else:
				for i in df['CONTENT']:
					sum = 0
					for j in i:
						if(j.isdigit()):
							sum += 1
					digits.append(sum)
			df['DIGITS'] = digits

		# Finds the number of URLs in each comment
		if('URLS' in features_list):
			urls = []
			for i in range(0, len(df['CONTENT'])):
				sum = 0
				for j in df['CONTENT'][i].split():
					if('https://' in j or 'www.' in j or 'http://' in j):
						sum += 1
				urls.append(sum)
			df['URLS'] = urls

		# Adds these five features to the list features
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
			if('DIGITS' in features_list):
				individual_features.append(df['DIGITS'][i])
			if('URLS' in features_list):
				individual_features.append(df['URLS'][i])
			features.append(individual_features)

		# Finds the frequency of each of the words listed in spam_words and
		# adds these to the features list
		if('WORDS' in features_list):
			spam_words = ['and','to','out','my','a','this','the','on','you','check','of','video','for','me','it','i','if','youtube','you','subscribe','like','can','in','please','just','is','channel','have','so','your','be','will','guys','music','at','money','from','up','but','as','make','get','would','do','all','with','our','new','are','am','that','who','comment','videos','really','us','or','know','u','not','song','people','could','more','playlist','help','see','called','I\'m','should','out','give','making','working','some','website','does']
			word_count = []
			for i in range(0, len(df['CONTENT'])):
			    word_count.append([])
			for i in range(0, len(df['CONTENT'])):
   				for j in spam_words:
   				    word_count[i].append((' '+df['CONTENT'][i]+' ').count(' ' + j + ' '))
			for i in range(0, len(word_count)):
				features[i] = features[i] + word_count[i]

		# Saves extracted feature to the features_list file so that processing
		# doesn't have to be unnecessarily repeated when testing
		with open('features_list.csv', mode='w') as features_file:
			csv_writer = csv.writer(features_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for i in features:	
				csv_writer.writerow(i)

		features = np.array(features)

	else:

		# Loads features from the features_list file
		features = []
		with open('features_list.csv', mode='r') as features_file:
			csv_reader = csv.reader(features_file, delimiter=',')
			line_count = 0
			for row in csv_reader:
				features.append(list(row))

		features = np.array(features)


	return features

# Create labels list and split data for training and testing
def splitData(proportion_testing, features):

	labels = np.array(df['CLASS'])

	train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = proportion_testing)

	return train_features, test_features, train_labels, test_labels


# Train model and create predictions on test data
def runModel(train_features, test_features, train_labels, test_labels):

	# Loads and fits model
	model = RandomForestClassifier(n_estimators = 100)
	model.fit(train_features, train_labels);
	predictions_float = model.predict(test_features)

	# Chooses spam comments above probability threshold
	predictions = []
	for i in predictions_float:
		if(i > 0.5):
			predictions.append(1)
		else:
			predictions.append(0)

	actual_values = test_labels

	# Calculates the proportion of comments labelled correctly
	predictions_correct = 0
	predictions_wrong = 0
	for i in range(0, len(actual_values)):
		if(predictions[i] == actual_values[i]):
			predictions_correct += 1
		else:
			predictions_wrong += 1
	predictions_ratio = float(predictions_correct / (predictions_correct + predictions_wrong))

	return predictions, actual_values, predictions_ratio, model

# Guess 1 or 0 to get an idea of the proportion we would expect to get right randomly
def runRandom(actual_values):

	random_guesses = []
	random_number = 0
	random_correct = 0
	random_wrong = 0

	# Creates a baseline proportion of comments labelled correctly by randomly
	# assigning a 1 or 0 to each comment
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

	return random_ratio

# Check difference in proportion predicted right and proportion guessed randomly
def checkImprovement(predictions_ratio, random_ratio):

	improvement = (predictions_ratio - random_ratio) * 100

	return improvement

# Runs all functions for tests and returns the improvement
def main(file_path, features_list, proportion_testing, reextract_features):
	importData(file_path)
	features = extractFeatures(features_list, reextract_features)
	train_features, test_features, train_labels, test_labels = splitData(proportion_testing, features)
	predictions, actual_values, predictions_ratio, model = runModel(train_features, test_features, train_labels, test_labels)
	random_ratio = runRandom(actual_values)
	return checkImprovement(predictions_ratio, random_ratio)

# Runs all the functions and saves the model for use in main.py
def train(file_path, features_list, proportion_testing, reextract_features):
	importData(file_path)
	features = extractFeatures(features_list, reextract_features)
	train_features, test_features, train_labels, test_labels = splitData(proportion_testing, features)
	predictions, actual_values, predictions_ratio, model = runModel(train_features, test_features, train_labels, test_labels)
	pickle.dump(model, open('model.sav', 'wb'))

# Runs the train function
# Leave commented unless refitting the model
# train(FILE_PATH, FEATURES_LIST, PROPORTION_TESTING, True)