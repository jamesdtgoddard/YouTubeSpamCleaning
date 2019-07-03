import Youtube_Spam_Cleaning
import matplotlib.pyplot as plt
import numpy as np

NUMBER_OF_REPEATS = 100
FILE_PATH = "/Users/relativeinsight/Desktop/Youtube Spam Cleaning/Data"
PROPORTION_TESTING = 0.1
ALL_FEATURES = [['LENGTH', 'CAPITALS', 'SYMBOLS'], ['LENGTH', 'SYMBOLS'], ['LENGTH', 'CAPITALS'], ['CAPITALS', 'SYMBOLS'], ['LENGTH'], ['CAPITALS'], ['SYMBOLS']]

results = []
individual_results = []
for i in ALL_FEATURES:
	for j in range(0, NUMBER_OF_REPEATS):
		individual_results.append(Youtube_Spam_Cleaning.main(FILE_PATH, i, PROPORTION_TESTING))
	results.append(individual_results)
	individual_results = []

average_results = []
for i in results:
	sum = 0
	for j in i:
		sum += j
	average_results.append(sum/NUMBER_OF_REPEATS)

plt.rcdefaults()
fig, ax = plt.subplots()

features = ('LCS', 'LS', 'LC', 'CS', 'L', 'C', 'S')
y_pos = np.arange(len(features))

ax.barh(y_pos, average_results, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(features)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Percentage above baseline')
ax.set_ylabel('Features')
ax.set_title('Comparing combinations of features.')

plt.show()