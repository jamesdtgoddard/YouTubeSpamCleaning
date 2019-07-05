import csv
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
import pickle

# Path to project folder and list of features to be used. If FEATURES_LIST is changed
# then the model will have to be retrained with the same features
FILE_PATH = "/Users/relativeinsight/Desktop/Youtube Spam Cleaning/"
FEATURES_LIST = ['LENGTH', 'SYMBOLS', 'CAPITALS', 'DIGITS', 'URLS', 'WORDS']

# Load in comments to be searched
df = pd.read_csv(FILE_PATH+"Comments.csv")

# Load in trained model
model = pickle.load(open('Training/model.sav', 'rb'))

# Analyses all comments and creates a list of the features from each comment
def extractFeatures(features_list):

	# Finds the length of each comment
	if('LENGTH' in features_list):
		df['LENGTH'] = df['CONTENT'].str.len()

	# Finds the frequency of upper case characters in each comment
	# unless length is unused
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

	# Finds the frequency of sybmols in each comment
	# unless length is unused
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
	# unless length is unused
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

	# Adds these five features to the features list
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

	# Finds the frequency of all the words listed in spam_words and 
	# adds them the the features list
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

	return features

# Runs extractFeatures and finds probabilites from model
features = extractFeatures(FEATURES_LIST)
probabilities = model.predict_proba(features)

# Selects comments whose probability is above the 60% threshold
predictions = []
for i in probabilities:
	if(i[0] > 0.6):
		predictions.append(0)
	else:
		predictions.append(1)

# Adds predictions to the csv file.
df['CLASS'] = predictions
df[['CONTENT', 'CLASS']].to_csv(FILE_PATH+"Comments.csv", index=False)

print(predictions)