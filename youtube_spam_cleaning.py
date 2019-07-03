import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from random import random
import glob

#Import all datasets into df variable
all_files = glob.glob("/Users/relativeinsight/Desktop/Youtube Spam Cleaning"+"/*.csv")
li = []
for filename in all_files:
	dftemp = pd.read_csv(filename)
	li.append(dftemp)
df = pd.concat(li, axis=0, ignore_index=True)

#Column for the string length of each comment
df['LENGTH'] = df['CONTENT'].str.len()

#Column for the number of capital letters in each comment
capitals = []
for i in df['CONTENT']:
    sum = 0
    for j in str(i):
        if(j.isupper()):
            sum += 1
    capitals.append(sum)
df['CAPITALS'] = capitals

#Column for the number of symbols (characters other than letters, numbers or spaces) in each comment
symbols = []
for i in df['CONTENT']:
	sum = 0
	for j in i:
		if(not j.isalpha() and not j.isdigit() and j != ' '):
			sum += 1
	symbols.append(sum)
df['SYMBOLS'] = symbols

#Create list called features that only contains the columns that are to be used as feautures in the model
features = []
iteration = 0
for i in df['CONTENT']:
	features.append([df['LENGTH'][iteration], df['CAPITALS'][iteration], df['SYMBOLS'][iteration]])
	iteration += 1
features = np.array(features)

#Create numpy array labels holding the true class of all comments
labels = np.array(df['CLASS'])

#Split dataset 75/25, train random forest model and make predictions on test data
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)
model = RandomForestClassifier(n_estimators = 1000)
model.fit(train_features, train_labels);
predictions_float = model.predict(test_features)

#Create list storing the absolute predictions made by the model
predictions = []
for i in predictions_float:
	if(i > 0.5):
		predictions.append(1)
	else:
		predictions.append(0)

#Create list storing the actual class values of all the comments
actual_values = []
for i in test_labels:
	actual_values.append(i)

#Randomly guess the class and compare with predictions to see how good the model is
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

#Calculate ratio actually predicted correctly by model
predictions_correct = 0
predictions_wrong = 0
for i in range(0, len(actual_values)):
	if(predictions[i] == actual_values[i]):
		predictions_correct += 1
	else:
		predictions_wrong += 1
predictions_ratio = float(predictions_correct / (predictions_correct + predictions_wrong))

#Calculate difference in percentage of classes predicted correctly and those guessed randomly
improvement = (predictions_ratio - random_ratio) * 100
print("Model improvement: "+str(improvement),"("+str(predictions_ratio*100)+", "+str(random_ratio*100)+")")

