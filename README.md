# YoutubeSpamCleaning

A python script that tries to recognise whether or not a youtube comment is spam. Trained from this [dataset](https://archive.ics.uci.edu/ml/machine-learning-databases/00380/) found online.

Currently the model uses the length, number of capital letters and number of symbols from each comment as features. These features are used to train a random forest classifier using scikit-learn.
