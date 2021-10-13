# Import libraries
import numpy as np 
import pandas as pd
import plotly.express as px
import re
import string

# for all NLP related operations on text
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

# To identify the sentiment of text
from textblob import TextBlob

# To expanding the dispay of text column
pd.options.display.max_columns = 100

# To load the data
data = pd.read_csv("./data/tweets_scraped.csv", encoding="ISO-8859-1")

# To take only the tweet column from the dataset and make a dataframe
df = pd.DataFrame(data['tweet'])

# To remove '@names' from the tweets
def remove_pattern(text, pattern_regex):
    r = re.findall(pattern_regex, text)
    for i in r:
        text = re.sub(i, '', text)
    return text 

# To keep cleaned tweets in a new column called 'tweets'
df['tweets'] = np.vectorize(remove_pattern)(df['tweet'], "@[\w]* | *RT*")

# To remove the links(http | https)
cleaned_tweets = []

for index, row in df.iterrows():
    # Here we are filtering out all the words that contains link
    words_without_links = [word for word in row.tweets.split() if 'http' not in word]
    cleaned_tweets.append(' '.join(words_without_links))

df['tweets'] = cleaned_tweets
