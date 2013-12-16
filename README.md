Influenza Trends
=================

1. Streamed Twiiter data using filters (flu, influenza)
2. Tokenized each twitter text and lemmatized the tokens to get proper words
3. Applied phrase segmentation using punctuation for each tweet
4. Trained and tagged the tweets with 3-gram tagging
5. Constructed a number of templates and triggered a count whenever a tweet matches each of the templates to create a vector table
6. Trained K-means classification with the vectored table with initial means set to known values from human judgement
