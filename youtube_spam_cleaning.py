import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from random import random
import glob
import csv

#Set default parameters
FILE_PATH = "/Users/relativeinsight/Desktop/Youtube Spam Cleaning/Data" #Path to folder containing csv data files
FEATURES_LIST = ['LENGTH', 'SYMBOLS', 'CAPITALS', 'DIGITS', 'WORDS'] #List of features to be used
PROPORTION_TESTING = 0.1 #Percentage of data to be split for testing

#Load all csv files into dataframe 'df'
def importData(file_path):

	global df

	all_files = glob.glob(file_path+"/*.csv")
	temporary_list = []

	for filename in all_files:
		temporary_df = pd.read_csv(filename)
		temporary_list.append(temporary_df)

	df = pd.concat(temporary_list, axis=0, ignore_index=True)

#Create a numpy array 'features' that contains all the extracted features listed in 'features_list'
def extractFeatures(features_list, reextract_features):

	if(reextract_features):

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
			features.append(individual_features)
		features = np.array(features)

		word_features = {}

		if('WORDS' in features_list):
			spam_words = ['and','to','out','my','a']#,'this','the','on','you','check','of','video','for','me','it','i','if','youtube','you','subscribe','like','can','in','please','just','is','channel','have','so','your','be','will','guys','music','at','money','from','up','but','as','make','get','would','do','all','with','our','new','are','am','that','who','comment','videos','really','us','or','know','u','not','song','people','could','more','playlist','help','see','called','I\'m','should','out','give','making','working','some','website','does']
			for i in spam_words:
				word_features[i] = 0
			for j in range(0, len(df['CONTENT'])):
				for k in df['CONTENT'][j].split():
					if(k.lower() in spam_words):
						word_features[i] +=1
				for i in word_features:
					features = features.tolist()
					features[j].append(word_features[i])
					features = np.array(features)
				for i in spam_words:
					word_features[i] = 0
				if(j/1955 % 0.1 == 0):
					print("~ "+str(j/1955 * 100)+"% of features extracted.")

		features = features.tolist()

		with open('features_list.csv', mode='w') as features_file:
			csv_writer = csv.writer(features_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for i in features:	
				csv_writer.writerow(i)

		features = np.array(features)

	else:

		features = []

		with open('features_list.csv', mode='r') as features_file:
			csv_reader = csv.reader(features_file, delimiter=',')
			line_count = 0
			for row in csv_reader:
				features.append(list(row))

		features = np.array(features)


	return features

#Create labels list and split data for training and testing
def splitData(proportion_testing, features):

	labels = np.array(df['CLASS'])

	train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = proportion_testing)

	return train_features, test_features, train_labels, test_labels


#Train model and create predictions on test data
def runModel(train_features, test_features, train_labels, test_labels):

	model = RandomForestClassifier(n_estimators = 100)
	model.fit(train_features, train_labels);
	predictions_float = model.predict(test_features)

	predictions = []
	for i in predictions_float:
		if(i > 0.5):
			predictions.append(1)
		else:
			predictions.append(0)

	actual_values = test_labels

	predictions_correct = 0
	predictions_wrong = 0
	for i in range(0, len(actual_values)):
		if(predictions[i] == actual_values[i]):
			predictions_correct += 1
		else:
			predictions_wrong += 1
	predictions_ratio = float(predictions_correct / (predictions_correct + predictions_wrong))

	return predictions, actual_values, predictions_ratio

#Guess 1 or 0 to get an idea of the proportion we would expect to get right randomly
def runRandom(actual_values):

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

	return random_ratio

#Check difference in proportion predicted right and proportion guessed right
def checkImprovement(predictions_ratio, random_ratio):

	improvement = (predictions_ratio - random_ratio) * 100

	return improvement

#Run all functions
def main(file_path, features_list, proportion_testing, reextract_features):
	importData(file_path)
	features = extractFeatures(features_list, reextract_features)
	train_features, test_features, train_labels, test_labels = splitData(proportion_testing, features)
	predictions, actual_values, predictions_ratio = runModel(train_features, test_features, train_labels, test_labels)
	random_ratio = runRandom(actual_values)
	return checkImprovement(predictions_ratio, random_ratio)
