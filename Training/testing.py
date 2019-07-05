import training
import matplotlib.pyplot as plt
import numpy as np

# Define the number of repeats, the path to the data folder, the proportion to
# be used for testing and the list of lists of features to compared
NUMBER_OF_REPEATS = 100
FILE_PATH = "/Users/relativeinsight/Desktop/Youtube Spam Cleaning/Training/Data"
PROPORTION_TESTING = 0.1
ALL_FEATURES = [['LENGTH', 'SYMBOLS', 'CAPITALS', 'DIGITS', 'WORDS', 'URLS']]

results = []
individual_results = []
full_length =len(ALL_FEATURES) * NUMBER_OF_REPEATS
amount_done = 0
last_printed = 0

# Runs the main function in training.py for all repeats and combinations of features
for i in ALL_FEATURES:
	REEXTRACT_FEATURES = True
	for j in range(0, NUMBER_OF_REPEATS):
		individual_results.append(training.main(FILE_PATH, i, PROPORTION_TESTING, REEXTRACT_FEATURES))
		REEXTRACT_FEATURES = False
		amount_done += 1
		if(int((amount_done / full_length) * 100) != last_printed):
			print(str(int((amount_done / full_length) * 100))+"% of repeats done.")
			last_printed = int((amount_done / full_length) * 100)
	results.append(individual_results)
	individual_results = []

# Calulates the average effectiveness
average_results = []
for i in results:
	sum = 0
	for j in i:
		sum += j
	average_results.append(sum/NUMBER_OF_REPEATS)

# Plots the data to a bar chart
plt.rcdefaults()
fig, ax = plt.subplots()

features = ('Features')
y_pos = np.arange(len(features))

ax.barh(y_pos, average_results, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(features)
ax.invert_yaxis()
ax.set_xlabel('Percentage above baseline')
ax.set_ylabel('Features')
ax.set_title('Comparing combinations of features')

plt.show()