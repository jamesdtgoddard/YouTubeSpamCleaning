# Youtube Spam Cleaning

This is a python script that tries to recognise whether or not a YouTube comment is spam or not. It uses a random forest classifier from sci-kit learn and is trained from this [dataset](https://archive.ics.uci.edu/ml/machine-learning-databases/00380/).

The model currently uses the length of each comment, the number of capital letters in each comment, the number of symbols in each comment, the number of digits in each comment and the frequency of certain popular words in each comment. The model is most effective when all features are used simultaneously and it can currently recognise spam with around 80% accuracy. The bar charts below compare the effectiveness of different combinations of these features:

![LCS](https://raw.githubusercontent.com/jamesdtgoddard/YoutubeSpamCleaning/master/Tests/LCS.png)

![LCSD](https://raw.githubusercontent.com/jamesdtgoddard/YoutubeSpamCleaning/master/Tests/LCSD.png)

![LCSDW](https://raw.githubusercontent.com/jamesdtgoddard/YoutubeSpamCleaning/master/Tests/LCSDW.png)

*Effectiveness is measured by running the model 100+ times on each set of features being compared. The percentage given is the average difference between the percentage of comments the model labels correctly and the percentage of comments labelled correctly by a random number generator. Note that the random number generator usually labels around 50% of the comments correctly.*