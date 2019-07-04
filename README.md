# Youtube Spam Cleaning

This program recognises spam amongst YouTube comments. It currently predicts whether a comment is spam or not with an 90% accuracy.

INSTRUCTIONS:

1. Place all the comments you want checking in the first column of the 'Comments.csv' file with cell A1 containing the title 'CONTENT'
2. Change the 'FILE_PATH' variable in 'main.py' to the path to the folder containing 'main.py'
3. Run 'main.py' and a list of 1s and 0s will be outputted. In the same order as your comments in the 'Comments.csv' file, a 1 represents spam and a 0 represents not spam