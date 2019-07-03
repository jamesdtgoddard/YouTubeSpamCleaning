# Youtube Spam Cleaning

A python script that tries to recognise whether or not a youtube comment is spam. Trained from this [dataset](https://archive.ics.uci.edu/ml/machine-learning-databases/00380/) found online.

Initially the model used the length, number of capital letters and number of symbols from each comment as features. These features are used to train a random forest classifier using scikit-learn. The following bar chart shows a comparison of the effectiveness of each combination of features:

![First Results](https://raw.githubusercontent.com/jamesdtgoddard/YoutubeSpamCleaning/master/First_Results_(100).png)

We see that the model is most effect when all three features are used together.

I have since added a fourth feature, the number of digits used in each comment. Using this feature very slightly improved the model's effectiveness as shown below:

![Digits Results](https://raw.githubusercontent.com/jamesdtgoddard/YoutubeSpamCleaning/master/LCSD.png)

