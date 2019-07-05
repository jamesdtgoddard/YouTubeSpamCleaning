# YouTube Spam Cleaning
A Python program to identify spam amongst YouTube comments. Currently identifies 90% of spam correctly.

*  Place all the comments you want checking in the 'Comments.csv' file under the title 'CONTENT'
* Change the 'FILE_PATH' variable in 'main.py' to the path to the folder containing 'main.py'
*  Run 'main.py'. A new column titled 'CLASS' will be added to the 'Comments.csv' file with either a 1 or a 0 in each row. Spam is labelled with a 1.

## Introduction
The program analyses the inputted comments and finds a number of features that are then inputted into a machine learning model from scikit-learn. This model outputs the probability of each comment being spam and then labels all the comments as either spam or not spam based on this probability.

When tested on a seperate section of the dataset, the model correctly labels around 90% of all the comments.

## The model
The model is trained from a [dataset](https://archive.ics.uci.edu/ml/machine-learning-databases/00380/) of around 2000 hand-labelled comments from popular songs on YouTube from a few years ago. Due to the age of the comments and the particular context for which they were written, it was important to make the model as general as possible in order for it to work on comments from all kinds of videos.

Due to the training data's limitations, I restricted the features used by the model to the following:
* Comment length
* Frequency of upper case character
* Frequency of symbols
* Frequency of digits
* Number of URLs
* Frequency of around 100 common words found in spam comments

The model's input is a csv file with all the comments under the heading 'CONTENT'. The model outputs a new column to this file with the heading 'CLASS'. This column contains 1s for comments marked as spam and 0s for comments marked as not spam. Currently, for the model to label a comment as spam, a threshold probability of 60% must be exceeded.

## Improvement

To test the model throughout development I have compared the model's effectiveness against previous versions. I have measured effectiveness as the difference in percentage of comments labelled correctly by the model compared to a baseline that labels comments randomly (and usually labels around 50% correctly). The optimal effectiveness would therefore be around 50%. The following bar chart shows a comparison of the different combinations of the first features I implemented (L - Length, C - Capitals, S - Symbols):
![LCS](https://raw.githubusercontent.com/jamesdtgoddard/YouTubeSpamCleaning/master/Training/Tests/LCS.png)It is evident that the model at this point was most effective when all three features were used simultaneously. The model was achieving an effectiveness of  25% meaning it labelled roughly 75% of comments correctly.

Below are a couple of bar charts showing the effectiveness of the model after new features were added:
![LCS](https://raw.githubusercontent.com/jamesdtgoddard/YouTubeSpamCleaning/master/Training/Tests/LCSD.png)![LCS](https://raw.githubusercontent.com/jamesdtgoddard/YouTubeSpamCleaning/master/Training/Tests/AllWords.png)
![LCS](https://raw.githubusercontent.com/jamesdtgoddard/YouTubeSpamCleaning/master/Training/Tests/URLS.png)Now that the model makes use of all of these features it achieves an effectiveness of over 40%, meaning it labels roughly 90% of comments correctly.

## Real-world results

After finishing development, I tested the model against a set of unlabelled comments from a very recent [YouTube video](https://www.youtube.com/watch?v=U1_0b7CkucA). 

While the results were not as good as when tested on comments from the original dataset, they were still good enough to be useful. I noticed that the program correctly identifies almost all of the spam comments amongst the data. The main problem is that the model labels many comments as spam that would not be seen as spam.

This is much better than if the program were to go the opposite way and label a lot of spam as not spam.

It seems that the model tends to label roughly 15% of data as spam when in reality only between 5% and 10% of the data would be seen as such.

## Conclusion

Overall, I believe that the program is effective enough to be useful as it is very good at identifying comments that are spam. If the dataset being searched is large then the elimination of a fraction of the non-spam data is not a big problem.
