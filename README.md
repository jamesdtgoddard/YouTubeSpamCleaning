# YouTube Spam Cleaning

This program recognises spam amongst YouTube comments. It currently predicts whether a comment is spam or not with a 90% accuracy.

INSTRUCTIONS:

1. Place all the comments you want checking in the 'Comments.csv' file under the title 'CONTENT'
2. Change the 'FILE_PATH' variable in 'main.py' to the path to the folder containing 'main.py'
3. Run 'main.py'. A new column titled 'CLASS' will be added to the 'Comments.csv' file with either a 1 or a 0 in each row. Spam is labelled with a 1.