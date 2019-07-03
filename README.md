# Youtube Spam Cleaning

A python script that tries to recognise whether or not a youtube comment is spam. Trained from this [dataset](https://archive.ics.uci.edu/ml/machine-learning-databases/00380/) found online.

Currently the model uses the length, number of capital letters and number of symbols from each comment as features. These features are used to train a random forest classifier using scikit-learn.

The file test_effectiveness.py runs the model using all combinations of features and displays their effectiveness (the difference in percentage predicted correct to random) as a bar chart.

The first test using the features length, capitals and symbols is shown below:

![First Results](https://raw.githubusercontent.com/jamesdtgoddard/YoutubeSpamCleaning/master/First_Results_(100).png)

From this we can see that the model is significantly more effective when all three features are being used together.