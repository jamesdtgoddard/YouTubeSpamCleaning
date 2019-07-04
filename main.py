import csv
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
import pickle

FILE_PATH = "/Users/relativeinsight/Desktop/Youtube Spam Cleaning/" #Path to Youtube Spam Cleaning Folder
FEATURES_LIST = ['LENGTH', 'SYMBOLS', 'CAPITALS', 'DIGITS', 'WORDS'] #List of features to be used

df = pd.read_csv(FILE_PATH+"Comments.csv")

model = pickle.load(open('Training/model.sav', 'rb'))

def extractFeatures(features_list):

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
					word_features[k.lower()] +=1
			for i in word_features:
				features = features.tolist()
				features[j].append(word_features[i])
				features = np.array(features)
			for i in spam_words:
				word_features[i] = 0

	return features


features = extractFeatures(FEATURES_LIST)
predictions = model.predict(features)

print(predictions)